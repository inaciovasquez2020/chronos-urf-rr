# EF Game Distinguishability for Bounded Supports

Let C be a support with size ≤ B.

Let a be its anchor vertex.

For any vertex v ∈ C there exists a path of length ≤ B from a to v.

Spoiler strategy:

1. Pebble vertex u ∈ C.
2. Walk along the cycle edges from anchor.
3. Force Duplicator to match adjacency pattern.

If v ∉ C, the bounded cycle neighborhood cannot be matched.

Thus

tp^k_r(u) ≠ tp^k_r(v).
