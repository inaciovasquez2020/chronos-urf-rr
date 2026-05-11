namespace Chronos
namespace Frontier
namespace RepositoryNativeZeroArityCarrierMigrationTarget

universe u v

/--
Repository-native migration interface.

This removes dependence on the prior local toy model and isolates the
exact native obligations needed to derive zero-arity carrier exhaustiveness.
-/
structure RepositoryNativeZeroArityInterface where
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

theorem zero_arity_carrier_exhaustiveness_from_repository_native_interface
    (I : RepositoryNativeZeroArityInterface) :
    ∀ z : I.Carrier,
      I.arity z = 0 →
        I.representedZeroArityRegistryPair z ∧ I.isFiniteRepresentedAtom z := by
  intro z hz
  exact ⟨
    I.representedZeroArityOfArityZero z hz,
    I.finiteRepresentedAtomOfFiniteRegistry z (I.finiteRegistryCarrier z)
  ⟩

def status : String :=
  "FRONTIER_OPEN / REPOSITORY_NATIVE_INTERFACE_REDUCTION_ONLY"

def boundary : String :=
  "Repository-native interface reduction only; no proof that Chronos repository-native Carrier and Registry satisfy the interface; no unrestricted Chronos-RR closure; no H4.1/FGL closure; no UniversalFiberEntropyGap closure; no P vs NP closure; no Clay-problem closure."

end RepositoryNativeZeroArityCarrierMigrationTarget
end Frontier
end Chronos
