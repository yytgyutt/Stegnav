from stegnav_reproduction.models import FrontierNode, Pose2D, Query
from stegnav_reproduction.pipeline import ExplorationPipeline


def test_pipeline_explores_when_no_known_target_matches():
    pipeline = ExplorationPipeline()
    frontier = FrontierNode("frontier_1", Pose2D(3, 4), 1.0, 5.0)

    def executor(candidate):
        return True, True, "new room observed", frontier.pose, 0.8

    event = pipeline.step(Query("unknown object"), [], [frontier], executor)
    assert event.target_id == "frontier_1"
    assert event.target_type == "frontier"
    assert pipeline.memory.find_anchor("frontier_1") is not None
