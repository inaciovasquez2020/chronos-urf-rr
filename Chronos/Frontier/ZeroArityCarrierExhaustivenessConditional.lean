namespace Chronos
namespace Frontier
namespace ZeroArityCarrierExhaustivenessConditional

structure CarrierData where
  arity : Nat
  tag : String
deriving Repr, DecidableEq

inductive Registry where
  | carrier : CarrierData → Registry
deriving Repr

def RegistryGenerates : Registry → CarrierData → Prop
  | Registry.carrier z, z' => z = z'

def FiniteRegistry : Registry → Prop
  | Registry.carrier _ => True

def RepresentedZeroArityRegistryPair (z : CarrierData) : Prop :=
  z.arity = 0

def IsFiniteRepresentedAtom (z : CarrierData) : Prop :=
  FiniteRegistry (Registry.carrier z)

theorem represented_zero_arity_registry_pair_of_arity_zero :
    ∀ z : CarrierData,
      z.arity = 0 →
        RepresentedZeroArityRegistryPair z :=
  fun _ hz => hz

theorem finite_registry_carrier :
    ∀ z : CarrierData,
      FiniteRegistry (Registry.carrier z) := by
  intro z
  trivial

theorem finite_represented_atom_of_finite_registry :
    ∀ z : CarrierData,
      FiniteRegistry (Registry.carrier z) →
        IsFiniteRepresentedAtom z :=
  fun _ hfin => hfin

theorem CarrierRegistryGeneration :
    ∀ z : CarrierData, ∃ r : Registry, RegistryGenerates r z := by
  intro z
  exact ⟨Registry.carrier z, rfl⟩

theorem ZeroArityRegistryRepresentation :
    ∀ z r,
      RegistryGenerates r z →
      z.arity = 0 →
        RepresentedZeroArityRegistryPair z := by
  intro z r hgen hz
  cases r with
  | carrier z₀ =>
      cases hgen
      exact represented_zero_arity_registry_pair_of_arity_zero z₀ hz

theorem RegistryGeneratedAtomsFinite :
    ∀ z r,
      RegistryGenerates r z →
      FiniteRegistry r →
        IsFiniteRepresentedAtom z := by
  intro z r hgen hfin
  cases r with
  | carrier z₀ =>
      cases hgen
      exact finite_represented_atom_of_finite_registry z₀ hfin

theorem ZeroArityCarrierExhaustiveness :
    ∀ z : CarrierData,
      z.arity = 0 →
        RepresentedZeroArityRegistryPair z ∧ IsFiniteRepresentedAtom z := by
  intro z hz
  obtain ⟨r, hgen⟩ := CarrierRegistryGeneration z
  exact ⟨
    ZeroArityRegistryRepresentation z r hgen hz,
    RegistryGeneratedAtomsFinite z r hgen (by
      cases r with
      | carrier z₀ =>
          exact finite_registry_carrier z₀)
  ⟩

def boundary : String :=
  "CONDITIONAL_SURFACE_ONLY: local CarrierData model; no unrestricted Chronos-RR closure; no H4.1/FGL closure; no P vs NP closure; no Clay-problem closure."

end ZeroArityCarrierExhaustivenessConditional
end Frontier
end Chronos
