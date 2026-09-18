"""End-to-end runs with every collaborator wired together.

These use ``InMemoryDataSource`` in place of a real repository, which is the
substitution a production test suite makes to keep I/O out of the run.
"""

import pytest

from model_architecture.adapters.data_sources import InMemoryDataSource
from model_architecture.adapters.renderers import PlotRenderer, TableRenderer
from model_architecture.application.pipeline import Pipeline
from model_architecture.artifacts import PlotArtifact, PlotSeries, TableArtifact
from model_architecture.domain.errors import DataValidationError
from model_architecture.examples.summary import (
    NumericDataProcessor,
    SummaryModel,
    SummaryRequest,
    SummaryResult,
    summary_table,
)


def summary_plot(result: SummaryResult) -> PlotArtifact:
    return PlotArtifact(
        title="summary",
        kind="bar",
        series=(PlotSeries(name="mean", x=(0.0,), y=(result.mean,)),),
    )


def build_pipeline(
    raw_data: tuple[float, ...],
) -> Pipeline[
    SummaryRequest,
    tuple[float, ...],
    tuple[float, ...],
    SummaryResult,
    TableArtifact | PlotArtifact,
]:
    """Wire the pipeline against a preloaded source instead of real I/O.

    ``ArtifactT`` is widened to a union because one pipeline may only carry
    renderers that agree on a single artifact type.
    """

    return Pipeline(
        data_source=InMemoryDataSource(raw_data),
        processor=NumericDataProcessor(),
        model=SummaryModel(),
        renderers=(TableRenderer(summary_table), PlotRenderer(summary_plot)),
    )


def test_swapped_data_source_feeds_the_whole_pipeline() -> None:
    pipeline = build_pipeline((2.0, 4.0, 6.0))

    run = pipeline.run(SummaryRequest(values=()))

    assert run.model_result == SummaryResult(count=3, total=12.0, mean=4.0)


def test_every_renderer_produces_its_own_artifact() -> None:
    pipeline = build_pipeline((2.0, 4.0, 6.0))

    run = pipeline.run(SummaryRequest(values=()))

    assert run.artifacts == (
        TableArtifact(
            name="summary",
            columns=("metric", "value"),
            rows=(("count", 3), ("total", 12.0), ("mean", 4.0)),
        ),
        PlotArtifact(
            title="summary",
            kind="bar",
            series=(PlotSeries(name="mean", x=(0.0,), y=(4.0,)),),
        ),
    )


def test_validation_failures_stop_before_the_model_runs() -> None:
    pipeline = build_pipeline(())

    with pytest.raises(DataValidationError, match="At least one value"):
        pipeline.run(SummaryRequest(values=()))
