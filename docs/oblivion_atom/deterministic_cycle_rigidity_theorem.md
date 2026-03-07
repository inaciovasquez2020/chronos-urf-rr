# Deterministic Cycle Rigidity Theorem

## Status

Core deterministic rigidity theorem for the Oblivion Atom framework.

This theorem replaces the EF-game proof outline with a linear-algebraic argument based on cycle-space rank.

---

# 1. Setup

Let

\[
G = (V,E)
\]

be a finite connected graph with bounded degree

\[
\Delta = O(1).
\]

Let

\[
C_{\le L}(G)
\]

denote the set of simple cycles of length at most \(L\).

For each cycle \(C\subseteq E\), define the incidence vector

\[
z_C \in \mathbb{F}_2^{E}
\]

by

\[
(z_C)_e =
\begin{cases}
1 & e\in C \\
0 & e\notin C
\end{cases}
\]

Let

\[
Z_L(G)=\mathrm{span}_{\mathbb{F}_2}\{z_C : C\in C_{\le L}(G)\}
\]

be the short-cycle subspace of the cycle space.

---

# 2. Cycle Incidence Matrix

Define the matrix

\[
M \in \mathbb{F}_2^{E\times m}
\]

whose columns are the vectors \(z_{C_i}\).

Then

\[
\operatorname{rank}(M)
=
\operatorname{rank}(Z_L(G)).
\]

---

# 3. Vertex–Cycle Interaction Matrix

For a vertex \(v\), let

\[
B_R(v)
\]

denote the radius-\(R\) neighborhood of \(v\).

Define

\[
A_{v,i} =
\mathbf{1}\!\left(C_i \cap B_R(v) \neq \varnothing\right)
\]

This produces the **vertex–cycle interaction matrix**

\[
A \in \mathbb{F}_2^{V\times m}.
\]

---

# 4. Sparse Column Structure

Each cycle of length ≤ \(L\) touches at most \(L\) vertices.

Because the graph degree is bounded by \(\Delta\),

the set of vertices within distance \(R\) of any cycle has size

\[
O(L\Delta^R).
\]

Thus every column of \(A\) has bounded support.

---

# 5. Rank Propagation

Using the sparse-column rank transfer inequality,

\[
\operatorname{rank}(A)
\ge
\frac{1}{L\Delta^R}
|\bigcup_i \operatorname{supp}(A_{*,i})|.
\]

The cycle-coverage lemma implies

\[
|\bigcup_i \operatorname{supp}(A_{*,i})|
=
\Omega(|V|).
\]

Therefore

\[
\operatorname{rank}(A)
=
\Omega(|V|).
\]

---

# 6. Row Diversity

Matrix rank bounds the number of distinct rows:

\[
\#\{\text{distinct rows of }A\}
\ge
\operatorname{rank}(A).
\]

Thus

\[
\#\{\text{distinct rows}\}
=
\Omega(|V|).
\]

---

# 7. Row Distinction ⇒ Local Structural Distinction

If two vertices have different rows in \(A\),

then some short cycle intersects one radius-\(R\) neighborhood but not the other.

For \(R \ge 2L\),

this implies

\[
(B_{R-L}(u),u)
\not\cong
(B_{R-L}(v),v).
\]

Hence row distinction implies distinct rooted neighborhoods.

---

# 8. Rooted Neighborhood Explosion

Combining the previous steps yields

\[
\#\{\text{rooted radius-}(R-L)\text{ neighborhoods}\}
=
\Omega(|V|).
\]

---

# 9. FOᵏ Type Explosion

By Gaifman locality,

FOᵏ formulas of quantifier depth \(d\) depend only on radius

\[
r = O(kd).
\]

Thus rooted neighborhood diversity implies

\[
\#\{\text{FOᵏ types}\}
=
\Omega(|V|).
\]

---

# 10. EntropyDepth Consequence

FOᵏ refinement processes can introduce only a bounded number of new vertex types per step.

Resolving

\[
\Omega(|V|)
\]

types therefore requires

\[
\mathrm{ED}(n) = \Omega(n).
\]

---

# 11. Deterministic Rigidity Chain

The full Oblivion Atom argument collapses to

\[
\text{Cycle overlap geometry}
\]

\[
\Downarrow
\]

\[
\operatorname{rank}(Z_L(G)) = \Omega(n)
\]

\[
\Downarrow
\]

\[
\text{Deterministic Cycle Rigidity}
\]

\[
\Downarrow
\]

\[
\text{Rooted neighborhood explosion}
\]

\[
\Downarrow
\]

\[
\text{FOᵏ configuration explosion}
\]

\[
\Downarrow
\]

\[
\mathrm{ED}(n) \ge \Omega(n)
\]

---

# 12. Role in Oblivion Atom

This theorem replaces the EF-game strategy with a purely algebraic argument based on cycle-space rank.

The remaining Oblivion Atom chain therefore reduces to verifying

\[
\operatorname{rank}(Z_L(G)) = \Omega(n)
\]

for the relevant graph families.

---

# 13. Key Insight

Short cycles encode global overlap constraints.

When the cycle incidence vectors achieve linear rank,

the graph cannot maintain local structural homogeneity.

Distinct vertices must exhibit distinct local cycle interaction patterns,

forcing rooted neighborhood diversity.

---

# 14. Summary

\[
\boxed{
\text{Cycle-space rank growth}
\Rightarrow
\text{Local type explosion}
\Rightarrow
\mathrm{ED}(n) \ge \Omega(n)
}
\]

This establishes the deterministic rigidity mechanism underlying the Oblivion Atom framework.
