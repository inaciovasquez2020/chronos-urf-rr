import Chronos.Frontier.TemporalRelaxationWaveInterface

namespace Chronos
namespace Frontier

def LyapunovDecayCertificate
    (State : Type)
    (evolve : State → ℝ → State)
    (Energy : State → ℝ)
    (D : State) : Prop :=
  ∃ rate : ℝ,
    0 < rate ∧
    ∀ t : ℝ,
      0 ≤ t →
        Energy (evolve D t) ≤ Energy D * Real.exp (-rate * t)

def UniformLyapunovDecayCertificate
    (State : Type)
    (evolve : State → ℝ → State)
    (Energy : State → ℝ) : Prop :=
  ∃ lam : ℝ,
    0 < lam ∧
    ∀ D : State,
      ∀ t : ℝ,
        0 ≤ t →
          Energy (evolve D t) ≤ Energy D * Real.exp (-lam * t)

theorem lyapunovDecay_from_temporalRelaxationWave
    {State : Type}
    {evolve : State → ℝ → State}
    {Energy : State → ℝ}
    {D : State}
    (h : TemporalRelaxationWave State evolve Energy D) :
    LyapunovDecayCertificate State evolve Energy D := by
  exact h

theorem uniformLyapunovDecay_from_uniformTemporalRelaxationWave
    {State : Type}
    {evolve : State → ℝ → State}
    {Energy : State → ℝ}
    (h : UniformTemporalRelaxationWave State evolve Energy) :
    UniformLyapunovDecayCertificate State evolve Energy := by
  exact h

end Frontier
end Chronos
