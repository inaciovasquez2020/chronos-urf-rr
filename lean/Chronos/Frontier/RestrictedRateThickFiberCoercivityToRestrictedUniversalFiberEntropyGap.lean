import Chronos.Frontier.MeasureFiberMassPackage

namespace Chronos

namespace Frontier

structure RestrictedUniversalFiberEntropyGap
    (D : MeasureFiberMassPackage) where
  epsilon : ℝ
  epsilon_pos : 0 < epsilon
  admissible_data : AdmissibleFiberMassData
  admissible_data_eq :
    admissible_data = finiteSupportPushforwardAdmissibleFiberMassData D
  uniform_floor : MeasureFiberMassUniformFloor D
  fiber_mass_floor : ∀ n : ℕ, epsilon ≤ D.data.fiberMass n

def RestrictedRateThickFiberCoercivityToRestrictedUniversalFiberEntropyGap
    (D : MeasureFiberMassPackage)
    (h : RestrictedRateThickFiberCoercivity D) :
    RestrictedUniversalFiberEntropyGap D :=
  {
    epsilon := D.epsilon
    epsilon_pos := h.uniform_floor.epsilon_pos
    admissible_data := h.admissible_data
    admissible_data_eq := h.admissible_data_eq
    uniform_floor := h.uniform_floor
    fiber_mass_floor := h.uniform_floor.fiber_mass_floor
  }

theorem restricted_rate_thick_coercivity_to_restricted_gap_closed
    (D : MeasureFiberMassPackage)
    (h : RestrictedRateThickFiberCoercivity D) :
    ∃ G : RestrictedUniversalFiberEntropyGap D,
      G =
        RestrictedRateThickFiberCoercivityToRestrictedUniversalFiberEntropyGap
          D h := by
  exact
    ⟨RestrictedRateThickFiberCoercivityToRestrictedUniversalFiberEntropyGap D h,
      rfl⟩

theorem restricted_gap_preserves_epsilon
    (D : MeasureFiberMassPackage)
    (h : RestrictedRateThickFiberCoercivity D) :
    (RestrictedRateThickFiberCoercivityToRestrictedUniversalFiberEntropyGap
      D h).epsilon = D.epsilon := by
  rfl

theorem restricted_gap_preserves_admissible_data
    (D : MeasureFiberMassPackage)
    (h : RestrictedRateThickFiberCoercivity D) :
    (RestrictedRateThickFiberCoercivityToRestrictedUniversalFiberEntropyGap
      D h).admissible_data = h.admissible_data := by
  rfl

theorem restricted_gap_preserves_uniform_floor
    (D : MeasureFiberMassPackage)
    (h : RestrictedRateThickFiberCoercivity D) :
    (RestrictedRateThickFiberCoercivityToRestrictedUniversalFiberEntropyGap
      D h).uniform_floor = h.uniform_floor := by
  rfl

inductive RestrictedUniversalFiberEntropyGapStatus where
  | restricted_gap_closed
  | unrestricted_gap_frontier_open
deriving DecidableEq, Repr

def restrictedUniversalFiberEntropyGapStatus :
    RestrictedUniversalFiberEntropyGapStatus :=
  RestrictedUniversalFiberEntropyGapStatus.restricted_gap_closed

def unrestrictedUniversalFiberEntropyGapStatus :
    RestrictedUniversalFiberEntropyGapStatus :=
  RestrictedUniversalFiberEntropyGapStatus.unrestricted_gap_frontier_open

def UnrestrictedUniversalFiberEntropyGapFrontierOpen : Prop :=
  unrestrictedUniversalFiberEntropyGapStatus =
    RestrictedUniversalFiberEntropyGapStatus.unrestricted_gap_frontier_open

theorem unrestricted_universal_fiber_entropy_gap_frontier_open :
    UnrestrictedUniversalFiberEntropyGapFrontierOpen := by
  rfl

end Frontier

end Chronos
