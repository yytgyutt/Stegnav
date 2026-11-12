from stegnav_reproduction.frontier_grounding import rank_frontiers
from stegnav_reproduction.models import FrontierNode, Pose2D, Query, SceneNode
from stegnav_reproduction.query_grounding import rank_scene_nodes


def test_query_grounding_prefers_matching_alias_and_room():
    query = Query("找到书房灯", preferred_room="study")
    nodes = [
        SceneNode("lamp", "ceiling light", Pose2D(1, 1), "study", aliases=["书房灯"]),
        SceneNode("sofa", "sofa", Pose2D(2, 2), "living_room", aliases=["沙发"]),
    ]
    assert rank_scene_nodes(query, nodes)[0].candidate_id == "lamp"


def test_frontier_grounding_skips_unreachable_frontier():
    frontiers = [
        FrontierNode("blocked", Pose2D(0, 0), 1, 10, reachable=False),
        FrontierNode("open", Pose2D(1, 0), 2, 3, reachable=True),
    ]
    ranked = rank_frontiers(frontiers, {})
    assert [item.candidate_id for item in ranked] == ["open"]
