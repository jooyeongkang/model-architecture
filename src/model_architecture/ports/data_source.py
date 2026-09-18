"""Inbound boundary: where raw data comes from."""

from typing import Protocol


class DataSource[RequestT, RawDataT](Protocol):
    """Fetch raw data for one model execution request.

    This is the only contract allowed to reach a database, object store,
    API, or filesystem. Adapters in ``adapters.data_sources`` implement it.
    """

    def retrieve(self, request: RequestT, /) -> RawDataT:
        """Return raw, unvalidated data for the given request."""
        ...
