import pytest

from model_architecture.adapters.outputs.artifacts import PlotArtifact, PlotSeries, TableArtifact
from model_architecture.adapters.outputs.mapped import PlotOutput


def test_table_artifact_rejects_rows_with_wrong_width() -> None:
    with pytest.raises(ValueError, match="match the number of columns"):
        TableArtifact(name="invalid", columns=("a", "b"), rows=((1,),))


def test_plot_series_rejects_mismatched_coordinates() -> None:
    with pytest.raises(ValueError, match="equal lengths"):
        PlotSeries(name="invalid", x=(1.0,), y=(1.0, 2.0))


def test_plot_output_maps_a_result_to_an_artifact() -> None:
    expected = PlotArtifact(
        title="result",
        kind="line",
        series=(PlotSeries(name="value", x=(1.0,), y=(2.0,)),),
    )
    output = PlotOutput[int](lambda _: expected)

    assert output.generate(2) == expected
