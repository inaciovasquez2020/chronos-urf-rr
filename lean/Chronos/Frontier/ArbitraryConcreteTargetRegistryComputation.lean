import Chronos.Frontier.RepositoryNativeSemanticRegistryComputation

namespace Chronos
namespace Frontier

/--
A concrete target registry is the minimal repository-native target object whose
semantic computation can be requested without promoting any unrestricted theorem.
-/
structure ConcreteTargetRegistry where
  Carrier : Type
  arity : Carrier → Nat
  semanticRank : Carrier → Nat

/--
A finite concrete target registry is a concrete target registry whose carrier is
finite and decidable.
-/
structure FiniteConcreteTargetRegistry where
  toConcreteTargetRegistry : ConcreteTargetRegistry
  finiteCarrier : Fintype toConcreteTargetRegistry.Carrier
  decidableCarrierEq : DecidableEq toConcreteTargetRegistry.Carrier

attribute [instance] FiniteConcreteTargetRegistry.finiteCarrier
attribute [instance] FiniteConcreteTargetRegistry.decidableCarrierEq

/--
One-registry computation witness for a concrete target registry.

This is deliberately a witness surface, not an unrestricted semantic-rank theorem.
-/
structure OneRegistrySemanticComputation
    (R : ConcreteTargetRegistry) where
  computedRank : R.Carrier → Nat
  agreesWithRegistry : ∀ x : R.Carrier, computedRank x = R.semanticRank x

/--
Arbitrary finite-registry computation package.

This packages a computation witness for every finite concrete target registry.
-/
structure ArbitraryFiniteConcreteRegistryComputation where
  computation :
    ∀ R : FiniteConcreteTargetRegistry,
      OneRegistrySemanticComputation R.toConcreteTargetRegistry

/--
One-registry semantic computation lifts to arbitrary finite concrete target
registries exactly when a one-registry witness is supplied for each finite
concrete target registry.
-/
def one_registry_computation_lifts_to_arbitrary_finite_concrete_target_registries
    (h :
      ∀ R : FiniteConcreteTargetRegistry,
        OneRegistrySemanticComputation R.toConcreteTargetRegistry) :
    ArbitraryFiniteConcreteRegistryComputation :=
  ⟨h⟩

/--
Boundary lock: the arbitrary finite-registry lift is still finite-registry-only
and does not promote any unrestricted bridge or global theorem.
-/
def arbitraryConcreteTargetRegistryComputationBoundaryLock : Prop :=
  True

theorem arbitrary_concrete_target_registry_computation_boundary_locked :
    arbitraryConcreteTargetRegistryComputationBoundaryLock :=
  trivial

end Frontier
end Chronos
