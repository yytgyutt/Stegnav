"""Small simulated home exploration demo."""

from __future__ import annotations

import json
from dataclasses import asdict

from .models import FrontierNode, Pose2D, Query, SceneNode
from .pipeline import ExplorationPipeline


def main() -> None:
    nodes = [
        SceneNode(
            node_id="sofa_01",
            label="sofa",
            aliases=["沙发"],
            pose=Pose2D(2.0, 1.0),
            room_id="living_room",
            appearance=(0.1, 0.8, 0.1),
        ),
        SceneNode(
            node_id="lamp_01",
            label="floor lamp",
            aliases=["落地灯", "客厅灯"],
            pose=Pose2D(3.2, 1.8),
            room_id="living_room",
            appearance=(0.9, 0.1, 0.1),
        ),
    ]
    frontiers = [
        FrontierNode(
            frontier_id="frontier_hallway",
            pose=Pose2D(5.0, 1.0),
            path_cost=3.0,
            information_gain=4.0,
            nearby_node_ids=["lamp_01"],
        )
    ]
    query = Query(
        text="找到客厅落地灯",
        preferred_room="living_room",
        embedding=(1.0, 0.0, 0.0),
    )
    pipeline = ExplorationPipeline()

    def simulated_executor(candidate):
        pose_by_id = {node.node_id: node.pose for node in nodes}
        pose_by_id.update({frontier.frontier_id: frontier.pose for frontier in frontiers})
        return True, True, "target visually verified", pose_by_id[candidate.candidate_id], 0.93

    event = pipeline.step(query, nodes, frontiers, simulated_executor)
    output = {
        "decision": asdict(event),
        "long_term_memory": [asdict(item) for item in pipeline.memory.verified_anchors],
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
