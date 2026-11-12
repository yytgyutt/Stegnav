import pytest

from stegnav_reproduction.memory import EventMemory
from stegnav_reproduction.models import DecisionEvent, Pose2D


def test_only_verified_success_enters_long_term_memory():
    memory = EventMemory(short_capacity=2)
    failed = DecisionEvent(1, "find lamp", "lamp", "scene_node", 0.8, False, False)
    memory.record(failed)
    with pytest.raises(ValueError):
        memory.promote(failed, Pose2D(1, 2), 0.5)

    verified = DecisionEvent(2, "find lamp", "lamp", "scene_node", 0.9, True, True)
    memory.record(verified)
    anchor = memory.promote(verified, Pose2D(1, 2), 0.95)
    assert anchor.node_id == "lamp"
    assert len(memory.verified_anchors) == 1
