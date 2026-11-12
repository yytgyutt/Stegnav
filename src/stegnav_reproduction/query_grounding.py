"""Query-to-scene grounding baseline.

The paper's learned components are not reproduced here.  This module provides
an inspectable deterministic baseline that can later be replaced by a VLM or
text/image encoder.
"""

from __future__ import annotations

import math
import re
from typing import Iterable, List, Sequence, Set

from .models import Query, RankedCandidate, SceneNode


def _tokens(text: str) -> Set[str]:
    return set(re.findall(r"[\w\u4e00-\u9fff]+", text.lower()))


def cosine_similarity(left: Sequence[float], right: Sequence[float]) -> float:
    if not left or not right or len(left) != len(right):
        return 0.0
    dot = sum(a * b for a, b in zip(left, right))
    left_norm = math.sqrt(sum(value * value for value in left))
    right_norm = math.sqrt(sum(value * value for value in right))
    if left_norm == 0.0 or right_norm == 0.0:
        return 0.0
    return dot / (left_norm * right_norm)


def rank_scene_nodes(
    query: Query,
    nodes: Iterable[SceneNode],
    semantic_weight: float = 0.55,
    appearance_weight: float = 0.30,
    room_weight: float = 0.15,
) -> List[RankedCandidate]:
    query_tokens = _tokens(query.text)
    ranked = []
    for node in nodes:
        name_tokens = _tokens(" ".join([node.label] + node.aliases))
        union = query_tokens | name_tokens
        semantic = len(query_tokens & name_tokens) / float(len(union) or 1)
        appearance = max(0.0, cosine_similarity(query.embedding, node.appearance))
        room = float(bool(query.preferred_room and node.room_id == query.preferred_room))
        score = node.confidence * (
            semantic_weight * semantic
            + appearance_weight * appearance
            + room_weight * room
        )
        ranked.append(
            RankedCandidate(
                candidate_id=node.node_id,
                candidate_type="scene_node",
                score=score,
                reasons={
                    "semantic": semantic,
                    "appearance": appearance,
                    "room": room,
                    "confidence": node.confidence,
                },
            )
        )
    return sorted(ranked, key=lambda item: item.score, reverse=True)
