# Verification manifest — 2026-11-19

Base: 457cad0f700bf4e5068ad3162463922a85337739 (remote main).
Scope: research-only; no production files, root imports, requirements, or workflows changed.

## Actual isolated execution

Environment: Python 3.13.5; SymPy 1.14.0 for the branching script only.
Both scripts ran in the assistant's isolated environment, not the researcher's Mac. Both exited zero.
No new dependencies installed for this replay. The remote blobs were fetched after upload; both matched the executed local source Git blob SHA-1.

| File | SHA-256 | Git blob SHA-1 |
|---|---|---|
| gravity_coefficient_check.py | e6da7690e37eb2b0aff94caf9abfb4e4d83e6259b4aaefe549f657e84e016f70 | cd7443a29b2b92eb44ff1002c42e82513420ab32 |
| chronos_branching_covariance.py | 774701ded180a96e0bce64510ac5357284de89dd1f38d09b9ddc12f74206a619 | 692892291aac53fc7635bf66bb65972d71fbdc4c |

### Arithmetic script output

```
DIRICHLET_MOMENTS := PASS (m=2..64)
EXACT_PLANE_WAVE_COEFFICIENTS := 1/252 -23/7560
ARXIV_V2_COEFFICIENT_GAP := 11/37800
CONDITIONAL_REASSEMBLY_ARITHMETIC := PASS
CHAIN_JACOBIAN_INVERSE := PASS
NESTED_DESIGN_IDENTITY := PASS
GEOMETRIC_INPUTS_AND_LEAN := NOT_VERIFIED_BY_THIS_SCRIPT
```

### Branching script output (final lines)

```
EXACT_ASSERTIONS := PASS
SCALAR_VARIANCE_REDUCTION_PERCENT 93.2286966974
```

The branching replay also checked zero means, exact response and covariance matrices, positive definiteness, WJ=I, and the optimized covariance identity. Its input response is conformal; its covariance is leading-order flat-reference. No assertion here establishes the general curved-spacetime boundary differentiation.

## Reproduction

From this directory, with Python 3 and SymPy already installed (do not run Python with optimization flags):

```sh
python3 -B gravity_coefficient_check.py
python3 -B chronos_branching_covariance.py
```

A missing dependency, exception, time/resource interruption, or nonzero exit is NOT_RUN or incomplete/failed, never PASS.

## Remaining review and promotion gates

- Exact-head GitHub workflow status and repository-wide tests: NOT_RUN at archive preparation.
- Local Mac state: NOT_INSPECTED; local build: NOT_RUN.
- Lean compilation and axiom audit: NOT_RUN.
- Earlier finite-sample overlap integrations, orders 4–6 GLS, direct numerical quadrature and separate tensor scripts: NOT_REPLAYED; only historical results recorded.
- Exact plane-wave geometric argument: paper derivation, external AI cross-check supplied by researcher; no independent human review.
- General vacuum coefficient: CONDITIONAL; independent derivation of moving boundary and density contributions OPEN.
- Journal-version comparison, author response, novelty: OPEN.
- Einstein dynamics and pure-poset general reconstruction: OPEN.

A successful arithmetic check is not a verification of its geometric input. Preserve the explicit scope labels. No merge until full exact-HEAD review and approval. No private email content included.
