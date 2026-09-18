"""Renderers backed by an injected mapping function.

A new output is a function, not a class: write ``ModelResult -> Artifact``
and wrap it in the matching renderer.
"""

from collections.abc import Callable
from dataclasses import dataclass

from model_architecture.artifacts import PlotArtifact, TableArtifact


@dataclass(frozen=True, slots=True)
class TableRenderer[ModelResultT]:
    """Map a model result into a table artifact."""

    mapper: Callable[[ModelResultT], TableArtifact]

    def render(self, model_result: ModelResultT, /) -> TableArtifact:
        return self.mapper(model_result)


@dataclass(frozen=True, slots=True)
class PlotRenderer[ModelResultT]:
    """Map a model result into a plot artifact."""

    mapper: Callable[[ModelResultT], PlotArtifact]

    def render(self, model_result: ModelResultT, /) -> PlotArtifact:
        return self.mapper(model_result)
