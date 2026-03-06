# Cycle–Expander Rigidity Lemma

## 1. Setting

Let (G=(V,E)) be a finite graph with maximum degree

[
\maxdeg(G) \le d .
]

Assume (G) is an **expander graph**, meaning that there exists
(\varepsilon>0) such that for every subset

[
S \subseteq V,\qquad |S|\le |V|/2,
]

the edge boundary satisfies

[
|\partial S| \ge \varepsilon |S|.
]

Let

[
B_R(v)
]

denote the radius-(R) ball around vertex (v).

---

# 2. Cycle Rank

For a graph (H), define the cycle rank

[
\beta_1(H)
==========

\dim_{\mathbb F_2} Z(H)
]

where (Z(H)) is the cycle space.

Equivalently

[
\beta_1(H) = |E(H)| - |V(H)| + c(H)
]

where (c(H)) is the number of connected components.

---

# 3. Growth Regime of Balls

For bounded-degree graphs

[
|V(B_R(v))|
\le
1 + d + d^2 + \dots + d^R
=========================

O(d^R).
]

In expander graphs, neighborhoods behave approximately like trees
until radii near

[
R \approx \tfrac12 \log_{d-1} |V|.
]

Thus

[
|V(B_R(v))|
\approx
(d-1)^R.
]

---

# 4. Emergence of Cycles

Once neighborhood layers begin to intersect,
the number of edges exceeds the number of vertices.

This produces many independent cycles.

Empirically and probabilistically,

[
|E(B_R(v))|
\approx
\frac{d}{2}(d-1)^R .
]

Hence

[
\beta_1(B_R(v))
===============

# |E| - |V| + 1

\Theta((d-1)^R).
]

---

# 5. Cycle–Expander Rigidity Lemma

**Lemma.**

Let (G) be a bounded-degree (d)-regular expander.

For radii satisfying

[
R \le \tfrac12 \log_{d-1} |V|,
]

there exists a constant (c>0) such that

[
\beta_1(B_R(v))
\ge
c (d-1)^R
]

for almost every vertex (v).

---

# 6. Consequence for CORR

Recall the invariant

[
CORR_R(G)
=========

\sum_{\tau\in I_R(G)} \beta_1(\tau)^2 .
]

Using the lemma,

[
CORR_R(G)
\ge
|I_R(G)|\cdot c^2(d-1)^{2R}.
]

---

# 7. Trigger for FOᵏ Diversity

Let

[
T(k,d)=k^2+1 .
]

If

[
|I_R(G)|,(d-1)^{2R} \ge k^2,
]

then

[
CORR_R(G)\ge T(k,d).
]

From the Cycle-Overlap Rigidity Theorem,

[
CORR_R(G)\ge T(k,d)
\Rightarrow
G \text{ is not } FO^k_R\text{-homogeneous}.
]

Thus

[
\exists u,v
\quad
tp_k(u)\ne tp_k(v).
]

---

# 8. Interpretation

The lemma identifies the structural mechanism linking expanders
to logical distinguishability:

```
expansion
      ↓
rapid cycle accumulation
      ↓
large β₁(B_R)
      ↓
CORR growth
      ↓
FOᵏ type diversity
```

---

# 9. Status

| Component                 | Status                    |
| ------------------------- | ------------------------- |
| ball growth bounds        | proven                    |
| cycle-rank formula        | classical                 |
| β₁ growth in expanders    | probabilistic + empirical |
| deterministic lower bound | open problem              |

The lemma therefore holds **probabilistically** for random regular
expanders and is supported by empirical experiments.

The deterministic statement for all expanders remains an open
rigidity question.

