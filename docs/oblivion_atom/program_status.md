# Oblivion Atom Program Status

## Deterministic Cycle Regime

Completed structural chain:

\[
\text{CycleOverlap}
\Rightarrow
\text{CycleRankRigidity}
\Rightarrow
\text{FO}^k\text{ Diversity}
\Rightarrow
\text{EntropyDepth}.
\]

Key result:

\[
\operatorname{rank}(B) \ge \frac{m}{K(L-1)+1}.
\]

Thus

\[
\operatorname{rank}(B)=\Omega(m).
\]

---

## Consequence

Cycle-dense bounded-degree graphs force

- linear cycle signature rank
- FOᵏ local type explosion
- linear EntropyDepth.

This establishes a **deterministic rigidity regime**.

---

## Remaining Regimes

Two additional structural regimes remain:

### 1. Hypergraph Gadget Rigidity

Constraint gadgets interacting through bounded overlaps.

Goal:

\[
\text{GadgetOverlap}
\Rightarrow
\text{FO}^k\text{ Diversity}.
\]

### 2. Random Expansion Regime

Random lifts and expanders where cycles are long but numerous.

Goal:

prove FOᵏ-type collisions decay exponentially.

---

## Target Closure

Combine regimes to obtain the universal obstruction:

\[
\text{Oblivion Atom}.
\]

This yields

\[
\text{EntropyDepth} = \Omega(n)
\]

for all FOᵏ-admissible refinement processes on hard instances.

---

## Current Status

Cycle regime: solved.

Hypergraph regime: open lemma.

Random expansion regime: partially established experimentally.

