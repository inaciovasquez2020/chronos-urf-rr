# Cycle–Rank Rigidity Lemma

## Statement

Let \(G=(V,E)\) be a bounded-degree graph.  
Let \(C_1,\dots,C_m\) be simple cycles.

Define the cycle–edge incidence matrix
\[
B \in \mathbb{F}_2^{E\times m},\qquad
B_{e,i}=1 \iff e\in C_i.
\]

Assume:

1. \(|C_i|\le K\)
2. Each edge lies in at most \(L\) cycles

Then

\[
\operatorname{rank}_{\mathbb F_2}(B)\ge \frac{m}{K(L-1)+1}
\]

In particular

\[
\operatorname{rank}_{\mathbb F_2}(B)=\Omega(m).
\]

---

## Proof

Define the intersection graph \(\Gamma\) on vertices \(\{1,\dots,m\}\):

\[
i\sim j \iff C_i\cap C_j\neq\varnothing
\]

Each cycle \(C_i\) has at most \(K\) edges.  
Each edge belongs to at most \(L\) cycles.

Thus

\[
\deg_\Gamma(i)\le K(L-1)
\]

Let \(S\) be a maximal independent set in \(\Gamma\).  
Standard bounds give

\[
|S|\ge \frac{m}{K(L-1)+1}.
\]

Independence implies cycles in \(S\) are edge-disjoint.

The corresponding columns of \(B\) therefore have disjoint support and are linearly independent over \(\mathbb F_2\).

Hence

\[
\operatorname{rank}(B)\ge |S|\ge \frac{m}{K(L-1)+1}.
\]

\[
\boxed{\operatorname{rank}(B)=\Omega(m)}
\]

---

## Role in Oblivion Atom

Cycle overlap density forces linear growth of cycle incidence rank.

This yields:

\[
\text{CycleOverlap} \Rightarrow \text{FO}^k\text{-type diversity} \Rightarrow \text{EntropyDepth growth}.
\]
