# EntropyDepth Lower Bound from COR

Assume:

1. COR_R(G) ≥ c·n
2. Algorithm is FO^k-local
3. Information per refinement step ≤ C(k,Δ,R)

Then

ED(F) ≥ H(X)/C(k,Δ,R)

Since H(X)=Θ(n),

ED(F)=Ω(n).

Under patch amplification,

ED(F)=Ω(n log n).
