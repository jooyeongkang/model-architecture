"""Reference model that summarizes numeric input."""

from dataclasses import dataclass
from math import isfinite

from model_architecture.adapters.outputs.artifacts import TableArtifact
from model_architecture.domain.errors import DataValidationError


@dataclass(frozen=True, slots=True)
class SummaryRequest:
    values: tuple[float, ...]


@dataclass(frozen=True, slots=True)
class SummaryResult:
    count: int
    total: float
    mean: float


class SummaryDataRepo:
    """Example repository that reads raw values from the request."""

    def retrieve(self, request: SummaryRequest, /) -> tuple[float, ...]:
        return request.values


class NumericData:
    """Validate raw values before they enter the model."""

    def process(self, raw_data: tuple[float, ...], /) -> tuple[float, ...]:
        if not raw_data:
            raise DataValidationError("At least one value is required.")
        if not all(isfinite(value) for value in raw_data):
            raise DataValidationError("All values must be finite numbers.")
        return raw_data


class SummaryModel:
    """Apply the example business calculation."""

    def run(self, model_input: tuple[float, ...], /) -> SummaryResult:
        total = sum(model_input)
        return SummaryResult(
            count=len(model_input),
            total=total,
            mean=total / len(model_input),
        )


def summary_table(result: SummaryResult) -> TableArtifact:
    """Map the example result to a presentation-neutral table."""

    return TableArtifact(
        name="summary",
        columns=("metric", "value"),
        rows=(
            ("count", result.count),
            ("total", result.total),
            ("mean", result.mean),
        ),
    )
