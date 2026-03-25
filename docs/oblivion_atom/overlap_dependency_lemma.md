# Overlap Dependency Lemma

## Status

Technical lemma supporting the **Local Cycle Span Bound** and the **Cycle–Overlap Rigidity Lemma** in the Oblivion → Chronos bridge.

Goal: prove that large families of embedded local cycles cannot remain linearly independent because bounded-radius neighborhoods necessarily overlap.

Target statement:

\[
\text{FO}^k_R\text{-homogeneous}
\;\Rightarrow\;
\dim \operatorname{span}\{\text{s-local cycles}\}
\le C(k,\Delta,R).
\]

The key mechanism is **overlap-induced linear dependence**.

---

# 1. Graph Model

Let

\[
G=(V,E)
\]

be a finite graph with maximum degree

\[
\deg(G)\le \Delta.
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

# 2. Template Ball

Assume

\[
G \text{ is } FO^k_R\text{-homogeneous}.
\]

Thus every vertex has the same logical neighborhood type.

Denote the canonical template ball

\[
B^\*.
\]

Every ball \(B_R(v)\) is FOᵏ-equivalent to \(B^\*\).

---

# 3. Template Cycles

Let

\[
Z_1(B^\*)
\]

be the cycle space of the template ball.

Dimension bound:

\[
\dim Z_1(B^\*) \le C_0(\Delta,R).
\]

Let

\[
\mathcal T=\{C_1^\*,\dots,C_t^\*\}
\]

be a basis of template cycles.

---

# 4. Embedded Cycles

For every vertex \(v\) and template cycle \(C_i^\*\), there is an embedding

\[
C_i(v) \subseteq G
\]

obtained from the ball \(B_R(v)\).

Thus the set of locally visible cycles is

\[
\mathcal C
=
\{C_i(v) : v\in V,\;1\le i\le t\}.
\]

---

# 5. Cycle Supports

Each embedded cycle satisfies

\[
C_i(v)\subseteq B_R(v).
\]

Hence

\[
|C_i(v)|\le s
\]

where

\[
s=O(\Delta^R).
\]

All generators of the cycle-overlap space are therefore **s-local**.

---

# 6. Ball Overlap

For adjacent vertices \(u,v\),

\[
B_R(u)\cap B_R(v)
\]

contains at least a radius \(R-1\) region.

Thus embeddings of template cycles from nearby centers share edges and vertices.

Overlap size bound:

\[
|B_R(u)\cap B_R(v)|=O(\Delta^{R-1}).
\]

---

# 7. Overlap-Induced Relations

Consider two embeddings of the same template cycle:

\[
C_i(u),\quad C_i(v).
\]

Because their supports intersect, the symmetric difference

\[
C_i(u)\oplus C_i(v)
\]

is supported inside

\[
B_R(u)\cup B_R(v).
\]

This difference decomposes into a bounded number of shorter cycles.

Thus the embeddings satisfy linear relations in \(Z_1(G)\).

---

# 8. Dependency Growth

If many embeddings were linearly independent, we would obtain a large family of disjoint or weakly overlapping s-local cycles.

However bounded degree forces repeated overlaps.

Repeated overlaps yield symmetric-difference relations.

These relations collapse the span dimension.

---

# 9. Overlap Dependency Lemma

There exists a constant

\[
C(\Delta,R)
\]

such that any family of s-local cycles in a bounded-degree graph satisfies

\[
\dim \operatorname{span}\{C_j\}
\le C(\Delta,R)
\]

whenever all cycles arise from embeddings of finitely many template cycles.

---

# 10. Consequence for Local Cycle Span

Since all local cycles in an FOᵏ-homogeneous graph arise from template embeddings,

\[
\dim \mathcal L_s(G)
\le
C(k,\Delta,R).
\]

Recall

\[
\mathcal L_s(G)
=
\operatorname{span}\{C_i(v)\}.
\]

Thus

\[
\mathrm{COR}_R(G)
=
\dim \mathcal L_s(G)
\le C(k,\Delta,R).
\]

---

# 11. Contrapositive

Therefore

\[
\mathrm{COR}_R(G)>C(k,\Delta,R)
\]

implies the graph cannot be FOᵏ\(_R\)-homogeneous.

Hence

\[
|\mathrm{Types}_{k,R}(G)|\ge2.
\]

This yields **FOᵏ local-type diversity**.

---

# 12. Role in the Oblivion Atom

This lemma supplies the structural mechanism:

emplate cycle embeddings
↓
overlap dependencies
↓
bounded cycle span
↓
FOᵏ rigidity


which is the combinatorial heart of the Oblivion framework.

---

# 13. Connection to Chronos

Once FOᵏ diversity is established, refinement algorithms must distinguish multiple local configurations.

FOᵏ locality bounds information per step.

Thus

\[
\mathrm{ED}(F)\ge\Omega(n).
\]

Under patch constructions:

\[
\mathrm{ED}(F)\ge\Omega(n\log n).
\]

---

# 14. Remaining Tasks

To complete the full proof pipeline:

1. formalize the overlap-dependency bound
2. quantify the constant \(C(\Delta,R)\)
3. verify expanders / random lifts satisfy

\[
\mathrm{COR}_R(G)=\Omega(n).
\]

These complete the Oblivion → Chronos bridge.
