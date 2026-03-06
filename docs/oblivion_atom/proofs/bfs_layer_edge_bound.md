# BFS Layer Edge Bound

## 1. Setup

Let (G=(V,E)) be a finite (d)-regular graph with edge expansion constant (\varepsilon>0).

For a fixed root vertex (v\in V), define the breadth-first search (BFS) layers

[
L_r(v)={u\in V : \mathrm{dist}(v,u)=r}.
]

The radius-(R) ball is

[
B_R(v)=\bigcup_{r=0}^{R} L_r(v).
]

Let (T_R(v)) be the BFS tree induced by these layers.

Edges not belonging to (T_R(v)) are called **collision edges**.

---

# 2. Tree Structure

In the BFS tree,

[
|E(T_R(v))| = |B_R(v)|-1.
]

Thus any additional edge inside (B_R(v)) contributes a cycle.

Define

[
E_{\mathrm{coll}}(R,v)
======================

|E(B_R(v))|-|E(T_R(v))|.
]

Then

[
E_{\mathrm{coll}}(R,v)
======================

|E(B_R(v))|-(|B_R(v)|-1).
]

---

# 3. Expansion Constraint

For every subset (S\subseteq V) with (|S|\le |V|/2),

[
|\partial S| \ge \varepsilon |S|.
]

Apply this to

[
S=B_R(v).
]

The number of edges leaving the ball must satisfy

[
|\partial B_R(v)|\ge \varepsilon |B_R(v)|.
]

---

# 4. Edge Accounting

Every vertex in (B_R(v)) has degree (d).

Hence

[
d|B_R(v)|
=========

2|E(B_R(v))|
+
|\partial B_R(v)|.
]

Substituting the expansion bound:

[
d|B_R(v)|
\ge
2|E(B_R(v))|
+
\varepsilon |B_R(v)|.
]

Thus

[
|E(B_R(v))|
\le
\frac{d-\varepsilon}{2}|B_R(v)|.
]

---

# 5. Collision Edge Lower Bound (Target)

The tree contains exactly (|B_R(v)|-1) edges.

Therefore

[
E_{\mathrm{coll}}(R,v)
======================

|E(B_R(v))|-|B_R(v)|+1.
]

Substituting the inequality structure suggests the existence of constants

[
\alpha>0
]

such that

[
E_{\mathrm{coll}}(R,v)\ge \alpha(d-1)^R.
]

---

# 6. BFS Layer Edge Bound Lemma (Target)

Fix (d\ge3) and (\varepsilon>0).

There exist constants ( \alpha>0 ) and ( R_0>0 ) such that for every
finite (d)-regular (\varepsilon)-expander (G), every vertex (v), and every

[
1\le R\le R_0\log_{d-1}|V|,
]

the number of collision edges satisfies

[
E_{\mathrm{coll}}(R,v)
\ge
\alpha(d-1)^R.
]

---

# 7. Consequence

Since

[
\beta_1(B_R(v)) = E_{\mathrm{coll}}(R,v),
]

the lemma implies

[
\beta_1(B_R(v))\ge \alpha(d-1)^R.
]

This is precisely the condition required by the
Cycle-Expander Rigidity Lemma.

---

# 8. Role in the Oblivion Chain

The BFS collision bound produces the deterministic inequality

[
\beta_1(B_R(v)) \ge \alpha(d-1)^R.
]

Combined with the CORR invariant:

[
CORR_R(G)=\sum_{\tau} \beta_1(\tau)^2,
]

we obtain

[
CORR_R(G)\ge T(k,d),
]

which forces

[
FO^k
\text{ type diversity}.
]

---

# 9. Status

| Component                           | Status      |
| ----------------------------------- | ----------- |
| BFS layer definitions               | proven      |
| expansion inequality                | classical   |
| collision counting framework        | established |
| deterministic collision lower bound | open        |

The lemma therefore represents the final deterministic ingredient required to close the expander rigidity chain.

