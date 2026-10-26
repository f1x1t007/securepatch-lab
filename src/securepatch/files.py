"""Safe report-file access for the SecurePatch Lab demo."""
from pathlib import Path


def read_report(reports_dir: str | Path, filename: str) -> str:
    """Read a report only if its resolved path remains inside reports_dir.

    Raises:
        ValueError: if the requested path escapes the reports directory.
        FileNotFoundError: if the in-scope report does not exist.
    """
    base = Path(reports_dir).resolve()
    candidate = (base / filename).resolve()

    # Python 3.9+: this checks path components, not string prefixes.
    if not candidate.is_relative_to(base):
        raise ValueError("Requested path is outside the reports directory")

    return candidate.read_text(encoding="utf-8")
