"""A lightweight repository adapter for examples and tests."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class InMemoryDataRepo[RequestT, RawDataT]:
    """Return preloaded raw data regardless of the request value."""

    raw_data: RawDataT

    def retrieve(self, request: RequestT, /) -> RawDataT:
        del request
        return self.raw_data
