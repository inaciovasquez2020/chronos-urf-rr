import Chronos.Frontier.RepositoryNativeRepresentedZeroArityRegistryPairInstantiation

namespace Chronos.Frontier

/--
Repository-native instantiation of the guarded field `isFiniteRepresentedAtom`.

This binds only carriers already witnessed as represented zero-arity registry pairs.
-/
def isFiniteRepresentedAtom (z : Carrier) : Prop :=
  representedZeroArityRegistryPair z

theorem isFiniteRepresentedAtom_of_representedZeroArityRegistryPair
    (z : Carrier)
    (hz : representedZeroArityRegistryPair z) :
    isFiniteRepresentedAtom z := by
  exact hz

theorem isFiniteRepresentedAtom_of_arity_zero
    (z : Carrier)
    (hz : z.arity = 0) :
    isFiniteRepresentedAtom z := by
  exact representedZeroArityRegistryPair_of_arity_zero z hz

end Chronos.Frontier
