# Theorem: Local Cycle Independence Bound

Let G be a graph with maximum degree ≤ Δ.

Define s-local cycles as cycles contained inside some B_R(v).

Theorem.

The number of linearly independent s-local cycles is bounded by

C(Δ,R) = O(Δ^(2R)).

Proof idea.

1. Each ball B_R(v) contains ≤ Δ^R vertices.
2. The cycle space dimension of each ball ≤ O(Δ^R).
3. Balls overlap in regions of size ≥ Δ^(R−1).
4. Overlap implies symmetric-difference relations among embedded cycles.
5. Therefore only O(Δ^(2R)) independent cycles exist.

Thus

dim span{s-local cycles} ≤ C(Δ,R).
