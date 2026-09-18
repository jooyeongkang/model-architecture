"""Output adapter implementations."""

from model_architecture.adapters.outputs.artifacts import PlotArtifact, PlotSeries, TableArtifact
from model_architecture.adapters.outputs.mapped import PlotOutput, TableOutput

__all__ = ["PlotArtifact", "PlotOutput", "PlotSeries", "TableArtifact", "TableOutput"]
