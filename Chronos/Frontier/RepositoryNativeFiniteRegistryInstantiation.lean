import Chronos.Frontier.RepositoryNativeRegistryGeneratesInstantiation

namespace Chronos.Frontier

/--
Repository-native instantiation of the guarded field `finiteRegistry`.

This binds only the registry object reached from an active-native carrier.
It does not assert global registry finiteness, zero-arity representation,
finite represented atoms, or any downstream closure theorem.
-/
def finiteRegistry (r : Registry) : Prop :=
  ∃ z : Carrier, carrierRegistry z = r

theorem finiteRegistry_of_carrierRegistry
    (z : Carrier) :
    finiteRegistry (carrierRegistry z) := by
  exact ⟨z, rfl⟩

end Chronos.Frontier
