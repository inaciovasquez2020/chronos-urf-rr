# Lcake Rigidity Conjecture

## Definition

Let \(G=(V,E)\) be a finite graph with maximum degree \(\Delta\).  
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

---

## Conjecture (Lcake Rigidity)

For every fixed \(\Delta,R\) there exists a constant \(C(\Delta,R)\) such that for every bounded-degree expander family \(G_n\),

\[
\mathrm{Lcake}_R(G_n) \le C(\Delta,R).
\]

---

## Equivalent Formulation

Let

\[
\Phi_R :
\bigoplus_{v\in V} Z_1(B_R(v))
\rightarrow Z_1(G).
\]

Then

\[
\dim \operatorname{Im}(\Phi_R) \le C(\Delta,R).
\]

---

## Empirical Evidence

Measured values for random regular graphs:

| n | degree | R | Lcake |
|---|---|---|---|
80 | 3 | 2 | 9 |
160 | 3 | 2 | 8 |
320 | 3 | 2 | 16 |
640 | 3 | 2 | 9 |

Values remain bounded as \(n\) grows.

---

## Contrast: Periodic Graphs

For lattice graphs:

\[
\mathrm{Lcake}_R(G) = \Theta(|V|)
\]

Example:

| Graph | Vertices | Lcake |
|---|---|---|
20×20 torus | 400 | 399 |
30×30 torus | 900 | 899 |

---

## Role in the Oblivion Atom Program

The Oblivion Atom statement can be expressed as

\[
\mathrm{Lcake}_R(G) \ge T(k,\Delta)
\Rightarrow
G \text{ is not } FO^k_R\text{-homogeneous}.
\]

Thus proving bounded Lcake for expander families establishes a **local topology capacity bound** for FO^k observers.

---

## Status

- Empirical evidence: strong  
- Formal proof: open

---

## Scripts

toolkit/oblivion/scripts/lcake_compute.py
toolkit/oblivion/scripts/lcake_torus_test.py
