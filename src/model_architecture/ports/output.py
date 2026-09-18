"""Output port for result presentation."""

from typing import Protocol


class Output[ModelResultT, ArtifactT](Protocol):
    """Generate one presentation artifact from a model result."""

    def generate(self, model_result: ModelResultT, /) -> ArtifactT:
        """Convert a model result into a table, plot, file, or message."""
        ...
