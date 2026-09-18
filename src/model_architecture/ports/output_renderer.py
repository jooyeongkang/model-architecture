"""Outbound boundary: how a result becomes something presentable."""

from typing import Protocol


class OutputRenderer[ModelResultT, ArtifactT](Protocol):
    """Render one presentation artifact from a model result.

    Implementations in ``adapters.renderers`` decide the shape of the
    artifact. Delivering it — printing, uploading, plotting — is the
    entrypoint's job, not the renderer's.
    """

    def render(self, model_result: ModelResultT, /) -> ArtifactT:
        """Return a table, plot, file, or message artifact."""
        ...
