import Chronos.Frontier.FinitePositiveFiberMassUniformFloor

namespace Chronos

namespace Frontier

structure FinitePositiveFiberMassAdmissiblePackage extends AdmissibleFiberMassData where
  finite_positive_payload : True := by trivial

def FinitePositiveFiberMassToAdmissibleFiberMassData
    (D : FinitePositiveFiberMassAdmissiblePackage) :
    AdmissibleFiberMassData :=
  D.toAdmissibleFiberMassData

theorem finite_positive_fiber_mass_to_admissible_fiber_mass_data_closed
    (D : FinitePositiveFiberMassAdmissiblePackage) :
    ∃ A : AdmissibleFiberMassData,
      A = FinitePositiveFiberMassToAdmissibleFiberMassData D := by
  exact ⟨FinitePositiveFiberMassToAdmissibleFiberMassData D, rfl⟩

theorem finite_positive_fiber_mass_to_admissible_fiber_mass_data_preserves_epsilon
    (D : FinitePositiveFiberMassAdmissiblePackage) :
    (FinitePositiveFiberMassToAdmissibleFiberMassData D).epsilon = D.epsilon := by
  rfl

theorem finite_positive_fiber_mass_to_admissible_fiber_mass_data_preserves_floor
    (D : FinitePositiveFiberMassAdmissiblePackage) :
    (FinitePositiveFiberMassToAdmissibleFiberMassData D).fiber_mass_floor =
      D.fiber_mass_floor := by
  rfl

end Frontier

end Chronos
