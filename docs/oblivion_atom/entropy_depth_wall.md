# EntropyDepth Wall (Cycle Regime)

## Theorem

Let \(G=(V,E)\) be a bounded-degree graph in the **Cycle Overlap Regime (COR)**:

- number of short cycles \(m = \Theta(n)\)
- cycle length bounded \( |C_i| \le K \)
- edge participation bounded \( \le L \)

Then any FOᵏ-admissible refinement process \(P\) satisfies

\[
ED(P) = \Omega(n).
\]

---

## Reduction Chain

\[
\text{CycleOverlap}
\Rightarrow
\text{CycleRankRigidity}
\Rightarrow
\text{FO}^k\text{ Diversity}
\Rightarrow
\text{EntropyDepth}.
\]

---

## Interpretation

Local refinement algorithms cannot compress structural information
in graphs with dense cycle overlap.

Each refinement step resolves only constant information,
forcing linear transcript growth.

---

## Chronos Consequence

Under transcript capacity bounds:

\[
T \ge \frac{H}{TC}
\]

linear EntropyDepth implies

\[
T = \Omega(n).
\]

Thus COR graphs lie on the **EntropyDepth Wall**.

---

## Role in the Chronos Program

This provides a deterministic structural regime where

local refinement cannot achieve sublinear inference depth.

