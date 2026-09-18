"""Contract for the business calculation itself."""

from typing import Protocol


class Model[ModelInputT, ModelResultT](Protocol):
    """Run deterministic business logic against model-ready input.

    Implementations hold the rules, equations, or inference that the
    application exists to run. They never retrieve or render data.
    """

    def run(self, model_input: ModelInputT, /) -> ModelResultT:
        """Return a business result for the given model input."""
        ...
