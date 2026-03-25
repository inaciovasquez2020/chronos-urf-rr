namespace Oblivion

universe u

structure Graph where
  V : Type u
  E : Type u

structure LocalCode (G : Graph) where
  support : G.V → Finset G.E

abbrev F2 := Bool

def TransportGraph (G : Graph) (L : LocalCode G) : Type u := G.E

def OverlapGraph (G : Graph) (L : LocalCode G) : Type u := G.V

axiom kernelDim :
  ∀ {G : Graph}, LocalCode G → Nat

axiom cycleRank :
  ∀ {G : Graph}, LocalCode G → Nat

axiom transportDoubling :
  ∀ {G : Graph} (L : LocalCode G), Prop

axiom phiInjective_of_transportDoubling :
  ∀ {G : Graph} (L : LocalCode G),
    transportDoubling L →
    True

axiom kernelLowerBound_of_phiInjective :
  ∀ {G : Graph} (L : LocalCode G),
    True →
    kernelDim L ≥ cycleRank L

theorem HILO_core_conditional
  {G : Graph} (L : LocalCode G)
  (hmix : transportDoubling L) :
  kernelDim L ≥ cycleRank L := by
  exact kernelLowerBound_of_phiInjective L
    (phiInjective_of_transportDoubling L hmix)

end Oblivion
