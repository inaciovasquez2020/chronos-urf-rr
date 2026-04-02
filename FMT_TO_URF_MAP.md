# FMT to URF Map

This file records the intended commutative map from `FMT` modules to URF claims.

## Module-to-claim correspondence

- `FMT.Types.*`
  - URF claim layer: local state/type abstraction
  - Meaning: local configurations are represented at the finite-model-theoretic level before any global rigidity conclusion

- `FMT.Game.*`
  - URF claim layer: locality indistinguishability proxy
  - Meaning: EF/WL-style indistinguishability infrastructure for bounded-radius reasoning

- `FMT.Graph.*`
  - URF claim layer: bounded-radius locality substrate
  - Meaning: graph/distance layer supporting local neighborhoods and separation structure

- `FMT.Bridge.LocalGlobal`
  - URF claim layer: local-to-global transport interface
  - Meaning: bridge schema from local formal structure to global rigidity statements

- `FMT.Invariants.*`
  - URF claim layer: obstruction / nonfactorization layer
  - Meaning: identifies when invariants fail to collapse through local types

- `FMT.Spec.*`
  - URF claim layer: formal target statement layer
  - Meaning: specification boundary for the current FMT slice

- `FMT.API.*`
  - URF claim layer: stable exported interface
  - Meaning: controlled presentation boundary of the formalized FMT slice

- `FMT.Examples.*`
  - URF claim layer: semantic regression / sanity verification
  - Meaning: minimal concrete verification surface for the FMT slice

## Commutativity principle

The intended URF flow is:

`FMT local types / games / graphs`
→ `FMT invariants and nonfactorization`
→ `local-to-global bridge interface`
→ `Chronos / EntropyDepth integration layer`

The first three stages are repository-level represented.
The final transport into the next URF layer remains conditional unless explicitly proved in a canonical note or formalized theorem.
