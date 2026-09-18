"""CLI entrypoint for the reference model."""

import argparse
from collections.abc import Sequence

from model_architecture.artifacts import TableArtifact
from model_architecture.bootstrap import build_summary_pipeline
from model_architecture.examples.summary import SummaryRequest


def _render_table(table: TableArtifact) -> str:
    rows = (table.columns, *table.rows)
    return "\n".join("\t".join(map(str, row)) for row in rows)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the model architecture example.")
    parser.add_argument("values", nargs="+", type=float, help="Values to summarize.")
    return parser


def main(argv: Sequence[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    pipeline = build_summary_pipeline()
    run = pipeline.run(SummaryRequest(values=tuple(args.values)))
    for artifact in run.artifacts:
        print(_render_table(artifact))
