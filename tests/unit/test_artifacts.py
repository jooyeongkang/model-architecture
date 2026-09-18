import pytest

from model_architecture.adapters.renderers import PlotRenderer
from model_architecture.artifacts import PlotArtifact, PlotSeries, TableArtifact


def test_table_artifact_rejects_rows_with_wrong_width() -> None:
    with pytest.raises(ValueError, match="match the number of columns"):
        TableArtifact(name="invalid", columns=("a", "b"), rows=((1,),))


def test_plot_series_rejects_mismatched_coordinates() -> None:
    with pytest.raises(ValueError, match="equal lengths"):
        PlotSeries(name="invalid", x=(1.0,), y=(1.0, 2.0))


def test_plot_renderer_maps_a_result_to_an_artifact() -> None:
    expected = PlotArtifact(
        title="result",
        kind="line",
        series=(PlotSeries(name="value", x=(1.0,), y=(2.0,)),),
    )
    renderer = PlotRenderer[int](lambda _: expected)

    assert renderer.render(2) == expected
