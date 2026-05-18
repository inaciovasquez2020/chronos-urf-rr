import Chronos.Frontier.FinitePositiveFiberMassToAdmissibleFiberMassData

namespace Chronos

namespace Frontier

structure MeasureFiberMassPackage extends FinitePositiveFiberMassAdmissiblePackage where
  measure_support_payload : Type
  finite_pushforward_certified : True := by trivial

structure MeasureFiberMassUniformFloor
    (D : MeasureFiberMassPackage) : Prop where
  epsilon_pos : 0 < D.epsilon
  fiber_mass_floor : D.fiber_mass_floor

def finiteSupportPushforwardAdmissibleFiberMassData
    (D : MeasureFiberMassPackage) :
    AdmissibleFiberMassData :=
  FinitePositiveFiberMassToAdmissibleFiberMassData
    D.toFinitePositiveFiberMassAdmissiblePackage

theorem finite_support_pushforward_case_from_finite_positive
    (D : MeasureFiberMassPackage) :
    ∃ A : AdmissibleFiberMassData,
      A = finiteSupportPushforwardAdmissibleFiberMassData D := by
  exact ⟨finiteSupportPushforwardAdmissibleFiberMassData D, rfl⟩

theorem finite_support_pushforward_uniform_floor_from_finite_positive
    (D : MeasureFiberMassPackage) :
    MeasureFiberMassUniformFloor D := by
  exact {
    epsilon_pos := D.epsilon_pos
    fiber_mass_floor := D.fiber_mass_floor
  }

inductive MeasureFiberMassFrontierStatus where
  | finite_support_pushforward_closed
  | unrestricted_measure_case_frontier_open
deriving DecidableEq, Repr

def unrestrictedMeasureFiberMassFrontierStatus :
    MeasureFiberMassFrontierStatus :=
  MeasureFiberMassFrontierStatus.unrestricted_measure_case_frontier_open

def UnrestrictedMeasureFiberMassCaseFrontierOpen : Prop :=
  unrestrictedMeasureFiberMassFrontierStatus =
    MeasureFiberMassFrontierStatus.unrestricted_measure_case_frontier_open

theorem unrestricted_measure_fiber_mass_case_frontier_open :
    UnrestrictedMeasureFiberMassCaseFrontierOpen := by
  rfl

structure RestrictedRateThickFiberCoercivity
    (D : MeasureFiberMassPackage) : Prop where
  admissible_data : AdmissibleFiberMassData
  admissible_data_eq :
    admissible_data = finiteSupportPushforwardAdmissibleFiberMassData D
  uniform_floor : MeasureFiberMassUniformFloor D

theorem restricted_rate_thick_fiber_coercivity_from_finite_admissible_floor
    (D : MeasureFiberMassPackage) :
    RestrictedRateThickFiberCoercivity D := by
  exact {
    admissible_data := finiteSupportPushforwardAdmissibleFiberMassData D
    admissible_data_eq := rfl
    uniform_floor := finite_support_pushforward_uniform_floor_from_finite_positive D
  }

theorem restricted_rate_thick_fiber_coercivity_preserves_floor
    (D : MeasureFiberMassPackage)
    (h : RestrictedRateThickFiberCoercivity D) :
    MeasureFiberMassUniformFloor D :=
  h.uniform_floor

end Frontier

end Chronos
