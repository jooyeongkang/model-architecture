from dataclasses import dataclass, field

from model_architecture.application.pipeline import Pipeline


@dataclass
class Trace:
    calls: list[str] = field(default_factory=list)


@dataclass
class FakeDataRepo:
    trace: Trace

    def retrieve(self, request: str, /) -> str:
        self.trace.calls.append(f"retrieve:{request}")
        return "  raw  "


@dataclass
class FakeData:
    trace: Trace

    def process(self, raw_data: str, /) -> str:
        self.trace.calls.append("process")
        return raw_data.strip()


@dataclass
class FakeModel:
    trace: Trace

    def run(self, model_input: str, /) -> str:
        self.trace.calls.append("model")
        return model_input.upper()


@dataclass
class FakeOutput:
    trace: Trace

    def generate(self, model_result: str, /) -> str:
        self.trace.calls.append("output")
        return f"artifact:{model_result}"


def test_pipeline_coordinates_dependencies_in_order() -> None:
    trace = Trace()
    pipeline: Pipeline[str, str, str, str, str] = Pipeline(
        data_repo=FakeDataRepo(trace),
        data=FakeData(trace),
        model=FakeModel(trace),
        outputs=(FakeOutput(trace),),
    )

    result = pipeline.run("request-1")

    assert result.model_result == "RAW"
    assert result.artifacts == ("artifact:RAW",)
    assert trace.calls == ["retrieve:request-1", "process", "model", "output"]


def test_pipeline_can_return_a_result_without_outputs() -> None:
    trace = Trace()
    pipeline: Pipeline[str, str, str, str, str] = Pipeline(
        data_repo=FakeDataRepo(trace),
        data=FakeData(trace),
        model=FakeModel(trace),
    )

    result = pipeline.run("request-2")

    assert result.model_result == "RAW"
    assert result.artifacts == ()
