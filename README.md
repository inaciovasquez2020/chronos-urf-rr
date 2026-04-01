# chronos-urf-rr

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18842937.svg)](https://doi.org/10.5281/zenodo.18842937)

This repository is a **frozen reference realization** of the Chronos / EntropyDepth framework within the Unified Rigidity Framework (URF).

## Purpose
- Provide a stable, executable reference implementation for Chronos relative rigidity.
- Support verification, reproducibility, and citation of Chronos artifacts.
- Serve as a non-normative reference module indexed by the Vasquez Index.

## Scope
- Deterministic verification scaffolds (tests, scripts, proof-check hooks).
- Reproducible execution under declared constraints.
- Verifier-checkable certification artifacts (schemas and signed examples).

## Non-scope
- No new axioms, theorems, or proof claims.
  - Status: conditional
- No claim that passing tests implies truth beyond stated invariants.
- No resolution of open complexity problems.

## Frozen status
The following are frozen:
- Mathematical scope and claims.
- Interfaces and artifact formats.
- Released certification artifacts (immutable once published).

## Reference status
This repository is a **reference implementation**:
executable, audit-ready, and non-normative.

Canonical specifications:
- https://github.com/inaciovasquez2020/Chronos-EntropyDepth
- https://github.com/inaciovasquez2020/urf-core

## GxD (Global × Detectability)

Quantitative key-to-keyhole invariant measuring exponential detectability
of global expansion through bounded observers.

See:
- toolkit/gxd/GxD_Canonical_Module.md
- toolkit/gxd/GxD_Chronos_Bridge.md
- models/gxd_f2/

Referee classification and review guidance are provided in:
- docs/referee/REFEREE_MAP.md

## Subcomponents

- `cslib-fmt` — finite-model-theoretic formalization slice of URF:
  https://github.com/inaciovasquez2020/cslib-fmt

## URF Claim Status

See `URF_STATUS.md` for the canonical classification of formalized, conditional, and open layers.

