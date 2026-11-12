"""Bounded short-term events and verified long-term anchors."""

from __future__ import annotations

from collections import deque
from typing import Deque, Dict, Iterable, List, Optional

from .models import DecisionEvent, Pose2D, VerifiedEventAnchor


class EventMemory:
    def __init__(self, short_capacity: int = 16, long_capacity: int = 128) -> None:
        self._short = deque(maxlen=short_capacity)  # type: Deque[DecisionEvent]
        self._long = {}  # type: Dict[str, VerifiedEventAnchor]
        self._long_capacity = long_capacity

    @property
    def recent_events(self) -> List[DecisionEvent]:
        return list(self._short)

    @property
    def verified_anchors(self) -> List[VerifiedEventAnchor]:
        return sorted(self._long.values(), key=lambda item: item.last_verified_step)

    def record(self, event: DecisionEvent) -> None:
        self._short.append(event)

    def promote(
        self,
        event: DecisionEvent,
        pose: Pose2D,
        confidence: float,
    ) -> VerifiedEventAnchor:
        if not event.success or not event.verified:
            raise ValueError("only successful, verified events can enter long-term memory")
        anchor_id = "{}:{}".format(event.target_type, event.target_id)
        anchor = VerifiedEventAnchor(
            anchor_id=anchor_id,
            node_id=event.target_id,
            query_text=event.query_text,
            pose=pose,
            confidence=confidence,
            observation=event.observation,
            last_verified_step=event.step,
        )
        self._long[anchor_id] = anchor
        self._trim_long_term()
        return anchor

    def find_anchor(self, node_id: str) -> Optional[VerifiedEventAnchor]:
        for anchor in self._long.values():
            if anchor.node_id == node_id:
                return anchor
        return None

    def load_anchors(self, anchors: Iterable[VerifiedEventAnchor]) -> None:
        for anchor in anchors:
            self._long[anchor.anchor_id] = anchor
        self._trim_long_term()

    def _trim_long_term(self) -> None:
        overflow = len(self._long) - self._long_capacity
        if overflow <= 0:
            return
        oldest = sorted(self._long.values(), key=lambda item: item.last_verified_step)
        for anchor in oldest[:overflow]:
            self._long.pop(anchor.anchor_id, None)
