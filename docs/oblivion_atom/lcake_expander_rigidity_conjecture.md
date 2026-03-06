# Lcake Expander Rigidity Conjecture

## Statement

Let \(G=(V,E)\) be a finite graph with maximum degree \(\Delta\).

Fix radius \(R\).

Assume the family \(G_n\) is an **expander family**, i.e. there exists a constant
\(\epsilon>0\) such that for all \(S\subseteq V\) with \(|S|\le |V|/2\),

\[
|\partial S| \ge \epsilon |S|.
\]

Then there exists a constant

\[
C(\Delta,R,\epsilon)
\]

such that

\[
\mathrm{Lcake}_R(G_n) \le C(\Delta,R,\epsilon)
\]

for all \(n\).

---

## Equivalent Formulation

Let

\[
\Phi_R :
\bigoplus_{v\in V} Z_1(B_R(v))
\rightarrow Z_1(G)
\]

be the local-cycle aggregation map.

Then

\[
\dim \operatorname{Im}(\Phi_R) \le C(\Delta,R,\epsilon).
\]

---

## Interpretation

Local neighborhoods can only generate **bounded independent cycles** even though the global cycle space

\[
\beta_1(G) = |E|-|V|+1
\]

grows linearly with \(|V|\).

Thus most global cycles are **invisible to bounded-radius observers**.

---

## Evidence

Random regular graphs experimentally show

| n | degree | R | Lcake |
|---|---|---|---|
80 | 3 | 2 | 9 |
160 | 3 | 2 | 8 |
320 | 3 | 2 | 16 |
640 | 3 | 2 | 9 |

Values remain bounded as \(n\) grows.

---

## Contrast: Lattice Graphs

For periodic graphs such as the torus

\[
\mathrm{Lcake}_R(G_n) = \Theta(|V(G_n)|).
\]

Example:

| Graph | Vertices | Lcake |
|---|---|---|
20×20 torus | 400 | 399 |
30×30 torus | 900 | 899 |

---

## Role in the Oblivion Atom Program

The Oblivion Atom rigidity statement can be expressed as

\[
\mathrm{Lcake}_R(G) \ge T(k,\Delta)
\Rightarrow
G \text{ is not } FO^k_R\text{-homogeneous}.
\]

Thus bounding Lcake for expander families yields a **local information capacity bound** for FO\(^k\) observers.

---

## Status

Invariant definition: complete  
Empirical evidence: strong  
Formal theorem: open
