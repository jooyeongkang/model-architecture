import pytest

from model_architecture.entrypoints.cli import main


def test_cli_prints_the_generated_table(capsys: pytest.CaptureFixture[str]) -> None:
    main(["10", "20", "30"])

    output = capsys.readouterr().out
    assert output == "metric\tvalue\ncount\t3\ntotal\t60.0\nmean\t20.0\n"
