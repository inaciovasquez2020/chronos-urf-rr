# Local Cycle Independence Theorem

Let G be a graph with maximum degree Δ.

A cycle is s-local if it is contained in B_R(v) for some vertex v.

Let s ≤ O(Δ^R).

Theorem.

In any bounded-degree graph,

dim span{ s-local cycles } ≤ C(Δ,R)

for constant

C(Δ,R) = O(Δ^{2R})

Proof sketch.

1. Each s-local cycle lies in some B_R(v).
2. |B_R(v)| ≤ Δ^R.
3. Number of edges in ball ≤ O(Δ^R).
4. Cycle space dimension ≤ E−V+1 ≤ O(Δ^R).
5. Overlapping balls produce linear dependencies.
6. Independent s-local cycles therefore bounded by O(Δ^{2R}).

Thus

COR_R(G) ≤ C(Δ,R).
