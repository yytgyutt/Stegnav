"""Best-effort adapter between heterogeneous HomeGraph JSON and scene nodes.

The adapter deliberately preserves unknown fields.  It is not a replacement
for the schema validator in a production HomeGraph repository.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Dict, Iterable, List, Mapping, MutableMapping, Optional

from .models import Pose2D, SceneNode


class HomeGraphAdapter:
    def __init__(self, document: Mapping[str, object]) -> None:
        self.document = deepcopy(dict(document))  # type: Dict[str, object]

    def _node_list(self) -> List[MutableMapping[str, object]]:
        raw_nodes = self.document.setdefault("nodes", [])
        if not isinstance(raw_nodes, list):
            raise ValueError("HomeGraph 'nodes' must be a list")
        return [node for node in raw_nodes if isinstance(node, MutableMapping)]

    def scene_nodes(self) -> List[SceneNode]:
        result = []
        for raw in self._node_list():
            node_type = str(raw.get("type", raw.get("node_type", "object")))
            if node_type not in {"object", "device", "portal", "semantic_object"}:
                continue
            node_id = str(raw.get("id", raw.get("node_id", "")))
            if not node_id:
                continue
            properties = raw.get("properties", {})
            if not isinstance(properties, dict):
                properties = {}
            pose = raw.get("pose", properties.get("pose", {}))
            if not isinstance(pose, dict):
                pose = {}
            aliases = raw.get("aliases", properties.get("aliases", []))
            if not isinstance(aliases, list):
                aliases = []
            result.append(
                SceneNode(
                    node_id=node_id,
                    label=str(raw.get("name", raw.get("label", node_id))),
                    pose=Pose2D(
                        x=float(pose.get("x", 0.0)),
                        y=float(pose.get("y", 0.0)),
                        yaw=float(pose.get("yaw", 0.0)),
                    ),
                    room_id=_optional_string(raw.get("room_id", properties.get("room_id"))),
                    aliases=[str(value) for value in aliases],
                    confidence=float(raw.get("confidence", properties.get("confidence", 1.0))),
                    properties=dict(properties),
                )
            )
        return result

    def upsert_verified_object(
        self,
        node_id: str,
        label: str,
        room_id: Optional[str],
        x: float,
        y: float,
        confidence: float,
    ) -> None:
        nodes = self._node_list()
        target = next((node for node in nodes if str(node.get("id")) == node_id), None)
        if target is None:
            target = {"id": node_id, "type": "object", "properties": {}}
            nodes.append(target)
            self.document["nodes"] = nodes
        target.update(
            {
                "name": label,
                "room_id": room_id,
                "pose": {"x": x, "y": y, "yaw": 0.0},
                "confidence": confidence,
            }
        )
        properties = target.setdefault("properties", {})
        if isinstance(properties, dict):
            properties.update(
                {
                    "memory_status": "verified",
                    "source": "stegnav_reproduction",
                }
            )

    def to_document(self) -> Dict[str, object]:
        return deepcopy(self.document)


def _optional_string(value: object) -> Optional[str]:
    return None if value is None else str(value)
