# Cross-Incidence Rank Lemma — Correction + Valid Statement

## Correction (invalid counterexample)
The previously claimed rank(A)=0 construction for a balanced partition on a bipartite expander is incorrect.

In the proposed bipartite expander construction with R = R1 ⊔ R2,
X = edges incident to R2 and Y = edges incident to R1,
for every X-edge e = {ℓ, r2} with r2 ∈ R2, ℓ ∈ L:

A[r2, e] = 1  ⇔  ℓ is incident to some Y-edge  ⇔  N(ℓ) ∩ R1 ≠ ∅.

In any d-regular bipartite expander with |R1| = |R2| = n/4,
expansion forces |{ℓ ∈ L : N(ℓ) ∩ R1 = ∅}| = o(n),
so A has Ω(n) nonzero distinct standard-basis rows on R2 and hence rank_F2(A)=Ω(n).

Therefore the asserted rank(A)=0 counterexample does not exist under the expander hypothesis.

## Valid theorem (rank lower bound)
Let G=(V,E) be a connected d-regular graph on n vertices with edge expansion h(G) ≥ ε > 0.
Let E = X ⊔ Y with |X|,|Y| ≥ c|E| for fixed c>0.

Let S := { v ∈ V : deg_Y(v) > 0 }.
Define A ∈ F2^{V×X} by A[v,e]=1 iff e={v,u} and u∈S.

Then rank_F2(A) = Ω(n). In particular, one can take

rank_F2(A) ≥ (ε c / (4d)) · n.
