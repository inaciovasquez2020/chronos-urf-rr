# Candidate finite holonomy / bounded-locality bridge (001–004)

**Status: research note, conditional integration, no theorem-level closure.**

Source-of-truth candidate: `inaciovasquez2020/urf-core` PR #590, source files `experiments/finite_transport_holonomy/urf_{finite_transport,holonomy_noise,multicycle,local_global}_bridge_00{1,2,3,4}.py` (see explicit paths below). The original `COMPUTATION_PASS` observations belonged to URF Core commit `a8a20ad91aae60e5843ea5c2e7f80718b5e3edd2`; corrected PR revisions require fresh validation. This is an experimental cross-repository reference, not an imported or verified Chronos theorem.

The exact Python cases cover: gauge-invariant cyclic transport, sharp bounded-error reconstruction, theta-graph redundant loop signatures, and locally gauge-trivial / globally nontrivial cyclic connections. See the URF Core overlay README and four scripts for hypotheses, algorithms, and reproducibility.

### Potential FMT interface

`FMT.Graph.*` (bounded-radius graph neighborhoods) → gauge-equivalence class of a restricted connection → test global holonomy distinguishability.

For cycle graph C_n with n > 2r+1, every **induced graph-distance radius-r ball** is a proper path. The counterexample applies ONLY when an observer receives each ball's restricted edge transport **independently quotiented by vertex gauge transformations**, with no coordinated gauge on overlaps. These observations cannot distinguish globally different cycle holonomies. For reconstruction from ball-restricted edge labels, require r >= 1 so the union of observed balls covers every cycle edge; when r = 0, all balls are isolated vertices and even shared-gauge observations reveal no edge transports. With r >= 1 and raw edge labels in a common gauge, or sufficiently compatible overlap/transition data preserving edge transport, the cycle holonomy can be reconstructed; the counterexample does NOT obstruct such stronger observation models. It does not establish equivalence with the existing `FMT.Types` or `FMT.Game` semantics; a precise translation is an open integration task.

### Existing open obligations

No implication for R1 Long-Chord Exclusion, R2 Diameter-Separation Filling Obstruction, or R3 Uniform Local-Type Capacity follows without verifying their precise carrier, witness, and quotient hypotheses. The new finite information-capacity argument is not a proof of R3.

For fifth-dimensional interpretations, Kaluza–Klein circle-bundle models encode gauge connections geometrically, but the present finite evidence does not distinguish such a model from four-dimensional gauge theory. No physical prediction is made.

`COMPUTATION_PASS` for the original pinned standalone Python scripts, not automatic for corrected revisions; `LEAN_VERIFIED := NOT_RUN`; `PHYSICAL_NECESSITY := OPEN`.

### Explicit research sources (URF Core PR #590)

- `experiments/finite_transport_holonomy/urf_finite_transport_bridge_001.py`
- `experiments/finite_transport_holonomy/urf_holonomy_noise_bridge_002.py`
- `experiments/finite_transport_holonomy/urf_multicycle_bridge_003.py`
- `experiments/finite_transport_holonomy/urf_local_global_bridge_004.py`

No cross-repository theorem import has been constructed.
