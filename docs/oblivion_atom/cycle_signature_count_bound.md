# Cycle Participation Signature Counting Bound

## Status

Structural lemma in the Oblivion framework.

Goal: bound the number of distinct **cycle participation signatures** that can occur in an FOᵏ_R-homogeneous bounded-degree graph.

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

Fix

\[
k,R\in\mathbb N.
\]

Define radius-R balls

\[
B_R(v).
\]

---

# 2. Cycle-Overlap Rank

Define

\[
\Phi_R :
\bigoplus_{v\in V} Z_1(B_R(v))
\to
Z_1(G)
\]

and

\[
\mathrm{COR}_R(G)
=
\dim_{\mathbb F_2}\operatorname{Im}(\Phi_R).
\]

Let

\[
C_1,\dots,C_m
\]

be independent cycles.

---

# 3. Cycle Participation Signatures

Define for each vertex

\[
\sigma(v)
=
(\mathbf 1_{v\in C_1},\dots,\mathbf 1_{v\in C_m}).
\]

This vector records which cycles contain the vertex.

---

# 4. Signature Bound

If neighborhoods are FOᵏ_R-equivalent, then local structure around each vertex is logically identical.

Therefore signatures must arise from a bounded template configuration.

Hence there exists

\[
S(k,\Delta,R)
\]

such that

\[
|\{\sigma(v):v\in V\}|
\le
S(k,\Delta,R).
\]

---

# 5. Consequence

If

\[
m
>
S(k,\Delta,R)
\]

then two vertices must have different cycle signatures visible in radius R.

Thus

\[
(G,u)\not\equiv_{FO^k_R}(G,v).
\]

---

# 6. Role

This lemma bounds how many independent cycles can coexist without breaking FOᵏ homogeneity.
