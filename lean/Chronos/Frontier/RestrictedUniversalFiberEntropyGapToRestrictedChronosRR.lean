import Chronos.Frontier.RestrictedRateThickFiberCoercivityToRestrictedUniversalFiberEntropyGap

namespace Chronos

namespace Frontier

structure RestrictedChronosRRWitness
    (D : MeasureFiberMassPackage) where
  restricted_gap : RestrictedUniversalFiberEntropyGap D
  epsilon : ℝ
  epsilon_pos : 0 < epsilon
  admissible_data : AdmissibleFiberMassData
  admissible_data_eq :
    admissible_data = finiteSupportPushforwardAdmissibleFiberMassData D
  uniform_floor : MeasureFiberMassUniformFloor D
  fiber_mass_floor : ∀ n : ℕ, epsilon ≤ D.data.fiberMass n

def RestrictedUniversalFiberEntropyGapToRestrictedChronosRR
    (D : MeasureFiberMassPackage)
    (h : RestrictedUniversalFiberEntropyGap D) :
    RestrictedChronosRRWitness D :=
  {
    restricted_gap := h
    epsilon := h.epsilon
    epsilon_pos := h.epsilon_pos
    admissible_data := h.admissible_data
    admissible_data_eq := h.admissible_data_eq
    uniform_floor := h.uniform_floor
    fiber_mass_floor := h.fiber_mass_floor
  }

theorem restricted_gap_to_restricted_chronos_rr_closed
    (D : MeasureFiberMassPackage)
    (h : RestrictedUniversalFiberEntropyGap D) :
    ∃ R : RestrictedChronosRRWitness D,
      R = RestrictedUniversalFiberEntropyGapToRestrictedChronosRR D h := by
  exact ⟨RestrictedUniversalFiberEntropyGapToRestrictedChronosRR D h, rfl⟩

theorem restricted_chronos_rr_preserves_gap
    (D : MeasureFiberMassPackage)
    (h : RestrictedUniversalFiberEntropyGap D) :
    (RestrictedUniversalFiberEntropyGapToRestrictedChronosRR D h).restricted_gap = h := by
  rfl

theorem restricted_chronos_rr_preserves_epsilon
    (D : MeasureFiberMassPackage)
    (h : RestrictedUniversalFiberEntropyGap D) :
    (RestrictedUniversalFiberEntropyGapToRestrictedChronosRR D h).epsilon = h.epsilon := by
  rfl

theorem restricted_chronos_rr_preserves_uniform_floor
    (D : MeasureFiberMassPackage)
    (h : RestrictedUniversalFiberEntropyGap D) :
    (RestrictedUniversalFiberEntropyGapToRestrictedChronosRR D h).uniform_floor =
      h.uniform_floor := by
  rfl

inductive RestrictedChronosRRStatus where
  | restricted_chronos_rr_closed
  | unrestricted_chronos_rr_frontier_open
deriving DecidableEq, Repr

def restrictedChronosRRStatus : RestrictedChronosRRStatus :=
  RestrictedChronosRRStatus.restricted_chronos_rr_closed

def unrestrictedChronosRRStatus : RestrictedChronosRRStatus :=
  RestrictedChronosRRStatus.unrestricted_chronos_rr_frontier_open

def UnrestrictedChronosRRFrontierOpen : Prop :=
  unrestrictedChronosRRStatus =
    RestrictedChronosRRStatus.unrestricted_chronos_rr_frontier_open

theorem unrestricted_chronos_rr_frontier_open :
    UnrestrictedChronosRRFrontierOpen := by
  rfl

end Frontier

end Chronos
