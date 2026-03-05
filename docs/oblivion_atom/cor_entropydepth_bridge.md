# COR → EntropyDepth Bridge

Assume:

1. COR_R(G) ≥ c n
2. FO^k locality restriction
3. Information gain per refinement step ≤ C(k,Δ,R)

Then refinement depth satisfies

ED(F) ≥ H(X) / C(k,Δ,R)

Since H(X)=Θ(n),

ED(F)=Ω(n)

Under patch-rank amplification:

ED(F)=Ω(n log n)
