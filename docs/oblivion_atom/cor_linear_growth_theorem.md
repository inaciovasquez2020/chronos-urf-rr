# COR Linear Growth Theorem

Let H be a finite connected base graph containing at least one cycle.

Let G_n be a random n-lift of H.

Then with high probability:

COR_R(G_n) = Ω(n)

Reason.

Each lift of a base cycle produces n edge-disjoint lifts.

Because lifts share only bounded-radius overlaps, at least a linear number remain independent.

Thus the cycle-overlap rank grows linearly with the lift size.

Formally:

∃ c(H,R) > 0 such that

COR_R(G_n) ≥ c(H,R) · n
