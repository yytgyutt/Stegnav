"""Ranks unknown-space frontiers using reachability, information and context."""

from __future__ import annotations

from typing import Dict, Iterable, List

from .models import FrontierNode, RankedCandidate


def rank_frontiers(
    frontiers: Iterable[FrontierNode],
    nearby_semantic_scores: Dict[str, float],
) -> List[RankedCandidate]:
    ranked = []
    for frontier in frontiers:
        if not frontier.reachable:
            continue
        semantic_hint = max(
            [nearby_semantic_scores.get(node_id, 0.0) for node_id in frontier.nearby_node_ids]
            or [0.0]
        )
        exploration = frontier.information_gain / (1.0 + max(frontier.path_cost, 0.0))
        score = 0.65 * exploration + 0.35 * semantic_hint
        ranked.append(
            RankedCandidate(
                candidate_id=frontier.frontier_id,
                candidate_type="frontier",
                score=score,
                reasons={
                    "exploration": exploration,
                    "semantic_hint": semantic_hint,
                    "path_cost": frontier.path_cost,
                },
            )
        )
    return sorted(ranked, key=lambda item: item.score, reverse=True)
