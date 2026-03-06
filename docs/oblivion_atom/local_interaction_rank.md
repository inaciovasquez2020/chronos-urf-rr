# Local Interaction Rank (LIR)

## Definition

Let \(G = (V,E)\) be a finite graph and let \(R \in \mathbb{N}\).

For each vertex \(v \in V\), denote by

\[
B_R(v)
\]

the radius-\(R\) ball around \(v\) in the graph metric.

Let

\[
\mathcal{C}_R(v)
\]

be the set of simple cycles contained in \(B_R(v)\).  
Choose a cycle basis for \(B_R(v)\), and represent each cycle as the set of its edges.

Define the **cycle-overlap graph**

\[
H_R(v)
\]

as follows:

- each node of \(H_R(v)\) corresponds to a cycle in the cycle basis of \(B_R(v)\)
- two nodes are connected if the corresponding cycles share at least one edge.

The **Local Interaction Rank** at \(v\) is

\[
\mathrm{LIR}_R(v) = 
\max_{C \subseteq H_R(v)} |C|
\]

where \(C\) ranges over the connected components of the cycle-overlap graph.

The **Local Interaction Rank of \(G\)** is

\[
\mathrm{LIR}_R(G) =
\max_{v \in V} \mathrm{LIR}_R(v)
\]

---

## Interpretation

\(\mathrm{LIR}_R(G)\) measures the **maximum number of mutually interacting local cycles** inside a radius-\(R\) neighborhood.

- If cycles are isolated, LIR is small.
- If cycles overlap and propagate across the neighborhood, LIR grows.

Thus LIR quantifies **local cycle entanglement**.

---

## Empirical Observations

Using `lir_test.py`, the following behavior is observed.

### Cycle graph

\[
\mathrm{LIR}_R(G) = 0
\]

A single loop has no interacting cycles.

---

### Ladder graph

\[
\mathrm{LIR}_R(G) = 1
\]

Each square interacts only with its immediate neighbors.

---

### Random regular graph

\[
\mathrm{LIR}_R(G) \approx O(1)
\]

Local neighborhoods are nearly tree-like, so cycle interaction remains bounded.

---

### Torus grid

\[
\mathrm{LIR}_R(G) \approx \Theta(R^2)
\]

Cycles overlap in a planar lattice structure.

---

### Triangular grid

Example scan:

R = 1 LIR = 5
R = 2 LIR = 24
R = 3 LIR = 54
R = 4 LIR = 96
R = 5 LIR = 150
R = 6 LIR = 216


Empirically:

\[
\mathrm{LIR}_R(G) \approx 6R^2
\]

---

## Structural Dichotomy (Empirical)

Graphs appear to fall into two regimes.

### Tree-like regime

\[
\mathrm{LIR}_R(G) = O(1)
\]

Examples:

- cycles
- ladders
- random regular graphs

---

### Dense cycle regime

\[
\mathrm{LIR}_R(G) = \Theta(R^2)
\]

Examples:

- torus grids
- triangular lattices

---

## Relation to the Oblivion Atom Program

The Oblivion Atom conjecture seeks a structural invariant that forces **FO\(^k\) type diversity** in bounded-degree graphs.

The working hypothesis emerging from experiments is:

> Large Local Interaction Rank may force FO\(^k\) configuration divergence.

Informally:

high LIR → overlapping cycle constraints → local type asymmetry


This suggests that **cycle interaction density** may be the missing structural obstruction.

---

## Status

Current status: **empirical invariant under investigation**.

Further work required:

- connect LIR to cycle-overlap rank
- relate LIR growth to EF-game configuration divergence
- test on expanders and random lifts
- determine whether bounded LIR implies FO\(^k\)-homogeneity

---

## Implementation

Reference implementation:

toolkit/oblivion/scripts/lir_test.py


The script computes:

LIR_R(G)


for several graph families and supports radius scanning experiments.

---

## Next Research Questions

1. Does bounded \(\mathrm{LIR}_R(G)\) imply bounded cycle-overlap rank?
2. Can large \(\mathrm{LIR}_R(G)\) force EF-configuration pumping?
3. Is \(\mathrm{LIR}_R(G)\) equivalent to the obstruction in the Oblivion Atom conjecture?

These questions remain open.


