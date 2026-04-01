# URF Status

This document classifies the current layers of the Unified Rigidity Framework.

## Formalized

- `cslib-fmt` finite-model-theoretic slice
  - Status: formalized
  - Scope: local types, factorization/nonfactorization interface, local/global bridge scaffolding, semantic examples, API/spec layer

## Conditional

- Chronos / EntropyDepth interface layer
  - Status: conditional
  - Reason: repository-level interface exists, but full theorem-to-theorem integration from the FMT slice into the next URF layer is not yet fully formalized here

- Program-level lower-bound synthesis
  - Status: conditional
  - Reason: depends on cross-layer integration and theorem transport beyond the current formalized FMT slice

## Open

- Full URF canonical integration across all layers
  - Status: open

- Full external theorem validation and referee uptake
  - Status: open

- Any non-formalized global claim not explicitly represented as a proved theorem in the repositories
  - Status: open

## Repository map

- `cslib-fmt`
  - Role: finite-model-theoretic formalization slice

- `chronos-urf-rr`
  - Role: meta-repo / integration spine

## Policy

Any theorem, reduction, or global implication not formalized in code or explicitly proved in a canonical manuscript integrated here must be treated as conditional or open.
