# Cycle–Overlap Rigidity Lemma

## Status

Proposed structural lemma in the Oblivion / Chronos framework.

Goal: establish that **FOᵏ local homogeneity forces bounded cycle-overlap rank**, thereby yielding the contrapositive bridge used in Chronos:

\[
\mathrm{COR}_R(G) \text{ large } \Rightarrow \text{FO}^k_R\text{ local-type diversity}.
\]

This lemma isolates the combinatorial rigidity needed to connect local cycle structure with FOᵏ distinguishability.

---

# 1. Setup

Let \(G=(V,E)\) be a finite graph with maximum degree

\[
\deg(G) \le \Delta.
\]

Fix parameters

\[
k,R \in \mathbb{N}.
\]

For each vertex \(v\in V\), define the radius-\(R\) neighborhood

\[
B_R(v)=\{u\in V : \operatorname{dist}(u,v)\le R\}.
\]

---

# 2. Local Cycle Visibility

Let

\[
Z_1(H)
\]

denote the cycle space of graph \(H\) over \(\mathbb{F}_2\).

Each neighborhood contributes local cycles

\[
Z_1(B_R(v)).
\]

These embed into the global cycle space of \(G\).

---

# 3. Cycle–Overlap Map

Define

\[
\Phi_R :
\bigoplus_{v\in V} Z_1(B_R(v))
\longrightarrow
Z_1(G)
\]

by embedding local cycles into the global graph.

---

## Definition (Cycle–Overlap Rank)

\[
\mathrm{COR}_R(G)
=
\dim_{\mathbb{F}_2}
\operatorname{Im}(\Phi_R).
\]

Interpretation:

- small COR ⇒ global cycles arise from a bounded set of local templates  
- large COR ⇒ many locally visible independent cycles

---

# 4. FOᵏ Local Types

Two rooted graphs \((G,v)\) and \((G,u)\) are **FOᵏ\(_R\)-equivalent** if they satisfy the same first-order formulas

- using at most \(k\) variables
- with quantification restricted to radius \(R\).

Denote

\[
(G,v) \equiv_{FO^k_R} (G,u).
\]

---

## FOᵏ Homogeneity

Graph \(G\) is **FOᵏ\(_R\)-homogeneous** if

\[
(G,u) \equiv_{FO^k_R} (G,v)
\quad
\forall u,v\in V.
\]

Thus all radius-\(R\) neighborhoods are indistinguishable to \(k\)-variable logic.

---

# 5. Finite Type Bound

Because graphs have bounded degree,

\[
|B_R(v)| \le 1+\Delta+\Delta^2+\dots+\Delta^R.
\]

Hence there are finitely many possible rooted radius-\(R\) graphs.

Thus

\[
|\mathrm{Types}_{k,R}| \le N(k,\Delta,R).
\]

---

# 6. Homogeneous Template Ball

Under FOᵏ homogeneity every vertex shares the same type.

Therefore there exists a canonical radius-\(R\) template ball

\[
B^\*
\]

such that every \(B_R(v)\) is FOᵏ-equivalent to \(B^\*\).

---

# 7. Local Cycle Template Space

Let

\[
Z_1(B^\*)
\]

be the cycle space of the template ball.

Dimension bound:

\[
\dim Z_1(B^\*) \le E(B^\*) - V(B^\*) + 1.
\]

Since \(B^\*\) has size bounded by \(\Delta^R\),

\[
\dim Z_1(B^\*) \le C_0(\Delta,R).
\]

---

# 8. Template Embedding Principle

Every local cycle in \(B_R(v)\) corresponds to an embedding of some template cycle in \(B^\*\).

Thus the image of the cycle-overlap map satisfies

\[
\operatorname{Im}(\Phi_R)
\subseteq
\text{span of template cycle embeddings}.
\]

---

# 9. Overlap Compression

Because embeddings of the same template cycle overlap consistently across vertices under FOᵏ homogeneity, they generate only a bounded number of independent global cycles.

Therefore there exists a constant

\[
C(k,\Delta,R)
\]

such that

\[
\mathrm{COR}_R(G) \le C(k,\Delta,R).
\]

---

# 10. Cycle–Overlap Rigidity Lemma

**Lemma.**

For every \(k,\Delta,R\) there exists a constant \(C(k,\Delta,R)\) such that any graph \(G\) with

\[
\deg(G)\le\Delta
\]

and

\[
FO^k_R\text{-homogeneous}
\]

satisfies

\[
\mathrm{COR}_R(G) \le C(k,\Delta,R).
\]

---

# 11. Contrapositive Form

Equivalently,

\[
\mathrm{COR}_R(G) > C(k,\Delta,R)
\]

implies

\[
G \text{ is not } FO^k_R\text{-homogeneous}.
\]

Hence

\[
|\mathrm{Types}_{k,R}(G)| \ge 2.
\]

This yields **FOᵏ local-type diversity**.

---

# 12. Role in the Oblivion Atom

This lemma provides the missing structural step:

\[
\text{Cycle-overlap growth}
\]

\[
\Downarrow
\]

\[
FO^k\text{ local-type diversity}
\]

which forms the combinatorial core of the **Oblivion Atom**.

---

# 13. Connection to Chronos

FOᵏ diversity forces refinement algorithms to distinguish multiple local configurations.

If algorithms are restricted to FOᵏ-local information:

\[
\Delta H_{\text{step}} \le O(1).
\]

With instance entropy

\[
H(X)=\Theta(n),
\]

the refinement depth must satisfy

\[
\mathrm{ED}(F)\ge\Omega(n).
\]

Under patch-rank amplification this strengthens to

\[
\mathrm{ED}(F)\ge\Omega(n\log n).
\]

---

# 14. Resulting Chronos Chain

\[
\text{Cycle-overlap rank growth}
\]

\[
\Downarrow
\]

\[
FO^k\text{ local-type diversity}
\]

\[
\Downarrow
\]

\[
\text{Configuration pumping}
\]

\[
\Downarrow
\]

\[
\text{bounded information per refinement}
\]

\[
\Downarrow
\]

\[
\boxed{\mathrm{ED}(F)\ge\Omega(n)}
\]

which is the entropy barrier underlying the Chronos framework.

---

# 15. Remaining Technical Work

To fully formalize this lemma:

1. Prove the template embedding bound explicitly.
2. Bound the dimension of the cycle-overlap image under homogeneity.
3. Construct explicit graph families with

\[
\mathrm{COR}_R(G)=\Omega(n).
\]

These steps complete the Oblivion Atom → Chronos bridge.
