"""Unofficial paper-inspired STEGNav reproduction components."""

from .models import FrontierNode, Pose2D, Query, SceneNode
from .pipeline import ExplorationPipeline

__all__ = [
    "ExplorationPipeline",
    "FrontierNode",
    "Pose2D",
    "Query",
    "SceneNode",
]

__version__ = "0.1.0"
