"""Lightweight verifier: check that core regression coverage remains present."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
TEST_FILE = ROOT / "tests" / "test_files.py"
SOURCE_FILE = ROOT / "src" / "securepatch" / "files.py"

tests = TEST_FILE.read_text(encoding="utf-8")
source = SOURCE_FILE.read_text(encoding="utf-8")

checks = {
    "path traversal regression test exists": "def test_rejects_path_traversal" in tests,
    "test asserts rejection via exception": "with pytest.raises(ValueError" in tests,
    "implementation resolves requested path": ".resolve()" in source,
    "implementation enforces directory containment": "is_relative_to(base)" in source,
}

failed = [name for name, ok in checks.items() if not ok]
for name, ok in checks.items():
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")

if failed:
    print("\\nVERDICT: REJECT — one or more expected security checks are missing.")
    sys.exit(1)

print("\\nVERDICT: STATIC GUARDRAILS PASS — run pytest and review the diff as well.")
