# Hypergraph Rank → FOᵏ Type Diversity

## Lemma

Let \(H=(V,\mathcal E)\) be a bounded-overlap hypergraph and let

\[
B_H \in \mathbb F_2^{V\times m}
\]

be its vertex–hyperedge incidence matrix.

If

\[
\operatorname{rank}(B_H)=\Omega(m),
\]

then the system exhibits \(\Omega(m)\) independent local gadget signatures.

---

## Definition — Gadget Signature

For a vertex \(v\in V\), define the gadget signature

\[
\sigma_H(v)\in \mathbb F_2^m
\]

by

\[
\sigma_H(v)_i =
\begin{cases}
1 & v\in E_i,\\
0 & v\notin E_i.
\end{cases}
\]

---

## Claim

Independent hyperedge columns induce linearly many independent local signatures.

Under bounded degree and bounded gadget radius, distinct local signatures induce distinct FOᵏ local types.

Therefore

\[
\text{HypergraphRankRigidity}
\Rightarrow
\text{FO}^k\text{ Diversity}.
\]

---

## Consequence

Combining with the rank lemma:

\[
\text{HyperedgeOverlap}
\Rightarrow
\text{RankGrowth}
\Rightarrow
\text{FO}^k\text{ Diversity}.
\]

This is the gadget-side analogue of the deterministic cycle regime.

