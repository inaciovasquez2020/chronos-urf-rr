# Support–Separation Realization

Let G be a graph with max degree Δ.

Let C₁,…,C_m be normalized supports with |supp(C_j)| ≤ B.

For each support choose an anchor vertex a_j.

Assume there exists an FO formula α_j(x) such that

G ⊨ α_j(v)  iff  v = a_j.

Define

φ_j(x) := ∃y ( α_j(y) ∧ dist(x,y) ≤ B ).

Then

G ⊨ φ_j(v)  iff  v ∈ supp(C_j).

Define the signature map

σ(v)_j = 1  if  G ⊨ φ_j(v)
σ(v)_j = 0  otherwise.

If σ(u) ≠ σ(v) then some φ_j separates them.

Therefore

tp^k_r(u) ≠ tp^k_r(v).

Hence

|FO^k_r(G)| ≥ |σ(V)|.
