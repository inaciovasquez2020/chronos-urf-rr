# Chronos #1334/#1335 — isolated reproducibility archive

**Scope:** archival audit evidence from 2026-11-08/09, not a physical measurement, a production implementation, mathematical peer review, or a change to any frozen experiment. This folder is independent of draft PRs #1330, #1331, #1333, #1334, #1335 and does not supersede their heads.

- **PR #1334:** [source-to-determinant audit](https://github.com/inaciovasquez2020/chronos-urf-rr/pull/1334#issuecomment-6729038835), head `55a0405dfa0ad831f8ae6c04ad06c96b6b68e875`. The source-action highest-jet quadratic coefficients give an exact six-state descriptor determinant and the specialized rational bound. See `verify_1334_factorization.py`. The script pins the source-action and generator digests, differentiates the actual source Lagrangian to extract C,D,G,F, cross-checks two descriptor pivots, and checks the exact determinant and rational nonvanishing bound. It does not establish the physical correctness of the source action.
- **PR #1335:** [classifier defect and proposed preflight audit](https://github.com/inaciovasquez2020/chronos-urf-rr/pull/1335#issuecomment-6729157278), head `93a32286f67c2ec6730fce832b1ecddc4fc05d49`. The frozen July 12 v1 lock was not changed. `pinned_v2.py` is the exact source snapshot; `test_1335_adversarial.py` **intentionally passes when historical defects are reproduced**; its authorization test checks the pinned frozen protocol rather than asserting a constant equals itself. The new `test_1335_preview_contract.py` (18 checks), `test_1335_contract_gaps.py` (6), and `test_1335_status_separation.py` (5) archive the earlier isolated synthetic suites. They are NOT a production readiness test.
- `preflight_contract.md` lists the 16-block and provenance requirements and remaining validation blockers.

## Offline verification

```sh
python3 -B -m unittest discover -s external-audit/cdt-gfe-20261109 -p 'test_1335*.py' -v
python3 -B external-audit/cdt-gfe-20261109/verify_1334_factorization.py
```

The second command needs SymPy 1.14.0 and independently differentiates the pinned source action. It is installed only by the isolated CI job, not by the first. A timeout, missing SymPy, or other resource failure is **INCOMPLETE**, never PASS.

The archive now contains **37 discovered unittest methods**: eight adversarial reproductions, eighteen synthetic preflight checks, six gap reproductions, and five synthetic-status checks. An intentionally reproduced defect producing an expected result counts as an archive test PASS, not a fixed production classifier. CI on the revised head must be checked separately.

**No mathematical promotion:** `GLOBAL_GFE := OPEN`; `CDT_PHYSICAL_EXECUTION := NOT_AUTHORIZED`; `EXTERNAL_PEER_REVIEW := OPEN`; `MERGE_APPROVAL := NOT_GRANTED`.
