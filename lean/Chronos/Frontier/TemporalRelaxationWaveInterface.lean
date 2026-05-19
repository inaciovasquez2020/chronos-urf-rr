import Mathlib

namespace Chronos
namespace Frontier

def TemporalRelaxationWave
    (State : Type)
    (evolve : State → ℝ → State)
    (Energy : State → ℝ)
    (D : State) : Prop :=
  ∃ rate : ℝ,
    0 < rate ∧
    ∀ t : ℝ,
      0 ≤ t →
        Energy (evolve D t) ≤ Energy D * Real.exp (-rate * t)

def UniformTemporalRelaxationWave
    (State : Type)
    (evolve : State → ℝ → State)
    (Energy : State → ℝ) : Prop :=
  ∃ lam : ℝ,
    0 < lam ∧
    ∀ D : State,
      ∀ t : ℝ,
        0 ≤ t →
          Energy (evolve D t) ≤ Energy D * Real.exp (-lam * t)

theorem temporalRelaxationWave_from_uniformDecay
    {State : Type}
    {evolve : State → ℝ → State}
    {Energy : State → ℝ}
    (h : UniformTemporalRelaxationWave State evolve Energy) :
    ∀ D : State,
      TemporalRelaxationWave State evolve Energy D := by
  rcases h with ⟨lam, hlam, hdecay⟩
  intro D
  exact ⟨lam, hlam, hdecay D⟩

def trivialEvolve (x : Unit) (_t : ℝ) : Unit := x

def zeroEnergy (_x : Unit) : ℝ := 0

theorem unit_uniformTemporalRelaxationWave :
    UniformTemporalRelaxationWave Unit trivialEvolve zeroEnergy := by
  refine ⟨1, by norm_num, ?_⟩
  intro D t ht
  simp [zeroEnergy]

example :
    ∀ D : Unit,
      TemporalRelaxationWave Unit trivialEvolve zeroEnergy D :=
  temporalRelaxationWave_from_uniformDecay unit_uniformTemporalRelaxationWave

end Frontier
end Chronos
