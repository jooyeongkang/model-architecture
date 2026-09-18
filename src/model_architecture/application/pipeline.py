"""Sequence a data source, processor, model, and renderers into one run."""

from dataclasses import dataclass

from model_architecture.domain.data_processor import DataProcessor
from model_architecture.domain.model import Model
from model_architecture.ports.data_source import DataSource
from model_architecture.ports.output_renderer import OutputRenderer


@dataclass(frozen=True, slots=True)
class PipelineResult[ModelResultT, ArtifactT]:
    """The business result and every artifact rendered from it."""

    model_result: ModelResultT
    artifacts: tuple[ArtifactT, ...]


@dataclass(frozen=True, slots=True)
class Pipeline[RequestT, RawDataT, ModelInputT, ModelResultT, ArtifactT]:
    """Coordinate one complete model execution.

    Collaborators are supplied by the composition root in ``bootstrap.py``.
    The pipeline owns sequencing but contains no retrieval, transformation,
    business, or presentation logic itself.
    """

    data_source: DataSource[RequestT, RawDataT]
    processor: DataProcessor[RawDataT, ModelInputT]
    model: Model[ModelInputT, ModelResultT]
    renderers: tuple[OutputRenderer[ModelResultT, ArtifactT], ...] = ()

    def run(self, request: RequestT, /) -> PipelineResult[ModelResultT, ArtifactT]:
        raw_data = self.data_source.retrieve(request)
        model_input = self.processor.process(raw_data)
        model_result = self.model.run(model_input)
        artifacts = tuple(renderer.render(model_result) for renderer in self.renderers)
        return PipelineResult(model_result=model_result, artifacts=artifacts)
