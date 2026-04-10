# CFI Lift Separation Template (Unbounded Treewidth)

## Construction
Let H_n be a base family with girth(H_n) > 2R and deg ≤ Δ.
Define G_n^+ , G_n^- as 2-lifts of H_n with a single global parity twist.

## Local Property
For fixed k,R:
B_R(G_n^+) ≅ B_R(G_n^-)
⇒ EF_k^R(G_n^+, G_n^-)

## Global Invariant
I_URF(G) := dim_F2( Z1(G) / Z1^{≤2R+1}(G) )

## Separation Claim
I_URF(G_n^+) ≠ I_URF(G_n^-)

## Treewidth Growth
tw(G_n^\pm) → ∞

## Status
Explicit Lean witness + invariant computation required.
