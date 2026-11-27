# Chronos URF-RR

**Proof-facing research repository for the Chronos / Unified Rigidity Framework (URF).**

This repository maintains formalization surfaces, reproducible symbolic/numerical certificates, JSON receipts, tests, and explicit boundaries between established results and unresolved mathematical claims. A successful build or passing certificate validates only the properties actually checked; it does not by itself establish global theorem closure or physical interpretation.

## Finite holonomy and locality

[The merged locality bridge note](docs/research/finite_holonomy_locality_bridge_001_004.md) records a candidate interface between bounded graph neighborhoods and finite transport. On a cycle of length greater than `2r + 1`, the observation model independently quotients each radius-`r` restriction by vertex gauge. The note documents a local observation collision for distinct global holonomies under that model. Formal integration and physical interpretation remain open.

## Event-first spacetime

Chronos supplies the four-dimensional event observables for the proposed transfer from [DFM-MKC Cosmology](https://github.com/inaciovasquez2020/dfm-mkc-cosmology). The finite [relative-conjugation audit](https://github.com/inaciovasquez2020/chronos-urf-rr/pull/1357) gives an exact \(S_3\) reconstruction obstruction under the stated observations.

From the repository root, replay the finite audit:

```bash
python3 tools/holonomy/verify_s3_relative_conjugation.py
```

**OPEN** — Match the coefficients of a specified 5D→4D reduction to a Chronos event observable, then compare its predictions with a matched four-dimensional model.

## Four-event Minkowski probability — 2026-11-27 UTC

[Mac-verified checkpoint (draft PR #1398, pinned revision)](https://github.com/inaciovasquez2020/chronos-urf-rr/blob/e6945b6946f500f917c8b427df411a0e796851b7/research/certificates/p42_physical_checkpoint_20261127/README.md): four IID uniform events in a unit Alexandrov interval in 3+1-dimensional Minkowski spacetime. The candidate probability that the first two elements of a uniformly selected linear extension are comparable is `p42 = 32*pi^2/7 - 13239637/294000`.

- LEAN_VERIFIED: physical common-future geometry, joint radial/angular/rapidity measure and explicit spacelike integral reduction. The [final eight-declaration axiom receipt](https://github.com/inaciovasquez2020/chronos-urf-rr/blob/e6945b6946f500f917c8b427df411a0e796851b7/research/certificates/p42_physical_checkpoint_20261127/verified/tmp.vmCoPZ4Zsi/LEAN.log) lists only propext, Classical.choice and Quot.sound.
- COMPUTATION_PASS: [exact arithmetic and finite-poset objective identity](https://github.com/inaciovasquez2020/chronos-urf-rr/blob/e6945b6946f500f917c8b427df411a0e796851b7/research/certificates/p42_physical_checkpoint_20261127/verified/tmp.qlXqdaOReV/COMPUTATION.log); 729 candidates, 219 labeled partial orders, 16 isomorphism classes.
- OPEN: full analytic evaluation in Lean, complete probability theorem and independent review/novelty. Fresh rebuild NOT_RUN. Research checkpoint is a pinned draft PR at the dated record, not a merge or global physical-closure claim.

## GfE research snapshot

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

See [Quickstart](QUICKSTART.md) for the repository setup.

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

## Cross-domain information recovery — 2026-11-27 UTC

Three scoped mathematical connections: 52 distinct audited Lean theorem declarations across two standalone certificates (41 + 11; the original 33 are counted once).

- [Chronos–Biological Friction, BFF #116](https://github.com/inaciovasquez2020/biological-friction-framework/blob/799b41b4692c71589587cba037f26f0ad4bff7fb/proofs/hidden-dissipation/receipt/HiddenDissipation.lean): merged; 33/33 audited declarations, fresh Linux build PASS. In finite cyclic Markov models with the stated stationary and path-gauge observations, different entropy production can be indistinguishable; sharp absolute-error minimax equals half maximal dissipation in the bounded current family. `BFF.HiddenDissipation.ring_observation_minimax`.
- [Biology–Cosmology, BFF #117](https://github.com/inaciovasquez2020/biological-friction-framework/blob/c5c8b2f24a0d4de57c764c161ab29c3689bec62f/proofs/hidden-dissipation/receipt/HiddenDissipation.lean): merged; eight additional declarations, cumulative 41/41 audit and fresh Linux build PASS. One diagonal generator-square observable with the specified stationary observations identifies squared current and entropy production; the restricted cosmological mode coefficient is invertible for known positive radius and nonzero mode. `BFF.HiddenDissipation.entropy_identified_by_curvature`, `BFF.HiddenDissipation.mode_identifiable`.
- [Cosmology–Chronos, #1392 pinned PR revision](https://github.com/inaciovasquez2020/chronos-urf-rr/blob/2ed7df1497824343fce34924501d42a220c3006f/research/certificates/cosmology_causal_projection/receipt/CausalProjection.lean): Mac 11/11 and dedicated Linux Lean CI PASS; wider integration CI pending at this dated checkpoint. Identical projected coordinates can conceal different causal comparability; strip-area algebra and optimal pointwise decision loss are verified. `Chronos.CosmologyBridge.no_perfect_visible_decoder`, `Chronos.CosmologyBridge.strip_optimal_decoder`.

Only permitted standard Lean axioms were audited. These are mathematical comparisons, not physical equivalence or software dependencies. Full semigroup derivative, covariant action/Fourier derivation, continuum measure formalization, empirical validation, physical 5D detection and independent novelty remain OPEN. No repository-wide status promotion.
