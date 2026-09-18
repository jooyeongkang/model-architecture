"""Input port for raw data retrieval."""

from typing import Protocol


class DataRepo[RequestT, RawDataT](Protocol):
    """Retrieve raw data from an external or in-memory source."""

    def retrieve(self, request: RequestT, /) -> RawDataT:
        """Retrieve raw data for a model execution request."""
        ...
