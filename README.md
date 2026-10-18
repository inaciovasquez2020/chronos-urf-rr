# Chronos URF-RR

**Proof-facing research repository for the Chronos / Unified Rigidity Framework (URF).**

This repository maintains formalization surfaces, reproducible symbolic/numerical certificates, JSON receipts, tests, and explicit boundaries between established results and unresolved mathematical claims. A successful build or passing certificate validates only the properties actually checked; it does not by itself establish global theorem closure or physical interpretation.

## Current research snapshot

As of 2026-10-18, recent GfE work has advanced from the corrected axial projector/GQQ certificate to several more specific, finite-scope results:

- **Corrected projector and GQQ certificate:** exact P/Q rank and idempotence checks, the corrected GQQ calculation, and the associated rank distinction were recorded. The leading commutator obstruction remains explicit: \([G_{-1},P_0]=G_{-1}\ne 0\).
- **Fixed-point Riesz projector limit:** a rank-two contour limit was certified at the single parameter point \(M=1, r=3, \lambda=6, \omega=i/4\) (commit [461ace4](https://github.com/inaciovasquez2020/chronos-urf-rr/commit/461ace45e0474522449f86fa8c896ceb928c4f43)).
- **Local-uniform Riesz limit:** exact symbolic-M beta-valuation cancellation and a local contour argument near \(M=1\) were recorded. This is local, not a global uniformity result (commit [4d850b7](https://github.com/inaciovasquez2020/chronos-urf-rr/commit/4d850b71d6d85588cb6982ecddcb16b218cf83ff)).
- **Finite-beta full-source determinant guard:** exact determinant specialization and a finite-beta guard were added in commits [ee844ae](https://github.com/inaciovasquez2020/chronos-urf-rr/commit/ee844aeaa3f41e858ca3ee759951492fd0d2c1da) and [eb20d8a](https://github.com/inaciovasquez2020/chronos-urf-rr/commit/eb20d8aeaa56635ede6e74e2868f75fe3d8c548e).
- **Exterior corrected-GQQ rank loss:** the exterior rank-loss obstruction and its exact isolated root were certified in [commit 2136cdd](https://github.com/inaciovasquez2020/chronos-urf-rr/commit/2136cdd389bd94721228b6aff9b5b84d46bf2e8d).
- **Full-pencil exterior contour:** the latest recorded result certifies, by exact elimination, exclusion of full six-state pencil zeros on \(|z|=2\) at the exterior corrected-GQQ rank-loss point (commit [2cb279a](https://github.com/inaciovasquez2020/chronos-urf-rr/commit/2cb279ae40a9af83831bf06b1929ad59bc77d1eb)).

These are bounded certificate and local-analysis results. Their scope should not be enlarged beyond the hypotheses, parameter regions, and observables recorded in the corresponding artifacts.

## Explicit open boundaries

The repository does **not** claim any of the following as established by the results above:

- a finite-\(\beta\) invariant-projector or all-orders invariant-graph closure;
- a globally uniform complement estimate or global uniform Riesz-projector limit;
- a Fredholm resolution;
- endpoint admissibility;
- horizon or outgoing-boundary closure;
- an unconditional global mode or physical-instability conclusion;
- unrestricted Chronos-RR, unrestricted H4.1/FGL, P vs NP, or resolution of any Clay problem.

In particular, the exact exterior contour certificate is a point-specific exclusion result. It does not remove the rank-loss obstruction, prove a global complement bound, or close the full spectral problem.

## Repository role

- `urf-core` — shared definitions, theorem/library layer, and foundations.
- `chronos-urf-rr` — executable frontier, status, and conditional/certificate surfaces.
- `frontier-status-dashboard` — public status presentation and synchronization.

## Verification

Typical local checks, when run in the repository environment:

```zsh
lake build
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q
git diff --check
git status --short
```

Interpret the result narrowly: a successful build means the checked targets compile; a passing test means the assertions in that test passed. Neither substitutes for a missing proof obligation.

## Evidence and provenance

The repository uses formal modules, symbolic or numerical generators, machine-readable artifacts, status documents, and tests to preserve reproducibility and claim boundaries. Relevant locations include:

```text
CLAIMS.md
STATUS.md
STATUS_SNAPSHOT.md
OPEN_INPUTS_REGISTRY.md
docs/status/
artifacts/chronos/
lean/Chronos/Frontier/
tools/
tests/
boundaries.toml
```

Use the specific artifact and its recorded assumptions as the authority for each result. Historical status snapshots and older README-audit files may not reflect the latest research commits.

## Claim discipline

- A certificate is evidence for its stated finite or conditional claim, not for an unstated global theorem.
- Assumptions, axioms, `admit`, `sorry`, placeholders, and proof surfaces must remain distinguishable from completed proofs.
- Do not promote CI success, documentation status, or a clean worktree into mathematical closure.

**Overall status:** active conditional research frontier; several exact, bounded GfE certificates are recorded, while global spectral closure and the listed boundary obligations remain open.
