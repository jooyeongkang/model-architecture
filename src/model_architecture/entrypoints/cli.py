"""CLI entrypoint for the reference model."""

import argparse
import sys
from collections.abc import Sequence

from model_architecture.artifacts import TableArtifact
from model_architecture.bootstrap import build_summary_pipeline
from model_architecture.domain.errors import ModelArchitectureError
from model_architecture.examples.summary import SummaryRequest

EXIT_OK = 0
EXIT_INVALID_DATA = 1


def _render_table(table: TableArtifact) -> str:
    rows = (table.columns, *table.rows)
    return "\n".join("\t".join(map(str, row)) for row in rows)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the model architecture example.")
    parser.add_argument("values", nargs="+", type=float, help="Values to summarize.")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the pipeline and return a process exit code.

    Expected failures surface as a one-line message on stderr. Every error
    the domain raises inherits from ``ModelArchitectureError``, so an
    entrypoint only has to catch that one type. Anything else is a bug and
    is deliberately left to propagate with its traceback.
    """

    args = build_parser().parse_args(argv)
    pipeline = build_summary_pipeline()
    try:
        run = pipeline.run(SummaryRequest(values=tuple(args.values)))
    except ModelArchitectureError as error:
        print(f"error: {error}", file=sys.stderr)
        return EXIT_INVALID_DATA
    for artifact in run.artifacts:
        print(_render_table(artifact))
    return EXIT_OK
