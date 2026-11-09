# Chronos #1334/#1335 — isolated reproducibility archive

**Scope:** archival audit evidence from 2026-11-08/09, not a physical measurement, a production implementation, mathematical peer review, or a change to any frozen experiment. This folder is independent of draft PRs #1330, #1331, #1333, #1334, #1335 and does not supersede their heads.

- **PR #1334:** [source-to-determinant audit](https://github.com/inaciovasquez2020/chronos-urf-rr/pull/1334#issuecomment-6729038835), head `55a0405dfa0ad831f8ae6c04ad06c96b6b68e875`. The source-action highest-jet quadratic coefficients give an exact six-state descriptor determinant and the specialized rational bound. See `verify_1334_factorization.py`. The script checks algebra *from extracted coefficients*, not the physical correctness or full source-to-Euler derivation.
- **PR #1335:** [classifier defect and proposed preflight audit](https://github.com/inaciovasquez2020/chronos-urf-rr/pull/1335#issuecomment-6729157278), head `93a32286f67c2ec6730fce832b1ecddc4fc05d49`. The frozen July 12 v1 lock was not changed. `pinned_v2.py` is the exact source snapshot; `test_1335_adversarial.py` **intentionally passes when historical defects are reproduced**. It is not a production readiness test.
- `preflight_contract.md` lists the 16-block and provenance requirements and remaining validation blockers.

## Offline verification

```sh
python3 -B -m unittest discover -s external-audit/cdt-gfe-20261109 -p 'test_1335_adversarial.py' -v
python3 -B external-audit/cdt-gfe-20261109/verify_1334_factorization.py
```

The second command needs SymPy; it is installed only by the isolated CI job, not by the first. A timeout, missing SymPy, or other resource failure is **INCOMPLETE**, never PASS.

Known test state at archival submission: pinned v2 source and original audit files were validated in an isolated container with Python 3.13.5, SymPy 1.14.0: 18/18 existing audit checks PASS, 6/6 contract-gap checks reproduced, 5/5 status-separation prototype checks PASS, #1334 exact factorization PASS. This folder's new CI result must be checked separately.

**No mathematical promotion:** `GLOBAL_GFE := OPEN`; `CDT_PHYSICAL_EXECUTION := NOT_AUTHORIZED`; `EXTERNAL_PEER_REVIEW := OPEN`; `MERGE_APPROVAL := NOT_GRANTED`.
