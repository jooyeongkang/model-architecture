"""Orchestrate repository, processing, model, and output objects."""

from dataclasses import dataclass

from model_architecture.domain.contracts import Data, Model
from model_architecture.ports.data_repo import DataRepo
from model_architecture.ports.output import Output


@dataclass(frozen=True, slots=True)
class PipelineResult[ModelResultT, ArtifactT]:
    """The business result and every generated presentation artifact."""

    model_result: ModelResultT
    artifacts: tuple[ArtifactT, ...]


@dataclass(frozen=True, slots=True)
class Pipeline[RequestT, RawDataT, ModelInputT, ModelResultT, ArtifactT]:
    """Coordinate one complete model execution.

    Dependencies are supplied by the composition root in ``bootstrap.py``.
    The pipeline owns sequencing but contains no retrieval, transformation,
    business, or presentation logic itself.
    """

    data_repo: DataRepo[RequestT, RawDataT]
    data: Data[RawDataT, ModelInputT]
    model: Model[ModelInputT, ModelResultT]
    outputs: tuple[Output[ModelResultT, ArtifactT], ...] = ()

    def run(self, request: RequestT, /) -> PipelineResult[ModelResultT, ArtifactT]:
        raw_data = self.data_repo.retrieve(request)
        model_input = self.data.process(raw_data)
        model_result = self.model.run(model_input)
        artifacts = tuple(output.generate(model_result) for output in self.outputs)
        return PipelineResult(model_result=model_result, artifacts=artifacts)
