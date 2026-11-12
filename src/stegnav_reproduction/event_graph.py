"""Builds a compact spatio-temporal context graph for a decision step."""

from __future__ import annotations

import json
from dataclasses import asdict
from typing import Iterable

from .memory import EventMemory
from .models import FrontierNode, Query, SceneNode


def build_event_graph(
    query: Query,
    nodes: Iterable[SceneNode],
    frontiers: Iterable[FrontierNode],
    memory: EventMemory,
) -> dict:
    return {
        "query": asdict(query),
        "scene_nodes": [asdict(node) for node in nodes],
        "frontiers": [asdict(frontier) for frontier in frontiers],
        "recent_events": [asdict(event) for event in memory.recent_events],
        "verified_anchors": [asdict(anchor) for anchor in memory.verified_anchors],
    }


def serialize_event_graph(graph: dict) -> str:
    return json.dumps(graph, ensure_ascii=False, sort_keys=True)
