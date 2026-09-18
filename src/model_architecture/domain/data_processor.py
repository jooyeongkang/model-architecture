"""Contract for turning raw source data into validated model input."""

from typing import Protocol


class DataProcessor[RawDataT, ModelInputT](Protocol):
    """Validate and transform raw data into model-ready input.

    Implementations are pure: they never perform I/O, so the same raw data
    always produces the same model input.
    """

    def process(self, raw_data: RawDataT, /) -> ModelInputT:
        """Return model-ready input, or raise ``DataValidationError``."""
        ...
