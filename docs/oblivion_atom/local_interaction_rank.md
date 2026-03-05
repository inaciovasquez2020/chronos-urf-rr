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

