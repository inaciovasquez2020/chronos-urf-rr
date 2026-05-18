import Chronos.Frontier.UniversalWeakestMissingMeasureFiberMassLemmaRefutation

/-!
Admissible replacement for the refuted unrestricted measure/fiber-mass floor.

PR #362 refuted the unrestricted statement over arbitrary `FiberMassData`.
This file closes the admissible replacement by packaging the uniform floor
as structure-level data and rebuilding the rate-thick coercivity target over
that admissible class only.
-/

namespace Chronos.Frontier

structure AdmissibleFiberMassData where
  data : FiberMassData
  epsilon : ℝ
  epsilon_pos : 0 < epsilon
  fiber_mass_floor : ∀ n : ℕ, epsilon ≤ data.fiberMass n

def AdmissibleFiberMassUniformFloor
    (A : AdmissibleFiberMassData) : Prop :=
  FiberMassUniformFloor A.data

theorem AdmissibleFiberMassUniformFloor_solved
    (A : AdmissibleFiberMassData) :
    AdmissibleFiberMassUniformFloor A := by
  exact ⟨A.epsilon, A.epsilon_pos, A.fiber_mass_floor⟩

def AdmissibleRateThickFiberCoercivityTarget : Prop :=
  ∀ A : AdmissibleFiberMassData,
    Nonempty (RateThickFiberCoercivityTarget A.data)

theorem AdmissibleRateThickFiberCoercivityTarget_solved :
    AdmissibleRateThickFiberCoercivityTarget := by
  intro A
  exact exact_coercivity_target_from_measure_fiber_mass_floor
    A.data order_surface_available_solved
    (AdmissibleFiberMassUniformFloor_solved A)

def constantOneFiberMassData : FiberMassData where
  fiberMass := fun _ => 1

def constantOneAdmissibleFiberMassData : AdmissibleFiberMassData where
  data := constantOneFiberMassData
  epsilon := 1
  epsilon_pos := by norm_num
  fiber_mass_floor := by
    intro n
    simp [constantOneFiberMassData]

theorem AdmissibleFiberMassData_nonempty :
    Nonempty AdmissibleFiberMassData := by
  exact ⟨constantOneAdmissibleFiberMassData⟩

end Chronos.Frontier
