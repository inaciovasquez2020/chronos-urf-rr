# Cyclone Lemma Status Update

## Previous Issue

The original Cyclone Core Lemma relied on **per-vertex FOᵏ type equality**

tp^{k,R}(v)

which is insufficient to bound the size of symmetric-difference components.

Counterexamples exist in highly symmetric bounded-degree graphs.

---

## Correction

Replace the hypothesis with **pair-type equality**

tp^{k,R}(v,w)

for every edge (v,w).

This stronger locality condition controls the interaction of cycle predicates along edges.

---

## Result

Under the pair-type hypothesis:

Every component H of D = C₁ ⊕ C₂ satisfies

|E(H)| ≤ L(k,Δ,R)

with

L(k,Δ,R) = T(k,Δ,r)².

---

## Program Impact

This modification preserves the rigidity program structure while fixing the false per-vertex assumption.

Affected components:

- Cycle Local Rigidity proof
- Cyclone reduction step
- COR rank bounds
- Oblivion Atom dependency graph

The corrected lemma restores the bounded-component property needed for the rigidity pipeline.
