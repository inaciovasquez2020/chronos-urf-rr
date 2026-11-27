# STATUS — chronos-urf-rr

## Repository role
chronos-urf-rr is a **internally frozen reference realization** of the Chronos / EntropyDepth framework within the Unified Rigidity Framework (URF).

It exists to provide an executable, audit-ready reference for verification, reproducibility, and citation.

## Scope (what this repository does)
- Provides deterministic verification scaffolds.
- Produces verifier-checkable certification artifacts.
- Supports reproducible execution under declared constraints.

## Non-scope (explicit non-claims)
- No new axioms or theorems are introduced here.
  - Status: conditional
- No claim that verification implies mathematical truth beyond stated invariants.
- No resolution of open complexity or foundational problems.

## Internally internally frozen components
The following are internally frozen and treated as immutable once released:
- Mathematical scope and claims.
- Public interfaces and artifact formats.
- Released certification artifacts.

## Normativity
This repository is **non-normative**.
It is executable and citable, but does not define standards or prescribe usage beyond verification.

## Review guidance
Formal classification of results, assumptions, and non-claims is provided in:
- docs/referee/REFEREE_MAP.md

## Status

Stable. Audit-ready. Conditional at theorem layer. No theorem-level closure beyond (R1), (R2), (R3) without new mathematical input.

## Four-event Minkowski probability — 2026-11-27 UTC

[Mac-verified checkpoint (draft PR #1398, pinned revision)](https://github.com/inaciovasquez2020/chronos-urf-rr/blob/e6945b6946f500f917c8b427df411a0e796851b7/research/certificates/p42_physical_checkpoint_20261127/README.md): four IID uniform events in a unit Alexandrov interval in 3+1-dimensional Minkowski spacetime. The candidate probability that the first two elements of a uniformly selected linear extension are comparable is `p42 = 32*pi^2/7 - 13239637/294000`.

- LEAN_VERIFIED: physical common-future geometry, joint radial/angular/rapidity measure and explicit spacelike integral reduction. The [final eight-declaration axiom receipt](https://github.com/inaciovasquez2020/chronos-urf-rr/blob/e6945b6946f500f917c8b427df411a0e796851b7/research/certificates/p42_physical_checkpoint_20261127/verified/tmp.vmCoPZ4Zsi/LEAN.log) lists only propext, Classical.choice and Quot.sound.
- COMPUTATION_PASS: [exact arithmetic and finite-poset objective identity](https://github.com/inaciovasquez2020/chronos-urf-rr/blob/e6945b6946f500f917c8b427df411a0e796851b7/research/certificates/p42_physical_checkpoint_20261127/verified/tmp.qlXqdaOReV/COMPUTATION.log); 729 candidates, 219 labeled partial orders, 16 isomorphism classes.
- OPEN: full analytic evaluation in Lean, complete probability theorem and independent review/novelty. Fresh rebuild NOT_RUN. Research checkpoint is a pinned draft PR at the dated record, not a merge or global physical-closure claim.
