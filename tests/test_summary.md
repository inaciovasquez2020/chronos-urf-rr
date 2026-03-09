# URF Lean Verification Test Suite

Modules tested:

- Oblivion/Cycle/CycleIncidenceMatrix.lean
- Oblivion/Cycle/CyclePackingBound.lean
- Oblivion/Cycle/LocalCycleWitness.lean
- FOk/Cycle/CycleDefinability.lean
- Chronos/EntropyDepthClosure.lean

Test coverage:

1. F₂ cycle incidence matrix construction
2. Cycle packing bound via rank
3. Local cycle witness lemma
4. FO^k cycle definability skeleton
5. Chronos entropy depth bound

Execution:

bash tests/run_all_lean_tests.sh
