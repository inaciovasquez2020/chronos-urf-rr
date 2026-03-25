# EF-Game Cycle Detection Lemma

## Status

Technical lemma in the Oblivion → Chronos bridge.

Purpose: show that sufficiently large **cycle-overlap rank** produces a **Spoiler win** in the \(k\)-pebble Ehrenfeucht–Fraïssé game on radius-\(R\) neighborhoods. This converts structural cycle growth into **FOᵏ distinguishability**.

Target implication:

\[
\mathrm{COR}_R(G) > C(k,\Delta,R)
\;\Rightarrow\;
\exists u,v \in V(G) \text{ such that } (G,u) \not\equiv_{FO^k_R} (G,v).
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

Define the radius-\(R\) neighborhood

\[
B_R(v)=\{u\in V:\operatorname{dist}(u,v)\le R\}.
\]

---

# 2. Cycle-Overlap Rank

Local cycles are cycles contained in some ball \(B_R(v)\).

Define the cycle-overlap map

\[
\Phi_R:
\bigoplus_{v\in V} Z_1(B_R(v))
\longrightarrow
Z_1(G).
\]

The **cycle-overlap rank** is

\[
\mathrm{COR}_R(G)
=
\dim_{\mathbb F_2}\operatorname{Im}(\Phi_R).
\]

Interpretation: number of independent cycles visible within radius \(R\).

---

# 3. FOᵏ Local Types

Two vertices \(u,v\) are FOᵏ\(_R\)-equivalent if

\[
(G,u)\equiv_{FO^k_R}(G,v).
\]

Equivalently, Duplicator wins the \(k\)-pebble EF game played inside radius \(R\) neighborhoods.

Graph \(G\) is **FOᵏ\(_R\)-homogeneous** if all vertices share the same type.

---

# 4. EF Game Model

The \(k\)-pebble Ehrenfeucht–Fraïssé game proceeds in rounds.

At each round:

1. Spoiler selects a vertex in one structure.
2. Duplicator selects a matching vertex in the other.
3. Pebble assignments must preserve adjacency relations.

Duplicator wins if the partial mapping remains a partial isomorphism.

---

# 5. Local Cycle Witness

Let

\[
C_1,\dots,C_m
\]

be independent cycles in

\[
\operatorname{Im}(\Phi_R).
\]

Each cycle lies inside some ball \(B_R(v_i)\).

If

\[
m>C(k,\Delta,R),
\]

these cycles produce many distinct local cycle configurations.

---

# 6. Configuration Diversity

Vertices participating in different subsets of independent cycles have distinct structural signatures.

Define the **cycle participation vector**

\[
\sigma(v)=(\mathbf{1}_{v\in C_1},\dots,\mathbf{1}_{v\in C_m}).
\]

Large \(m\) produces many distinct signatures.

These signatures are detectable within bounded radius.

---

# 7. Spoiler Strategy

Suppose \(u,v\) have different cycle signatures.

Spoiler plays as follows:

1. Place pebble on vertex \(u\).
2. Force exploration along edges of cycle \(C_i\) that passes through \(u\).
3. Duplicator must respond with vertices preserving adjacency.

Because \(v\) does not lie on the same cycle configuration, the partial isomorphism fails.

Spoiler wins in at most

\[
O(R)
\]

moves.

---

# 8. Bounded Variable Constraint

Because cycles have bounded radius \(R\), Spoiler needs only

\[
k
\]

pebbles to track cycle adjacency and closure.

Thus the distinguishing strategy lies inside FOᵏ.

---

# 9. EF-Game Cycle Detection Lemma

**Lemma**

There exists a constant

\[
C(k,\Delta,R)
\]

such that if

\[
\mathrm{COR}_R(G)>C(k,\Delta,R),
\]

then Spoiler wins the \(k\)-pebble EF game on some pair of vertices.

Therefore

\[
(G,u)\not\equiv_{FO^k_R}(G,v)
\]

for some \(u,v\in V(G)\).

---

# 10. Result

Large cycle-overlap rank forces

\[
|\mathrm{Types}_{k,R}(G)|\ge2.
\]

Hence FOᵏ local diversity follows from cycle growth.

---

# 11. Role in Oblivion

This lemma provides the **logical detection step**:

cycle-overlap rank growth
↓
EF-game detection
↓
FOᵏ local-type diversity


This complements the **linear-algebraic compression** arguments of the previous lemmas.

---

# 12. Connection to Chronos

Once FOᵏ diversity exists, refinement algorithms must distinguish multiple local configurations.

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

# 13. Remaining Technical Tasks

To finalize the proof:

1. bound the number of distinct cycle participation signatures
2. formalize the Spoiler strategy
3. connect EF-game witnesses to FOᵏ formulas

Completing these tasks establishes the cycle-overlap ⇒ FOᵏ diversity bridge.
