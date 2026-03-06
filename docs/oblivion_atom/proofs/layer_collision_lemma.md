# Layer Collision Lemma

## 1. Context

Let (G=(V,E)) be a finite (d)-regular graph with edge expansion constant (\varepsilon>0).

For a vertex (v\in V), define the radius-(R) ball

[
B_R(v) = { u \in V : \mathrm{dist}(v,u) \le R }.
]

Let (T_R(v)) denote the breadth-first search tree of (B_R(v)).

Edges of (B_R(v)) not belonging to (T_R(v)) are called **non-tree edges**.

Each such edge contributes at least one independent cycle in the ball.

---

# 2. Cycle Rank Relation

For any connected graph (H),

[
\beta_1(H) = |E(H)| - |V(H)| + 1.
]

Equivalently,

[
\beta_1(H) = #(\text{non-tree edges in }H).
]

Therefore

[
\beta_1(B_R(v))
\ge
#(\text{non-tree edges in }B_R(v)).
]

---

# 3. Expansion Constraint

Since (G) is an (\varepsilon)-edge-expander,

for every set (S\subseteq V) with (|S|\le |V|/2),

[
|\partial S| \ge \varepsilon |S|.
]

Applying this to BFS layers forces rapid growth of neighborhoods.

---

# 4. BFS Layer Growth

Let

[
L_r(v)={u: \mathrm{dist}(v,u)=r}.
]

Then

[
|L_r(v)| \le d(d-1)^{r-1}.
]

For expanders, collisions between BFS layers occur frequently once

[
r \approx \log_{d-1}|V|.
]

These collisions generate non-tree edges.

---

# 5. Layer Collision Lemma (Target)

**Lemma.**

Fix (d\ge3) and (\varepsilon>0).

There exist constants

[
\alpha>0,\quad R_0>0
]

such that for every finite (d)-regular (\varepsilon)-expander (G), every vertex (v), and every radius

[
1\le R\le R_0\log_{d-1}|V|,
]

the ball (B_R(v)) contains at least

[
\alpha (d-1)^R
]

non-tree edges.

---

# 6. Consequence

From Section 2,

[
\beta_1(B_R(v))
\ge
\alpha(d-1)^R.
]

Thus balls in expanders accumulate cycles exponentially in the radius.

---

# 7. Role in Oblivion Atom

Combining the lemma with the CORR invariant:

[
CORR_R(G)
=========

\sum_{\tau\in I_R(G)} \beta_1(\tau)^2,
]

we obtain

[
CORR_R(G)
\ge
|I_R(G)|\alpha^2(d-1)^{2R}.
]

Hence sufficiently large (R) forces

[
CORR_R(G)\ge T(k,d),
]

which triggers FO(^k) type diversity.

---

# 8. Status

| Component                 | Status               |
| ------------------------- | -------------------- |
| ball size bounds          | proven               |
| cycle rank formula        | classical            |
| collision phenomenon      | empirically verified |
| deterministic lower bound | open                 |

This lemma represents the final deterministic rigidity step required in the Oblivion chain.

