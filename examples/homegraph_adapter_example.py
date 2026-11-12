"""Run with: PYTHONPATH=src python3 examples/homegraph_adapter_example.py"""

import json

from stegnav_reproduction.homegraph_adapter import HomeGraphAdapter


document = {
    "schema": "example-only",
    "nodes": [
        {
            "id": "lamp_01",
            "type": "device",
            "name": "书房灯",
            "room_id": "study",
            "pose": {"x": 2.3, "y": 4.1, "yaw": 0.0},
            "properties": {"controllable": True},
        }
    ],
}

adapter = HomeGraphAdapter(document)
adapter.upsert_verified_object(
    node_id="chair_new_01",
    label="chair",
    room_id="study",
    x=1.8,
    y=3.7,
    confidence=0.92,
)

print(json.dumps(adapter.to_document(), ensure_ascii=False, indent=2))
