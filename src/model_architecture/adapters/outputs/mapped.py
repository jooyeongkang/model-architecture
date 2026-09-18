"""Output adapters backed by injected mapping functions."""

from collections.abc import Callable
from dataclasses import dataclass

from model_architecture.adapters.outputs.artifacts import PlotArtifact, TableArtifact


@dataclass(frozen=True, slots=True)
class TableOutput[ModelResultT]:
    """Map a model result into a table artifact."""

    mapper: Callable[[ModelResultT], TableArtifact]

    def generate(self, model_result: ModelResultT, /) -> TableArtifact:
        return self.mapper(model_result)


@dataclass(frozen=True, slots=True)
class PlotOutput[ModelResultT]:
    """Map a model result into a plot artifact."""

    mapper: Callable[[ModelResultT], PlotArtifact]

    def generate(self, model_result: ModelResultT, /) -> PlotArtifact:
        return self.mapper(model_result)
