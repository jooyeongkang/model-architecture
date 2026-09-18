"""A data source adapter backed by preloaded values."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class InMemoryDataSource[RequestT, RawDataT]:
    """Return preloaded raw data regardless of the request value.

    Useful as a stand-in for a real source in examples and tests.
    """

    raw_data: RawDataT

    def retrieve(self, request: RequestT, /) -> RawDataT:
        del request
        return self.raw_data
