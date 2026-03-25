# Random Lift Cycle Independence

Let H be a base graph containing a cycle.

Let G_n be an n-lift of H.

Each base cycle lifts to n cycles.

Claim.

A linear subset of these lifted cycles are linearly independent in Z_1(G_n).

Reason.

Lifted cycles share only bounded overlap regions.

Thus symmetric-difference dependencies cannot eliminate more than O(1) per overlap cluster.

Therefore

COR_R(G_n) ≥ c(H,R)·n.
