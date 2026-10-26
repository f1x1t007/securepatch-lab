# SecurePatch Lab: Security Regression Tests & AI Patch Verification

A small, reproducible Python project demonstrating how to verify security fixes and reject a misleading AI-agent patch.

> **Scope:** Local, synthetic demonstration only. No real credentials, sensitive files, or external targets are used.

## Vulnerability and impact

The demo models **path traversal** (CWE-22). A report-download function accepts a user-controlled filename and reads a file relative to a reports directory. Without enforcing the directory boundary, an input such as `../outside.txt` can resolve to a file outside the intended directory. In a real application, this may expose configuration, application data, or other files readable by the service account.

## Root cause and source locations

- `src/securepatch/files.py` — vulnerable and fixed file-resolution logic.
- `tests/test_files.py` — security regression tests.
- `scripts/verify_patch.py` — simple evidence-based verifier for expected security properties.
- `examples/bad_ai_patch.diff` — intentionally bad patch that disables the security assertion.

The vulnerable implementation joins the trusted base directory with an untrusted filename and reads it without verifying the resolved path remains beneath the base directory.

## Run it

Requires Python 3.10+.

```bash
python -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows PowerShell:
# .venv\Scripts\Activate.ps1

python -m pip install -r requirements.txt
pytest -q
python scripts/verify_patch.py
```

Expected result for the fixed code: all tests pass and the verifier reports that the key security conditions are satisfied.

## Original failing test

The core regression test is `test_rejects_path_traversal`. It asks the file-serving function to read a synthetic file located outside the reports directory and expects the request to be rejected with `ValueError`.

To observe the original failure safely, inspect the historical vulnerable implementation in `examples/vulnerable_files.py`. It is isolated from the active application and uses only a temporary directory created by the test. Do not deploy it.

## The patch and why it is appropriate

The fixed implementation:
1. Resolves the reports directory and requested path.
2. Uses `Path.resolve()` to normalize `..` and symlink components.
3. Checks containment with `Path.is_relative_to()` (Python 3.9+).
4. Rejects paths outside the approved directory before reading any content.
5. Preserves valid downloads, covered by a positive test.

This addresses the root cause rather than hiding the symptom. The regression suite tests both rejection of traversal and continued access to a legitimate report.

## Bad AI-agent patch: weakening the test

`examples/bad_ai_patch.diff` illustrates a common failure mode: an agent changes the test to skip or remove the traversal assertion instead of fixing the vulnerable code.

**Verdict: reject.** A green test run after removing the security assertion is not evidence of remediation. The test no longer checks the security property, and the vulnerable behavior can remain unchanged. The verifier checks that the regression test still contains the expected assertion; this is a useful guardrail, not a complete proof of security.

Evidence:
- The diff changes test logic rather than the vulnerable implementation.
- It removes or skips the assertion that traversal is rejected.
- The verifier flags the weakened test.
- The genuine fix passes the security regression test while preserving the valid-file test.

## Results after applying the fix

Run `pytest -q` and `python scripts/verify_patch.py`. The expected result is:
- legitimate report reads succeed;
- traversal attempts are rejected;
- missing files are rejected;
- the verifier confirms that the regression assertion is present.

Record the actual command output in your repository or CI run when you execute it locally. Do not claim a test result that you have not reproduced.

## Limitations and remaining concerns

- This is a focused teaching example, not a full web server or a comprehensive security audit.
- Filesystem race conditions may require stronger handling in high-risk deployments; path validation followed by a separate open can have time-of-check/time-of-use concerns.
- Production systems should consider symlink policy, OS permissions, least privilege, logging, and platform-specific path behavior.
- The verifier uses simple source checks and can be evaded by more sophisticated changes. Combine it with code review, behavioral tests, and independent security analysis.
- No automated test suite proves the absence of all vulnerabilities.

## Suggested repository structure

```text
securepatch-lab/
├── README.md
├── requirements.txt
├── src/securepatch/
│   ├── __init__.py
│   └── files.py
├── tests/
│   └── test_files.py
├── scripts/
│   └── verify_patch.py
└── examples/
    ├── vulnerable_files.py
    └── bad_ai_patch.diff
```

## Security references

- CWE-22: Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') — https://cwe.mitre.org/data/definitions/22.html
- OWASP Path Traversal — https://owasp.org/www-community/attacks/Path_Traversal

## Portfolio note

When presenting this project, explain the threat model, show the failing regression test, review the smallest effective fix, then demonstrate why the bad patch is rejected. Clearly label the vulnerable implementation as an intentionally unsafe teaching fixture.
