# Cycle Rank → FOᵏ Type Diversity

## Lemma

Let \(G=(V,E)\) be a bounded-degree graph and  
let \(C_1,\dots,C_m\) be simple cycles with bounded length and bounded edge multiplicity.

Let

\[
B \in \mathbb{F}_2^{E\times m}
\]

be the cycle–edge incidence matrix.

If

\[
\operatorname{rank}(B)=\Omega(m)
\]

then there exist \(\Omega(m)\) distinct **cycle signatures** in local neighborhoods of \(G\).

---

## Definition — Cycle Signature

For a vertex \(v\), define the cycle signature vector

\[
\sigma(v) \in \mathbb{F}_2^m
\]

where

\[
\sigma(v)_i =
\begin{cases}
1 & v \text{ lies on } C_i \\
0 & \text{otherwise}
\end{cases}
\]

---

## Claim

Distinct independent cycle columns induce distinct vertex signatures.

Thus the number of distinct vertex signatures grows linearly with the number of independent cycles.

---

## FOᵏ Consequence

Vertices with different cycle signatures are distinguishable by FOᵏ formulas using bounded-radius neighborhoods.

Therefore

\[
\text{CycleRankRigidity}
\Rightarrow
\text{FO}^k\text{ Type Diversity}.
\]

---

## Position in Oblivion Chain

\[
\text{COR}
\Rightarrow
\text{CycleRankRigidity}
\Rightarrow
\text{FO}^k\text{ Diversity}
\Rightarrow
\text{EntropyDepth}.
\]

