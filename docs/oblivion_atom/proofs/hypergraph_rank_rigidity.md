# Hypergraph Rank Rigidity Lemma

## Statement

Let \(H=(V,\mathcal E)\) be a finite hypergraph with hyperedges
\[
\mathcal E = \{E_1,\dots,E_m\}.
\]

Assume:

1. **Bounded hyperedge size**
\[
|E_i|\le K
\qquad (1\le i\le m)
\]

2. **Bounded vertex participation**
\[
\deg_H(v)\le L
\qquad (v\in V)
\]

Define the vertex–hyperedge incidence matrix
\[
B_H \in \mathbb F_2^{V\times m},
\qquad
(B_H)_{v,i}=1 \iff v\in E_i.
\]

Then
\[
\operatorname{rank}_{\mathbb F_2}(B_H)\ge \frac{m}{K(L-1)+1}.
\]

In particular,
\[
\operatorname{rank}_{\mathbb F_2}(B_H)=\Omega(m).
\]

---

## Proof

Define the intersection graph \(\Gamma_H\) on vertex set \([m]=\{1,\dots,m\}\) by
\[
i\sim j \iff i\neq j \text{ and } E_i\cap E_j\neq \varnothing.
\]

Fix \(i\). Since \(E_i\) has at most \(K\) vertices and each vertex belongs to at most \(L\) hyperedges total, each vertex of \(E_i\) contributes at most \(L-1\) neighboring hyperedges distinct from \(E_i\). Therefore
\[
\deg_{\Gamma_H}(i)\le K(L-1).
\]

Hence
\[
\Delta(\Gamma_H)\le K(L-1).
\]

Let \(S\subseteq [m]\) be a maximal independent set in \(\Gamma_H\). By the standard greedy bound,
\[
|S|\ge \frac{m}{\Delta(\Gamma_H)+1}\ge \frac{m}{K(L-1)+1}.
\]

Independence of \(S\) means that the hyperedges \(\{E_i:i\in S\}\) are pairwise disjoint.

Now consider the corresponding columns of \(B_H\). Their supports are pairwise disjoint and each support is nonempty unless \(E_i=\varnothing\). For nonempty hyperedges, disjoint-support columns are linearly independent over \(\mathbb F_2\). Indeed, if
\[
\sum_{i\in S'} \mathbf 1_{E_i}=0
\]
for some nonempty \(S'\subseteq S\), choose \(i_0\in S'\) and \(v\in E_{i_0}\). Since the supports are pairwise disjoint, the \(v\)-coordinate of the sum equals \(1\), contradiction.

Therefore the columns indexed by \(S\) are linearly independent, so
\[
\operatorname{rank}_{\mathbb F_2}(B_H)\ge |S|
\ge \frac{m}{K(L-1)+1}.
\]

Thus
\[
\boxed{
\operatorname{rank}_{\mathbb F_2}(B_H)\ge \frac{m}{K(L-1)+1}
}
\]
and in particular
\[
\boxed{
\operatorname{rank}_{\mathbb F_2}(B_H)=\Omega(m).
}
\]

---

## Consequence

Bounded-overlap gadget systems force linear incidence-rank growth.

Thus
\[
\text{HyperedgeOverlap}
\Rightarrow
\text{RankGrowth}.
\]

Combined with the cycle case, this yields a unified bounded-overlap rigidity principle.

