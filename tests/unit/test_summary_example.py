import pytest

from model_architecture.adapters.outputs.artifacts import TableArtifact
from model_architecture.bootstrap import build_summary_pipeline
from model_architecture.domain.errors import DataValidationError
from model_architecture.examples.summary import SummaryRequest, SummaryResult


def test_summary_pipeline_generates_business_result_and_table() -> None:
    pipeline = build_summary_pipeline()

    run = pipeline.run(SummaryRequest(values=(10.0, 20.0, 30.0)))

    assert run.model_result == SummaryResult(count=3, total=60.0, mean=20.0)
    assert run.artifacts == (
        TableArtifact(
            name="summary",
            columns=("metric", "value"),
            rows=(("count", 3), ("total", 60.0), ("mean", 20.0)),
        ),
    )


def test_summary_pipeline_rejects_empty_data() -> None:
    pipeline = build_summary_pipeline()

    with pytest.raises(DataValidationError, match="At least one value"):
        pipeline.run(SummaryRequest(values=()))


def test_summary_pipeline_rejects_non_finite_data() -> None:
    pipeline = build_summary_pipeline()

    with pytest.raises(DataValidationError, match="finite numbers"):
        pipeline.run(SummaryRequest(values=(float("inf"),)))
