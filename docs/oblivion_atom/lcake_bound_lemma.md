# Lcake Local Bound Lemma

## Lemma (Local Cycle Bound)

Let \(G\) be a graph with maximum degree \(\Delta\).  
Fix radius \(R\).

Then for any vertex \(v\),

\[
\dim_{\mathbb F_2} Z_1(B_R(v)) \le |E(B_R(v))|
\]

and

\[
|E(B_R(v))| \le \frac{\Delta^{R+1}}{\Delta-1}.
\]

Thus

\[
\dim Z_1(B_R(v)) = O(\Delta^R).
\]

---

## Consequence

Each radius-\(R\) neighborhood contributes at most

\[
O(\Delta^R)
\]

independent cycles.

---

## Global Lcake Bound

Since

\[
\mathrm{Lcake}_R(G)
=
\dim
\operatorname{span}
\Big(
\bigcup_{v\in V} Z_1(B_R(v))
\Big),
\]

we obtain the trivial bound

\[
\mathrm{Lcake}_R(G)
\le
|V| \cdot O(\Delta^R).
\]

---

## Interpretation

The challenge in the Lcake Rigidity Program is to prove that **most of these local cycles are linearly dependent globally**, giving

\[
\mathrm{Lcake}_R(G)=O(1)
\]

for expander families.

---

## Role in Oblivion Atom

This lemma establishes the **local information ceiling** for cycle visibility used by FO\(^k\) observers.

The remaining step is to show that expansion forces **strong overlap dependencies** between local cycles.

---

## Status

Local bound: proven  
Global rigidity: open
