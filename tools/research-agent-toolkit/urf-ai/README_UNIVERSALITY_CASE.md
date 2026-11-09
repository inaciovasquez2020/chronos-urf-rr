# Isolated URF-AI Universality Bridge regression case

This lightweight archive contains an isolated research candidate, not a modified GitHub repository. It has no model inference or automated network actions. `PYTHONPATH=.` allows running the tests without installing anything.

## What to read

1. `UNIVERSALITY_BRIDGE_AUDIT_20261109.md` — mathematical proof/refutation notes and status boundary.
2. `receipts/universality_bridge_audit_20261109.json` — exact, bounded audit receipt, bound to the reviewed PDF SHA-256.
3. `urf_ai/bridge_cases.py` — bounded deterministic transcript and entropy fixtures.
4. `tests/test_bridge_cases.py` — adversarial source-specific regressions.

## Prerequisite

Python 3.11+ is recommended. Only the Python standard library is required for the included unittest commands. The original PDF is **not** redistributed in this archive; its reviewed SHA-256 is `34096bfa667267624b5b6ad3b76ccb7b0d9eca8e90f129f85ad4b8b9a7eabc30`.

## macOS / zsh commands (no downloads or installations)

From the directory in which you extracted the zip:

```bash
PYTHONPATH="$PWD" python3 -m unittest discover -s tests -p 'test_*.py' -q
PYTHONPATH="$PWD" python3 -m unittest discover -s paired_eval -p 'test_*.py' -q
```

If the reviewed PDF is present on your Mac, reproduce the SHA-bound report by substituting its real path:

```bash
PYTHONPATH="$PWD" python3 tools/run_universality_bridge_audit.py --source '/absolute/path/to/the/reviewed.pdf'
```

The PDF fingerprint must match; otherwise the runner exits without a PASS. This fixture is disclosed and **not** an unseen model test. No repository mutation, push, promotion, external model call, or Lean verification is authorized by these scripts.

## Added second-stage SAT information/query audit (2026-11-09)

`SAT_INPUT_INFORMATION_NO_GO_20261109.md` proves the *read-first no-go boundary*
for input-information-only SAT hardness arguments and separates it from the
exact restricted 1-CNF sensitivity/query lower bound. This is a mathematical
research note, not a Lean proof or claimed P-vs-NP result.

The candidate now includes 11 source/structural cases and 71 unit tests
(59 primary + 12 paired-evaluator harness tests; the paired harness uses mocked
responses, **not independent GPT-6 model calls**). No remote repo or Mac changes.

With the original reviewed PDF available (absolute path required), from the
extracted candidate directory:

```bash
PYTHONPATH="$PWD" python3 tools/run_sat_query_boundary_audit.py --source '/absolute/path/to/reviewed.pdf'
```

The source SHA-256 is required to match exactly. The runner prints JSON only;
it makes no network calls and does not modify the source PDF.
