"""Library-neutral artifacts produced by output adapters."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TableArtifact:
    """A serializable table representation."""

    name: str
    columns: tuple[str, ...]
    rows: tuple[tuple[object, ...], ...]

    def __post_init__(self) -> None:
        expected_width = len(self.columns)
        if any(len(row) != expected_width for row in self.rows):
            message = "Every table row must match the number of columns."
            raise ValueError(message)


@dataclass(frozen=True, slots=True)
class PlotSeries:
    """One named numeric series in a plot artifact."""

    name: str
    x: tuple[float, ...]
    y: tuple[float, ...]

    def __post_init__(self) -> None:
        if len(self.x) != len(self.y):
            message = "Plot series x and y values must have equal lengths."
            raise ValueError(message)


@dataclass(frozen=True, slots=True)
class PlotArtifact:
    """A plotting-library-neutral plot specification."""

    title: str
    kind: str
    series: tuple[PlotSeries, ...]
    x_label: str = ""
    y_label: str = ""
