# FOᵏ Diversity → EntropyDepth Growth

## Lemma

Let \(G=(V,E)\) be a bounded-degree graph.

Suppose the number of distinct FOᵏ local types satisfies

\[
T_k(G) \ge \alpha n
\]

for some constant \(\alpha>0\).

Then any FOᵏ-admissible refinement process \(P\) requires

\[
ED(P) = \Omega(n).
\]

---

## Definition — EntropyDepth

For a refinement process \(P\), define

\[
ED(P) = \sum_{t=1}^{T} \Delta H_t
\]

where

\[
\Delta H_t = H(\mathcal{T}_{t}) - H(\mathcal{T}_{t-1})
\]

is the increase in transcript entropy.

---

## Argument

Each refinement step can resolve only \(O(1)\) FOᵏ types due to bounded locality.

If \(T_k(G) = \Omega(n)\), the refinement process must perform

\[
\Omega(n)
\]

steps.

Thus

\[
ED(P) = \Omega(n).
\]

---

## Consequence

\[
\text{FO}^k\text{ Diversity}
\Rightarrow
\text{EntropyDepth Growth}.
\]

---

## Oblivion Atom Chain

\[
\text{COR}
\Rightarrow
\text{CycleRankRigidity}
\Rightarrow
\text{FO}^k\text{ Diversity}
\Rightarrow
\text{EntropyDepth}.
\]

