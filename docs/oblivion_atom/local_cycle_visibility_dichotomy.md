# Local Cycle Visibility Dichotomy (Lcake)

## Definition

Let \(G=(V,E)\) be a finite graph.

Fix a radius \(R\). For each vertex \(v \in V\), define the radius-\(R\) ball

\[
B_R(v) = \{u \in V : \mathrm{dist}(u,v) \le R\}.
\]

Let \(Z_1(H)\) denote the cycle space of a graph \(H\) over \(\mathbb{F}_2\).

Define the **Local-Cycle Aggregation Kernel Energy**

\[
\mathrm{Lcake}_R(G)
=
\dim_{\mathbb F_2}
\operatorname{span}
\left(
\bigcup_{v \in V}
(\iota_v)_* Z_1(B_R(v))
\right),
\]

where \((\iota_v)_*\) denotes the inclusion of cycles from the ball \(B_R(v)\) into the global cycle space \(Z_1(G)\).

Equivalently,

\[
\mathrm{Lcake}_R(G)
=
\dim_{\mathbb F_2} \operatorname{Im}(\Phi_R)
\]

where

\[
\Phi_R :
\bigoplus_{v\in V} Z_1(B_R(v))
\rightarrow
Z_1(G).
\]

Thus \(\mathrm{Lcake}_R(G)\) measures how much of the **global cycle space** can be generated from **cycles visible in radius-\(R\) neighborhoods**.

---

## Empirical Observation

Experiments on random regular graphs and periodic lattices show two sharply different scaling regimes.

### Random bounded-degree graphs

For random \(d\)-regular graphs with bounded degree,

\[
\mathrm{Lcake}_R(G_n) = O(d^R),
\]

independent of the number of vertices.

Example measurements (degree \(3\), \(R=2\)):

| n | Lcake |
|---|---|
80 | 9 |
160 | 8 |
320 | 16 |
640 | 9 |

Thus local cycle information remains **bounded** even as the graph size grows.

---

### Periodic lattice graphs

For periodic lattice graphs such as the 2-dimensional torus,

\[
\mathrm{Lcake}_R(G_n) = \Theta(|V(G_n)|).
\]

Example measurements:

| graph | vertices | Lcake |
|---|---|---|
20×20 torus | 400 | 399 |
30×30 torus | 900 | 899 |

Local cycles generate essentially the **entire global cycle space**.

---

## Local Cycle Visibility Dichotomy

These experiments suggest the following structural phenomenon.

### Dichotomy (empirical form)

For bounded-degree graph families \(G_n\) and fixed radius \(R\),

\[
\mathrm{Lcake}_R(G_n)
\in
\{ O(1),\ \Theta(|V(G_n)|) \}.
\]

That is, local cycles either generate **only a bounded amount of global topology**, or they generate **a linear fraction of the global cycle space**.

---

## Interpretation

The invariant \(\mathrm{Lcake}\) measures **how much global topology is visible locally**.

Two regimes appear:

| Graph type | Local visibility of cycles |
|---|---|
Expander-type graphs | bounded |
Periodic lattices | extensive |

Thus \(\mathrm{Lcake}\) detects whether the global cycle structure of a graph is **locally reconstructible**.

---

## Relation to Oblivion Atom

The Oblivion Atom program studies limits of information available to algorithms restricted to bounded-radius local views.

Since such algorithms can only observe subgraphs \(B_R(v)\), the quantity

\[
\mathrm{Lcake}_R(G)
\]

measures the **maximum global cycle information accessible to any radius-\(R\) observer**.

In expander-type graphs this information is **bounded**, while in periodic graphs it scales with graph size.

This invariant therefore provides an operational probe for **local-vs-global topology separation**.

---

## Current Status

- Definition: complete
- Computation: implemented
- Empirical evidence: strong
- Formal theorem: open

---

## Experimental Scripts

The following scripts compute Lcake:

toolkit/oblivion/scripts/lcake_compute.py
toolkit/oblivion/scripts/lcake_torus_test.py


These generate empirical measurements for random regular graphs and lattice graphs.

---

## Open Problem

Prove a structural theorem of the form

\[
\mathrm{Lcake}_R(G_n) = O(1)
\]

for bounded-degree expander families, and characterize precisely which graph families satisfy

\[
\mathrm{Lcake}_R(G_n) = \Theta(|V(G_n)|).
\]

Such a theorem would formalize the **Local Cycle Visibility Dichotomy** suggested by the experiments.


