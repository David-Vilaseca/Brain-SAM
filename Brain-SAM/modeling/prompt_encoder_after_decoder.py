"""Compatibility import for checkpoints produced with the older module name."""

from .prompt_encoder import PromptEncoder3D, TwoWayTransformer

__all__ = ["PromptEncoder3D", "TwoWayTransformer"]
