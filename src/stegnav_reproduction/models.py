"""Small, dependency-free data contracts used by the reproduction scaffold."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence


@dataclass(frozen=True)
class Pose2D:
    x: float
    y: float
    yaw: float = 0.0


@dataclass
class SceneNode:
    node_id: str
    label: str
    pose: Pose2D
    room_id: Optional[str] = None
    aliases: List[str] = field(default_factory=list)
    appearance: Sequence[float] = field(default_factory=tuple)
    confidence: float = 1.0
    properties: Dict[str, object] = field(default_factory=dict)


@dataclass
class FrontierNode:
    frontier_id: str
    pose: Pose2D
    path_cost: float
    information_gain: float
    reachable: bool = True
    nearby_node_ids: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class Query:
    text: str
    preferred_room: Optional[str] = None
    embedding: Sequence[float] = field(default_factory=tuple)


@dataclass
class RankedCandidate:
    candidate_id: str
    candidate_type: str
    score: float
    reasons: Dict[str, float] = field(default_factory=dict)


@dataclass
class DecisionEvent:
    step: int
    query_text: str
    target_id: str
    target_type: str
    score: float
    success: bool
    verified: bool
    observation: str = ""


@dataclass
class VerifiedEventAnchor:
    anchor_id: str
    node_id: str
    query_text: str
    pose: Pose2D
    confidence: float
    observation: str
    last_verified_step: int
