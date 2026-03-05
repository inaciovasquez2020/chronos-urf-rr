# docs/oblivion_atom/trace_method_short_cycles.md

Trace Method Short Cycle Bound

Let A be the adjacency matrix of a d-regular graph.

trace(A^k) = sum_i λ_i^k

If |λ_i| ≤ λ < d for i ≥ 2 then

trace(A^k) ≥ d^k − (n−1)λ^k

Choose

k ≈ (2 log n)/(log(d/λ))

Then

d^k >> n λ^k

Thus many closed walks exist.

Each simple cycle contributes ≤ 2k walks.

Therefore

#cycles ≥ d^k / (4k)
