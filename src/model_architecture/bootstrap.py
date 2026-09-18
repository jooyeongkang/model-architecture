"""Composition root: construct and connect concrete dependencies here."""

from model_architecture.adapters.outputs.artifacts import TableArtifact
from model_architecture.adapters.outputs.mapped import TableOutput
from model_architecture.application.pipeline import Pipeline
from model_architecture.examples.summary import (
    NumericData,
    SummaryDataRepo,
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
        data_repo=SummaryDataRepo(),
        data=NumericData(),
        model=SummaryModel(),
        outputs=(TableOutput(summary_table),),
    )
