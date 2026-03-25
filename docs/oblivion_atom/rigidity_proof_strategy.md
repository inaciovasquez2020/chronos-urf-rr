# Proof Strategy for the Cycle–Overlap Rigidity Lemma

## Status

Strategy document for the missing lemma in the Oblivion → Chronos bridge.

Target lemma:

\[
FO^k_R\text{-homogeneous}
\Rightarrow
\mathrm{COR}_R(G) \le C(k,\Delta,R).
\]

This document outlines the proof program required to establish the rigidity statement.

---

# 1. Graph Model

Let \(G=(V,E)\) be a finite graph with maximum degree

\[
\deg(G)\le \Delta.
\]

Fix parameters

\[
k,R \in \mathbb{N}.
\]

Define the radius-\(R\) neighborhood

\[
B_R(v) = \{u \in V : \mathrm{dist}(u,v) \le R\}.
\]

---

# 2. Cycle–Overlap Rank

Local cycles are drawn from

\[
Z_1(B_R(v)).
\]

Define the embedding map

\[
\Phi_R :
\bigoplus_{v\in V} Z_1(B_R(v))
\longrightarrow
Z_1(G).
\]

Cycle–overlap rank:

\[
\mathrm{COR}_R(G)
=
\dim_{\mathbb F_2} \operatorname{Im}(\Phi_R).
\]

---

# 3. FOᵏ Homogeneity

Graph \(G\) is \(FO^k_R\)-homogeneous if

\[
(G,u) \equiv_{FO^k_R} (G,v)
\quad \forall u,v \in V.
\]

Thus every radius-\(R\) neighborhood is indistinguishable by \(k\)-variable logic.

---

# 4. Finite Template Space

Because graphs have bounded degree:

\[
|B_R(v)| \le 1+\Delta+\dots+\Delta^R.
\]

Hence the number of possible rooted \(R\)-balls is finite.

Thus the FOᵏ type space satisfies

\[
|\mathrm{Types}_{k,R}| \le N(k,\Delta,R).
\]

Under homogeneity there exists a canonical template ball

\[
B^\*.
\]

---

# 5. Template Cycle Space

Let

\[
Z_1(B^\*)
\]

be the cycle space of the template ball.

Dimension bound:

\[
\dim Z_1(B^\*) \le E(B^\*) - V(B^\*) + 1.
\]

Since \(B^\*\) is bounded:

\[
\dim Z_1(B^\*) \le C_0(\Delta,R).
\]

---

# 6. Embedding Structure

Each local cycle in \(B_R(v)\) corresponds to an embedding of a template cycle in \(B^\*\).

Hence

\[
\operatorname{Im}(\Phi_R)
\subseteq
\text{span of embeddings of cycles in } B^\*.
\]

The main difficulty is bounding the dimension of this span.

---

# 7. Cycle Support Compression

Key observation:

Every cycle from \(B_R(v)\) has support contained in a ball of radius \(R\).

Therefore every generator of \(\operatorname{Im}(\Phi_R)\) has support size

\[
O(\Delta^R).
\]

Let

\[
s = O(\Delta^R).
\]

All generators are \(s\)-local cycles.

---

# 8. Linear Dependency Mechanism

If

\[
\mathrm{COR}_R(G)
\]

were arbitrarily large under homogeneity, we would obtain many linearly independent \(s\)-local cycles.

However overlapping cycles produce linear dependencies because:

* cycles share edges
* cycles share vertices
* template embeddings repeat

This yields compression in the cycle span.

---

# 9. Bounded Dimension Claim

Goal:

show that the span of all \(s\)-local cycles in a homogeneous graph has bounded dimension.

Formally prove

\[
\dim \operatorname{span}\{s\text{-local cycles}\}
\le C(k,\Delta,R).
\]

---

# 10. EF-Game Perspective

If the cycle-overlap rank were too large, then many vertices would participate in different local cycle configurations.

Spoiler could distinguish these configurations in the \(k\)-pebble Ehrenfeucht–Fraïssé game.

This would contradict FOᵏ homogeneity.

---

# 11. Result

Combining compression and EF distinguishability yields

\[
\mathrm{COR}_R(G)
\le
C(k,\Delta,R).
\]

---

# 12. Contrapositive

Therefore

\[
\mathrm{COR}_R(G) > C(k,\Delta,R)
\]

implies

\[
|\mathrm{Types}_{k,R}(G)| \ge 2.
\]

Hence FOᵏ local diversity follows from large cycle-overlap rank.

---

# 13. Role in Chronos

This rigidity lemma provides the structural bridge:

Cycle overlap growth
↓
FOᵏ local-type diversity
↓
Configuration pumping
↓
bounded refinement information
↓
EntropyDepth lower bound


Thus the lemma completes the Oblivion → Chronos connection.

---

# 14. Remaining Tasks

To finish the proof formally:

1. Bound the dimension of \(s\)-local cycle span.
2. Formalize EF-game distinguishability argument.
3. Construct explicit graph families with

\[
\mathrm{COR}_R(G)=\Omega(n).
\]

These complete the rigidity argument needed for the Chronos entropy barrier.
