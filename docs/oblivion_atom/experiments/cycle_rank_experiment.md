# Cycle–Rank Rigidity Experiment

## Goal

Empirically verify that the cycle–edge incidence matrix rank grows linearly with the number of sampled cycles.

\[
\operatorname{rank}(B) = \Omega(m)
\]

where

- \(B\) is the cycle–edge incidence matrix
- \(m\) is the number of cycles.

---

## Method

1. Generate a random \(d\)-regular graph.
2. Extract simple cycles using `networkx.cycle_basis`.
3. Construct the cycle–edge incidence matrix \(B\).
4. Compute rank over \(\mathbb{F}_2\) using Gaussian elimination.

---

## Script

toolkit/oblivion/experiments/cycle_rank_test.py

---

## Expected Observation

For bounded-degree graphs:

\[
\frac{\operatorname{rank}(B)}{m} \to c > 0
\]

consistent with the theoretical bound

\[
\operatorname{rank}(B) \ge \frac{m}{K(L-1)+1}.
\]

---

## Role in Oblivion Atom

This experiment validates the structural claim:

\[
\text{CycleOverlap} \Rightarrow
\text{CycleRankRigidity}.
\]

which feeds the chain

\[
\text{COR}
\Rightarrow
\text{FO}^k\text{ Diversity}
\Rightarrow
\text{EntropyDepth}.
\]

