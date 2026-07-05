import Chronos.Frontier.ConcreteNativeBindingSpec
import Chronos.Frontier.R1R2R3IsolatedTargetsConditionalClosure

namespace Chronos
namespace Frontier

def NonFactorisationConcreteObject : Type :=
  Prop

def NonFactorisationConcreteFactorisation
    (P : NonFactorisationConcreteObject) : Prop :=
  ¬ P

def NonFactorisationConcreteAdmissibleObject :
    NonFactorisationConcreteObject :=
  RepositoryNativeNonFactorisationPromotionAllowed concreteNativeBindingSpec

theorem non_factorisation_concrete_non_factorisation :
    ¬ NonFactorisationConcreteFactorisation
        NonFactorisationConcreteAdmissibleObject := by
  intro hFactorisation
  exact hFactorisation concrete_native_nonfactorisation_promotion_allowed

def NonFactorisationConcreteInputSurface :
    NonFactorisationInputSurface :=
  NonFactorisationInputSurface.mk
    NonFactorisationConcreteObject
    NonFactorisationConcreteFactorisation
    NonFactorisationConcreteAdmissibleObject
    non_factorisation_concrete_non_factorisation

end Frontier
end Chronos
