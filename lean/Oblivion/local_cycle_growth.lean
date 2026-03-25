theorem cycle_sheet_rigidity
  (G : Graph)
  (Δ : ℕ)
  (hdeg : max_degree G ≤ Δ)
  (hFO : FO_k_homogeneous G k R)
  :
  ∀ v, β₁ (ball G v R) ≥ c * R^2
