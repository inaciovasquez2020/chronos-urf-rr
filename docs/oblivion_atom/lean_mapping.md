# Lean Mapping for Oblivion Atom Chain

## Purpose

Map the mathematical reduction chain to the Lean formalization modules.

---

## Chain

CycleOverlap → CycleRankRigidity → FOᵏ Diversity → EntropyDepth

---

## Lean Modules

### Cycle Rank Rigidity
lean/Oblivion/Rigidity/CycleRankRigidity.lean

Formal target:

rank(B) ≥ m / (K(L-1)+1)

---

### Rank → FOᵏ Diversity
lean/Oblivion/Rigidity/CycleRankToFok.lean

Bridge lemma connecting structural rank growth to local type diversity.

---

### FOᵏ → EntropyDepth
lean/Oblivion/Rigidity/FokToEntropyDepth.lean

Formalization target:

FOᵏ type explosion ⇒ linear refinement depth.

---

### EntropyDepth Wall
lean/Oblivion/Rigidity/EntropyDepthWall.lean

Final rigidity statement.

---

### Reduction Chain
lean/Oblivion/Rigidity/Chain.lean

Formal composition of the four lemmas.

---

## Status

Cycle regime documentation: complete

Lean skeletons: created

Formal proofs: pending

