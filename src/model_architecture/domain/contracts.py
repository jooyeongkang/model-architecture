"""Behavioral contracts owned by the domain layer."""

from typing import Protocol


class Data[RawDataT, ModelInputT](Protocol):
    """Transform raw repository data into validated model input."""

    def process(self, raw_data: RawDataT, /) -> ModelInputT:
        """Return model-ready input without performing external I/O."""
        ...


class Model[ModelInputT, ModelResultT](Protocol):
    """Run deterministic business logic against model-ready input."""

    def run(self, model_input: ModelInputT, /) -> ModelResultT:
        """Return a business result without retrieving or rendering data."""
        ...
