# Local Cycle Packing Lemma

Let G be a graph with maximum degree ≤ Δ.

Let R ≥ 1.

Define B_R(v) as the radius-R ball.

Lemma.

There exists a set V0 ⊆ V(G) such that

1. Balls B_{R-1}(v) for v ∈ V0 are pairwise disjoint.
2. |V0| ≥ |V| / (1 + Δ + … + Δ^{R-1}).

Proof.

Construct V0 greedily:

Pick an arbitrary vertex v,
remove B_{R-1}(v),
repeat.

Each step removes ≤ 1 + Δ + … + Δ^{R-1} vertices.

Thus at least |V| / (1 + Δ + … + Δ^{R-1}) vertices are selected.
