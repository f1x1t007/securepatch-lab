"""Intentionally vulnerable teaching fixture. Never use in production."""
from pathlib import Path


def read_report_vulnerable(reports_dir: str | Path, filename: str) -> str:
    # Root cause: untrusted filename is joined and read without containment check.
    target = Path(reports_dir) / filename
    return target.read_text(encoding="utf-8")
