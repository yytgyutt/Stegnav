"""A simple policy over grounded known targets and exploration frontiers."""

from __future__ import annotations

from typing import Iterable, Optional

from .models import RankedCandidate


class RuleBasedPolicy:
    def __init__(self, known_target_threshold: float = 0.25) -> None:
        self.known_target_threshold = known_target_threshold

    def choose(
        self,
        known_targets: Iterable[RankedCandidate],
        frontiers: Iterable[RankedCandidate],
    ) -> Optional[RankedCandidate]:
        known = list(known_targets)
        unknown = list(frontiers)
        if known and known[0].score >= self.known_target_threshold:
            return known[0]
        if unknown:
            return unknown[0]
        return known[0] if known else None
