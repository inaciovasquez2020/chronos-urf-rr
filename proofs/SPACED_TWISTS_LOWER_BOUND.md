# Spaced Twists Lower Bound (URF)

## Statement
Let B_n be a graph with girth > 2R+1.
Let M_n ⊂ E(B_n) be an R-spaced edge set.

Then for the twisted lift G_n^- and trivial lift G_n^+:

I_URF(G_n^-, R) - I_URF(G_n^+, R) ≥ |M_n|.

## Proof Sketch
1. Each e_j ∈ M_n induces a lifted cycle γ_j of length ≥ 2*girth.
2. γ_j ∉ Z1^{≤2R+1} (length bound).
3. Parity map φ_j detects γ_j uniquely.
4. {γ_j} linearly independent in quotient.
5. Therefore dim ≥ |M_n|.
