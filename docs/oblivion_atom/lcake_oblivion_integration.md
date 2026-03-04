# Lcake Integration into the Oblivion Atom Framework

## Purpose

This document integrates the **Lcake invariant** into the Oblivion Atom program as an operational proxy for **cycle-overlap rank**.

The invariant measures the amount of global cycle information accessible through bounded-radius neighborhoods.

---

# 1 Definition

Let \(G=(V,E)\) be a finite graph.

Fix radius \(R\).

Define

\[
\mathrm{Lcake}_R(G)
=
\dim_{\mathbb F_2}
\operatorname{span}
\left(
\bigcup_{v\in V}
(\iota_v)_* Z_1(B_R(v))
\right).
\]

Equivalently,

\[
\Phi_R :
\bigoplus_{v\in V} Z_1(B_R(v))
\to Z_1(G)
\]

\[
\mathrm{Lcake}_R(G)
=
\dim \operatorname{Im}(\Phi_R).
\]

Thus Lcake measures the **global cycle information accessible locally**.

---

# 2 Relation to Cycle-Overlap Rank

Recall the Oblivion Atom quantity

\[
COR_R(G)
=
\dim_{\mathbb F_2}
\left(
\sum_{v\in V}
(\iota_v)_* Z_1(B_R(v))
\right).
\]

Therefore

\[
\boxed{
\mathrm{Lcake}_R(G) = COR_R(G)
}
\]

so Lcake is simply the **computable form of cycle-overlap rank**.

---

# 3 Empirical Regimes

Experiments reveal two scaling regimes.

### Expander-type graphs

\[
\mathrm{Lcake}_R(G_n) = O(1)
\]

independent of graph size.

Example:

| n | Lcake |
|---|---|
80 | 9 |
160 | 8 |
320 | 16 |
640 | 9 |

---

### Periodic lattices

\[
\mathrm{Lcake}_R(G_n) = \Theta(|V|)
\]

Example:

| Graph | Vertices | Lcake |
|---|---|---|
20×20 torus | 400 | 399 |
30×30 torus | 900 | 899 |

---

# 4 Local Cycle Visibility Principle

Local observers with radius \(R\) can only access cycle information bounded by

\[
\mathrm{Lcake}_R(G).
\]

Thus

| Graph family | Local topology capacity |
|---|---|
Expanders | bounded |
Lattices | extensive |

---

# 5 Oblivion Atom Reformulation

The Oblivion Atom statement can be restated as

\[
\mathrm{Lcake}_R(G) \ge T(k,\Delta)
\Rightarrow
G \text{ is not } FO^k_R\text{-homogeneous}.
\]

Equivalently:

large local cycle span forces **local type diversity**.

---

# 6 Interpretation for FO^k Algorithms

FO^k algorithms observe only bounded neighborhoods.

Therefore the **cycle information capacity available to such algorithms** is limited by

\[
\mathrm{Lcake}_R(G).
\]

For expander families

\[
\mathrm{Lcake}_R(G)=O(1)
\]

so global topology cannot be reconstructed from local views.

---

# 7 Role in the Chronos / EntropyDepth Program

Lcake provides an operational measurement of the **topological information available to local refinement processes**.

It therefore connects:

- cycle-overlap rank
- FO^k locality limits
- Oblivion Atom
- EntropyDepth information constraints.

---

# 8 Current Status

Component | Status
---|---
Definition | complete
Computation | implemented
Empirical evidence | strong
Formal theorem | open

---

# 9 Repository scripts

toolkit/oblivion/scripts/lcake_compute.py
toolkit/oblivion/scripts/lcake_torus_test.py


---

# 10 Open Problem

Prove a structural theorem of the form

\[
\mathrm{Lcake}_R(G_n)=O(1)
\]

for bounded-degree expander families.

This would establish the **Oblivion Atom rigidity condition** for such graphs.
