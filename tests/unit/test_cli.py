import pytest

from model_architecture.entrypoints.cli import main


def test_cli_prints_the_generated_table(capsys: pytest.CaptureFixture[str]) -> None:
    exit_code = main(["10", "20", "30"])

    assert exit_code == 0
    assert capsys.readouterr().out == "metric\tvalue\ncount\t3\ntotal\t60.0\nmean\t20.0\n"


def test_cli_reports_invalid_data_without_a_traceback(
    capsys: pytest.CaptureFixture[str],
) -> None:
    exit_code = main(["nan"])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert captured.out == ""
    assert captured.err == "error: All values must be finite numbers.\n"


def test_cli_rejects_missing_arguments() -> None:
    with pytest.raises(SystemExit) as exit_info:
        main([])

    assert exit_info.value.code == 2
