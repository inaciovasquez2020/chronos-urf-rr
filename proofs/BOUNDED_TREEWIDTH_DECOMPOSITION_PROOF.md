# Bounded Treewidth ⇒ Decomposition Property

## Statement
For fixed treewidth t and radius R, there exists C(t,R) such that
dim(Z₁(G)/Z₁^{≤ 2R+1}(G)) ≤ C(t,R).

## Proof Sketch
Use tree decomposition (bags of size ≤ t+1).

1. Every cycle decomposes into cycles supported on bags + boundary corrections.
2. Each bag induces subgraph of size O(t), so local cycle space bounded.
3. Gluing along tree introduces at most O(t) independent residual cycles per separator.
4. Total residual dimension bounded by function of (t,R), independent of |V(G)|.

## Status
Sketch (requires formalization).
