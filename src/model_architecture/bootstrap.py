"""Composition root: construct and connect concrete collaborators here.

This is the only module that names every layer at once. Entrypoints call
it; nothing else imports adapters directly.
"""

from model_architecture.adapters.renderers.mapped import TableRenderer
from model_architecture.application.pipeline import Pipeline
from model_architecture.artifacts import TableArtifact
from model_architecture.examples.summary import (
    NumericDataProcessor,
    SummaryDataSource,
    SummaryModel,
    SummaryRequest,
    SummaryResult,
    summary_table,
)


def build_summary_pipeline() -> Pipeline[
    SummaryRequest,
    tuple[float, ...],
    tuple[float, ...],
    SummaryResult,
    TableArtifact,
]:
    """Build the executable example with constructor injection."""

    return Pipeline(
        data_source=SummaryDataSource(),
        processor=NumericDataProcessor(),
        model=SummaryModel(),
        renderers=(TableRenderer(summary_table),),
    )
