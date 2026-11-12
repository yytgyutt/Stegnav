"""Select-execute-verify-update loop for the reproduction scaffold."""

from __future__ import annotations

from typing import Callable, Dict, Iterable, List, Optional, Tuple

from .frontier_grounding import rank_frontiers
from .memory import EventMemory
from .models import DecisionEvent, FrontierNode, Pose2D, Query, RankedCandidate, SceneNode
from .policy import RuleBasedPolicy
from .query_grounding import rank_scene_nodes

ExecutionResult = Tuple[bool, bool, str, Pose2D, float]
Executor = Callable[[RankedCandidate], ExecutionResult]


class ExplorationPipeline:
    def __init__(
        self,
        memory: Optional[EventMemory] = None,
        policy: Optional[RuleBasedPolicy] = None,
    ) -> None:
        self.memory = memory or EventMemory()
        self.policy = policy or RuleBasedPolicy()
        self.step_count = 0

    def rank(
        self,
        query: Query,
        nodes: Iterable[SceneNode],
        frontiers: Iterable[FrontierNode],
    ) -> Tuple[List[RankedCandidate], List[RankedCandidate]]:
        known = rank_scene_nodes(query, nodes)
        semantic_scores = {item.candidate_id: item.score for item in known}
        unknown = rank_frontiers(frontiers, semantic_scores)
        return known, unknown

    def step(
        self,
        query: Query,
        nodes: Iterable[SceneNode],
        frontiers: Iterable[FrontierNode],
        executor: Executor,
    ) -> DecisionEvent:
        known, unknown = self.rank(query, nodes, frontiers)
        choice = self.policy.choose(known, unknown)
        if choice is None:
            raise RuntimeError("no known target or reachable frontier is available")

        success, verified, observation, pose, confidence = executor(choice)
        self.step_count += 1
        event = DecisionEvent(
            step=self.step_count,
            query_text=query.text,
            target_id=choice.candidate_id,
            target_type=choice.candidate_type,
            score=choice.score,
            success=success,
            verified=verified,
            observation=observation,
        )
        self.memory.record(event)
        if success and verified:
            self.memory.promote(event, pose=pose, confidence=confidence)
        return event
