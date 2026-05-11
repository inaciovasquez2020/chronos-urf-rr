import Chronos.Frontier.RepositoryNativeZeroArityGuardedFields
import Chronos.Frontier.IntendedChronosAdmissibility

namespace Chronos.Frontier

/--
Repository-native instantiation of the guarded field `registryGenerates`.

This is intentionally only the first guarded-field binding:
it does not instantiate finite registries, represented zero-arity pairs,
finite represented atoms, or any downstream closure theorem.
-/
def registryGenerates (r : Registry) (z : Carrier) : Prop :=
  carrierRegistry z = r

theorem registryGenerates_of_carrierRegistry
    (z : Carrier) :
    registryGenerates (carrierRegistry z) z := by
  rfl

end Chronos.Frontier
