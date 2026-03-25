# Local Cycle Span Bound

## Status

Structural lemma candidate in the Oblivion → Chronos bridge.

Purpose: bound the dimension of the span of all **s-local cycles** in an FOᵏ-homogeneous bounded-degree graph.

Target result:

\[
FO^k_R\text{-homogeneous}
\;\Rightarrow\;
\dim \operatorname{span}\{\text{s-local cycles}\} \le C(k,\Delta,R)
\]

which implies

\[
\mathrm{COR}_R(G) \le C(k,\Delta,R).
\]

---

# 1. Graph Model

Let

\[
G=(V,E)
\]

be a finite graph with maximum degree

\[
\deg(G)\le\Delta.
\]

Fix parameters

\[
k,R\in\mathbb N.
\]

Define the radius-\(R\) ball

\[
B_R(v)=\{u\in V:\operatorname{dist}(u,v)\le R\}.
\]

---

# 2. Cycle Space

Let

\[
Z_1(G)
\]

denote the cycle space over

\[
\mathbb F_2.
\]

Dimension:

\[
\beta_1(G)=|E|-|V|+c
\]

where \(c\) is the number of connected components.

---

# 3. Local Cycles

A cycle \(C\subseteq G\) is **s-local** if its support lies inside a ball

\[
C \subseteq B_R(v)
\]

for some vertex \(v\).

The support size satisfies

\[
|C|\le s
\]

with

\[
s=O(\Delta^R).
\]

---

# 4. Local Cycle Span

Define the span of all s-local cycles:

\[
\mathcal L_s(G)
=
\operatorname{span}\{C : C\subseteq B_R(v)\text{ for some }v\}.
\]

This space contains all cycles locally visible in radius \(R\).

Observe

\[
\mathcal L_s(G)
=
\operatorname{Im}(\Phi_R)
\]

from the cycle-overlap map.

Thus

\[
\dim \mathcal L_s(G)
=
\mathrm{COR}_R(G).
\]

---

# 5. FOᵏ Homogeneity

Graph \(G\) is FOᵏ\(_R\)-homogeneous if

\[
(G,u)\equiv_{FO^k_R}(G,v)
\quad
\forall u,v\in V.
\]

Hence all radius-\(R\) balls share the same logical structure.

Denote the template ball

\[
B^\*.
\]

---

# 6. Template Cycle Set

Let

\[
Z_1(B^\*)
\]

be the cycle space of the template ball.

Dimension bound:

\[
\dim Z_1(B^\*)\le C_0(\Delta,R).
\]

Each local cycle in \(G\) corresponds to an embedding of a cycle from this finite template set.

---

# 7. Embedding Multiplicity

For each template cycle \(C^\*\subseteq B^\*\) and each vertex \(v\), there exists an embedding

\[
\iota_v(C^\*)
\subseteq G.
\]

These cycles overlap heavily because neighboring balls intersect.

Thus embeddings of the same template cycle generate linear dependencies in

\[
Z_1(G).
\]

---

# 8. Overlap-Induced Dependencies

Let

\[
C_1,\dots,C_m
\]

be embeddings of the same template cycle.

Because balls intersect along regions of size

\[
O(\Delta^{R-1}),
\]

symmetric differences between overlapping embeddings produce shorter cycles or cancellations.

Thus large families of embeddings cannot remain linearly independent.

---

# 9. Bounded Dimension Claim

There exists a constant

\[
C(k,\Delta,R)
\]

such that

\[
\dim \mathcal L_s(G) \le C(k,\Delta,R).
\]

Reason:

1. the number of template cycles is bounded
2. embeddings overlap in bounded regions
3. linear dependencies arise from overlaps

Hence the span of all s-local cycles is bounded.

---

# 10. Consequence for Cycle-Overlap Rank

Since

\[
\mathrm{COR}_R(G)=\dim \mathcal L_s(G),
\]

we obtain

\[
FO^k_R\text{-homogeneous}
\Rightarrow
\mathrm{COR}_R(G)\le C(k,\Delta,R).
\]

---

# 11. Contrapositive

If

\[
\mathrm{COR}_R(G) > C(k,\Delta,R)
\]

then \(G\) cannot be FOᵏ\(_R\)-homogeneous.

Therefore

\[
|\mathrm{Types}_{k,R}(G)|\ge2.
\]

This yields **FOᵏ local-type diversity**.

---

# 12. Role in the Oblivion Atom

This lemma completes the structural step

cycle-overlap growth
↓
FOᵏ local-type diversity


which is the combinatorial core of the Oblivion framework.

---

# 13. Connection to Chronos

FOᵏ diversity forces refinement algorithms to distinguish many local configurations.

If each refinement step uses FOᵏ-local information, the information gain per step is bounded.

Hence

\[
\mathrm{ED}(F)\ge\Omega(n).
\]

Under patch-rank amplification:

\[
\mathrm{ED}(F)\ge\Omega(n\log n).
\]

---

# 14. Remaining Technical Steps

To convert this strategy into a full proof:

1. Formalize the overlap-dependency argument.
2. Prove a universal bound on independent embeddings.
3. Construct explicit graph families with

\[
\mathrm{COR}_R(G)=\Omega(n).
\]

These steps close the Oblivion → Chronos bridge.
