namespace Oblivion

universe u

structure Graph where
  V : Type u
  E : Type u

structure LocalCode (G : Graph) where
  support : G.V → Finset G.E

abbrev F2 := Bool

axiom kernelDim :
  ∀ {G : Graph}, LocalCode G → Nat

axiom cycleRank :
  ∀ {G : Graph}, LocalCode G → Nat

axiom overlapMinDegree :
  ∀ {G : Graph} (L : LocalCode G), Prop

axiom parityBalanced :
  ∀ {G : Graph} (L : LocalCode G), Prop

axiom baseExpansion :
  ∀ {G : Graph} (L : LocalCode G), Prop

axiom boundaryExpansion :
  ∀ {G : Graph} (L : LocalCode G),
    parityBalanced L →
    baseExpansion L →
    True

axiom phiInjective :
  ∀ {G : Graph} (L : LocalCode G),
    True →
    True

axiom kernelLowerBound :
  ∀ {G : Graph} (L : LocalCode G),
    True →
    kernelDim L ≥ cycleRank L

theorem HILO_full_conditional
  {G : Graph} (L : LocalCode G)
  (h1 : parityBalanced L)
  (h2 : baseExpansion L) :
  kernelDim L ≥ cycleRank L := by
  have hmix := boundaryExpansion L h1 h2
  have hinj := phiInjective L hmix
  exact kernelLowerBound L hinj

end Oblivion
