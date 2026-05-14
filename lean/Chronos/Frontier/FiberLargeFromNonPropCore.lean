namespace Chronos
namespace Frontier
namespace FiberLargeFromNonPropCore

structure CarrierData where
  arity : Nat
  stratum : Rat
deriving DecidableEq, Repr

structure FiberWitness where
  carrierId : Nat
  fiberSize : Nat
  rankMass : Nat
  entropyMass : Rat
deriving DecidableEq, Repr

structure NonPropFinalCarrierInvariant where
  rank : CarrierData → Nat
  fiberSize : CarrierData → Nat
  entropyMass : CarrierData → Rat
  arity : CarrierData → Nat
  stratum : CarrierData → Rat

  rank_positive :
    ∀ c : CarrierData, 0 < rank c

  fiber_large_from_rank :
    ∀ c : CarrierData, rank c ≤ fiberSize c

  entropy_mass_lower :
    ∀ c : CarrierData, (rank c : Rat) ≤ entropyMass c

  arity_agrees :
    ∀ c : CarrierData, arity c = c.arity

  stratum_agrees :
    ∀ c : CarrierData, stratum c = c.stratum

def FiberLargeExistsFromNonProp
    (I : NonPropFinalCarrierInvariant) : Prop :=
  ∀ c : CarrierData,
    ∃ w : FiberWitness,
      w.carrierId = c.arity ∧
      w.rankMass = I.rank c ∧
      w.fiberSize = I.fiberSize c ∧
      0 < w.rankMass ∧
      w.rankMass ≤ w.fiberSize ∧
      (w.rankMass : Rat) ≤ w.entropyMass

theorem fiberLargeExists_from_nonprop_invariant
    (I : NonPropFinalCarrierInvariant) :
    FiberLargeExistsFromNonProp I := by
  intro c
  refine ⟨
    {
      carrierId := c.arity,
      fiberSize := I.fiberSize c,
      rankMass := I.rank c,
      entropyMass := I.entropyMass c
    },
    ?_
  ⟩
  exact ⟨
    rfl,
    rfl,
    rfl,
    I.rank_positive c,
    I.fiber_large_from_rank c,
    I.entropy_mass_lower c
  ⟩

def FrontierStatus : String :=
  "LAKE_NATIVE_FIBER_LARGE_FROM_NONPROP_CORE_CLOSED"

def Boundary : String :=
  "Lake-native core theorem only; does not migrate root Chronos/Frontier tree; no UniversalFiberEntropyGap, Chronos-RR, H4.1/FGL, P vs NP, or Clay closure"

end FiberLargeFromNonPropCore
end Frontier
end Chronos
