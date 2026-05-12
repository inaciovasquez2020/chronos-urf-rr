import Chronos.Frontier.RepositoryNativeFiniteRegistryInstantiation

namespace Chronos.Frontier

/--
Repository-native instantiation of the guarded field
`representedZeroArityRegistryPair`.

This binds only zero-arity carriers to their active-native registry witness.
It does not assert finite represented atoms, carrier-registry generation,
or any downstream closure theorem.
-/
def representedZeroArityRegistryPair (z : Carrier) : Prop :=
  z.arity = 0 ∧
  registryGenerates (carrierRegistry z) z ∧
  finiteRegistry (carrierRegistry z)

theorem representedZeroArityRegistryPair_of_arity_zero
    (z : Carrier)
    (hz : z.arity = 0) :
    representedZeroArityRegistryPair z := by
  exact ⟨hz, registryGenerates_of_carrierRegistry z, finiteRegistry_of_carrierRegistry z⟩

end Chronos.Frontier
