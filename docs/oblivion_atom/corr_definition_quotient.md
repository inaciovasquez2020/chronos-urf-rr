# Quotient Cycle–Overlap Correlation Rank (CORR)

## Motivation

The original span-based definition of cycle-overlap correlation rank embeds
cycle-pair indicators into ( \mathbb{F}_2^{E\times E} ).
Under graph symmetries (e.g., vertex-transitive graphs like the torus
( \mathbb{Z}_n \times \mathbb{Z}_n )), translated copies of the same
cycle contribute linearly independent vectors.

This causes the span dimension to grow as ( \Theta(|V|^2) ), which breaks
rigidity statements relating cycle overlap to FOᵏ local homogeneity.

To remove this artifact, the correct invariant is defined **modulo rooted
ball isomorphism**, collapsing all isomorphic local structures to a single
representative.

---

## Rooted Ball Types

Let ( G = (V,E) ) be a finite graph with ( \maxdeg(G) \le \Delta ).

For ( R \in \mathbb{N} ), define the radius-(R) rooted ball

[
B_R(v) = \text{induced subgraph on vertices within distance } \le R \text{ of } v.
]

Two vertices (u,v) have the same **rooted (R)-type** if

[
B_R(u) \cong B_R(v)
]

as rooted graphs.

Define the set of rooted ball types

[
T_R(G) =
{, [B_R(v)]_{\cong} \mid v \in V(G) ,}.
]

---

## Cycle Space of a Ball

For a graph (H), let

[
Z(H)
]

denote the cycle space over ( \mathbb{F}_2 ).

Define

[
\beta_1(H) = \dim_{\mathbb{F}_2} Z(H)
]

which equals the first Betti number of (H).

---

## Definition: Quotient CORR

The **cycle-overlap correlation rank** at radius (R) is

[
CORR_R(G)
=========

\sum_{\tau \in T_R(G)}
\beta_1(\tau)^2 .
]

Interpretation:

* each rooted ball type contributes once
* its contribution is the square of its cycle-space dimension
* multiplicities from vertex translations are removed

---

## Module Formulation

Let

[
M_R(G)
======

\bigoplus_{v \in V(G)}
Z(B_R(v)) \otimes Z(B_R(v)).
]

For every rooted isomorphism

[
\varphi : B_R(v) \to B_R(w)
]

identify generators via

[
c_1 \otimes c_2
\sim
\varphi_*(c_1) \otimes \varphi_*(c_2).
]

The quotient module dimension equals

[
CORR_R(G)
=========

\dim_{\mathbb{F}_2} M_R(G).
]

---

## Bounds

For graphs with ( \maxdeg(G) \le \Delta ):

[
|V(B_R)| \le \Delta^R
]

[
|E(B_R)| \le \frac{\Delta^{R+1}}{2}
]

Thus

[
\beta_1(B_R)
\le
\frac{\Delta^{R+1}}{2}.
]

---

## Conditional Rigidity Statement

Let

[
R(k,\Delta) = \left\lfloor \frac{\log(2k)}{\log \Delta} \right\rfloor
]

[
T(k,\Delta) =
\left(\frac{\Delta^{R(k,\Delta)+1}}{2}\right)^2 + 1 .
]

Assuming WL-completeness at radius (R),

[
CORR_R(G) \ge T(k,\Delta)
\Rightarrow
G \text{ is not } FO^k_R\text{-homogeneous}.
]

---

## Role in the Oblivion Atom

The quotient CORR invariant removes translation artifacts and isolates
the **local cycle complexity** of graph neighborhoods.

This allows cycle-overlap growth to be linked to:

* FOᵏ local type diversity
* configuration pumping arguments
* EntropyDepth lower bounds
* Chronos rigidity phenomena.

It therefore forms the corrected algebraic invariant used by the
Oblivion Atom framework.

