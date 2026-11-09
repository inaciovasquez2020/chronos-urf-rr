# Candidate finite holonomy / bounded-locality bridge (001–004)

**Status: research note, conditional integration, no theorem-level closure.**

Source-of-truth candidate: `inaciovasquez2020/urf-core`, `experiments/finite_transport_holonomy/`. This is an experimental cross-repository reference, not an imported or verified Chronos theorem.

The exact Python cases cover: gauge-invariant cyclic transport, sharp bounded-error reconstruction, theta-graph redundant loop signatures, and locally gauge-trivial / globally nontrivial cyclic connections. See the URF Core overlay README and four scripts for hypotheses, algorithms, and reproducibility.

### Potential FMT interface

`FMT.Graph.*` (bounded-radius graph neighborhoods) → gauge-equivalence class of a restricted connection → test global holonomy distinguishability.

This provides a *counterexample family to unrestricted local-gauge-data reconstruction* when cycles exceed local observation radius. It does not establish equivalence with the existing `FMT.Types` or `FMT.Game` semantics; a precise translation is an open integration task.

### Existing open obligations

No implication for R1 Long-Chord Exclusion, R2 Diameter-Separation Filling Obstruction, or R3 Uniform Local-Type Capacity follows without verifying their precise carrier, witness, and quotient hypotheses. The new finite information-capacity argument is not a proof of R3.

For fifth-dimensional interpretations, Kaluza–Klein circle-bundle models encode gauge connections geometrically, but the present finite evidence does not distinguish such a model from four-dimensional gauge theory. No physical prediction is made.

`COMPUTATION_PASS` for the standalone Python scripts; `LEAN_VERIFIED := NOT_RUN`; `PHYSICAL_NECESSITY := OPEN`.
