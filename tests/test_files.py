from pathlib import Path

import pytest

from securepatch.files import read_report


def test_reads_legitimate_report(tmp_path: Path) -> None:
    reports = tmp_path / "reports"
    reports.mkdir()
    (reports / "weekly.txt").write_text("Synthetic report", encoding="utf-8")

    assert read_report(reports, "weekly.txt") == "Synthetic report"


def test_rejects_path_traversal(tmp_path: Path) -> None:
    reports = tmp_path / "reports"
    reports.mkdir()
    # Synthetic outside file: no real sensitive data is used.
    (tmp_path / "outside.txt").write_text("NOT A SECRET", encoding="utf-8")

    with pytest.raises(ValueError, match="outside the reports directory"):
        read_report(reports, "../outside.txt")


def test_missing_in_scope_report_raises(tmp_path: Path) -> None:
    reports = tmp_path / "reports"
    reports.mkdir()

    with pytest.raises(FileNotFoundError):
        read_report(reports, "missing.txt")
