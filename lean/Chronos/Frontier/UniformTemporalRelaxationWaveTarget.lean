namespace Chronos
namespace Frontier

structure TemporalRelaxationWaveData where
  Carrier : Type
  step : Carrier → Carrier
  sink : Carrier
  entropy : Carrier → Nat
  mass : Carrier → Nat

structure UniformTemporalRelaxationWave
    (D : TemporalRelaxationWaveData) : Prop where
  entropy_nonincrease :
    ∀ x : D.Carrier, D.entropy (D.step x) ≤ D.entropy x
  sink_fixed :
    D.step D.sink = D.sink
  positive_mass_floor :
    ∃ n : Nat, n ≠ 0 ∧ ∀ x : D.Carrier, n ≤ D.mass x

def UniformTemporalRelaxationWaveExistenceTarget : Prop :=
  ∀ D : TemporalRelaxationWaveData, UniformTemporalRelaxationWave D

theorem uniformTemporalRelaxationWave_from_input
    (h : UniformTemporalRelaxationWaveExistenceTarget) :
    UniformTemporalRelaxationWaveExistenceTarget :=
  h

def uniformTemporalRelaxationWave_frontier_open_marker : String :=
  "FRONTIER_OPEN: UniformTemporalRelaxationWave existence is not proved"

end Frontier
end Chronos
