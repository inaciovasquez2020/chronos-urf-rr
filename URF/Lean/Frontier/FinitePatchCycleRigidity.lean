namespace URF

universe u

/-- Abstract graph carrier for the frontier statement. -/
constant Graph : Type u

/-- Maximum degree bound. -/
constant DegLe : Graph → Nat → Prop

/-- FO^k-homogeneity at radius R. -/
constant FOHomogeneous : Nat → Nat → Graph → Prop

/-- Global cycle quotient dimension dim_F2(Z₁(G) / Z₁^{≤R}(G)). -/
constant CycleQuotientDim : Nat → Graph → Nat

/--
Finite-Patch Cycle Rigidity frontier statement:
for fixed k,Δ there exist R,B bounding the nonlocal cycle quotient dimension.
-/
axiom finitePatchCycleRigidity
  (k Δ : Nat) :
  ∃ R B : Nat, ∀ G : Graph,
    DegLe G Δ →
    FOHomogeneous k R G →
    CycleQuotientDim R G ≤ B

end URF
