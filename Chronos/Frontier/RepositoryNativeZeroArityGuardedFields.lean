import Chronos.Frontier.RepositoryNativeZeroArityCarrierMigrationTarget

namespace Chronos
namespace Frontier
namespace RepositoryNativeZeroArityGuardedFields

universe u v

/--
Guarded field layer for the eight active-native fields missing from the
repository-native zero-arity interface audit.

This is not an instantiation of active Chronos Carrier/Registry objects.
It only packages the missing fields as explicit obligations.
-/
structure GuardedRepositoryNativeZeroArityFields where
  Carrier : Type u
  Registry : Type v
  arity : Carrier → Nat
  carrierRegistry : Carrier → Registry

  registryGenerates : Registry → Carrier → Prop
  finiteRegistry : Registry → Prop
  representedZeroArityRegistryPair : Carrier → Prop
  isFiniteRepresentedAtom : Carrier → Prop

  carrierRegistryGenerates :
    ∀ z : Carrier,
      registryGenerates (carrierRegistry z) z
  finiteRegistryCarrier :
    ∀ z : Carrier,
      finiteRegistry (carrierRegistry z)
  representedZeroArityOfArityZero :
    ∀ z : Carrier,
      arity z = 0 →
        representedZeroArityRegistryPair z
  finiteRepresentedAtomOfFiniteRegistry :
    ∀ z : Carrier,
      finiteRegistry (carrierRegistry z) →
        isFiniteRepresentedAtom z

def toRepositoryNativeZeroArityInterface
    (G : GuardedRepositoryNativeZeroArityFields) :
    RepositoryNativeZeroArityCarrierMigrationTarget.RepositoryNativeZeroArityInterface where
  Carrier := G.Carrier
  Registry := G.Registry
  arity := G.arity
  carrierRegistry := G.carrierRegistry
  registryGenerates := G.registryGenerates
  finiteRegistry := G.finiteRegistry
  representedZeroArityRegistryPair := G.representedZeroArityRegistryPair
  isFiniteRepresentedAtom := G.isFiniteRepresentedAtom
  carrierRegistryGenerates := G.carrierRegistryGenerates
  finiteRegistryCarrier := G.finiteRegistryCarrier
  representedZeroArityOfArityZero := G.representedZeroArityOfArityZero
  finiteRepresentedAtomOfFiniteRegistry := G.finiteRepresentedAtomOfFiniteRegistry

theorem guarded_fields_imply_zero_arity_carrier_exhaustiveness
    (G : GuardedRepositoryNativeZeroArityFields) :
    ∀ z : G.Carrier,
      G.arity z = 0 →
        G.representedZeroArityRegistryPair z ∧ G.isFiniteRepresentedAtom z := by
  intro z hz
  exact
    RepositoryNativeZeroArityCarrierMigrationTarget.zero_arity_carrier_exhaustiveness_from_repository_native_interface
      (toRepositoryNativeZeroArityInterface G) z hz

def status : String :=
  "FRONTIER_OPEN / GUARDED_INTERFACE_FIELDS_ONLY"

def boundary : String :=
  "Guarded field-obligation layer only; no active Chronos Carrier/Registry instantiation; no unrestricted Chronos-RR closure; no H4.1/FGL closure; no UniversalFiberEntropyGap closure; no P vs NP closure; no Clay-problem closure."

end RepositoryNativeZeroArityGuardedFields
end Frontier
end Chronos
