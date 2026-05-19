import Chronos.Frontier.TemporalRelaxationWaveLyapunovBridge

namespace Chronos
namespace Frontier

def PointwiseEnergyBoundCertificate
    (State : Type)
    (evolve : State → ℝ → State)
    (Energy : State → ℝ)
    (D : State) : Prop :=
  ∃ rate : ℝ,
    0 < rate ∧
    ∀ t : ℝ,
      0 ≤ t →
        Energy (evolve D t) ≤ Energy D * Real.exp (-rate * t)

def UniformEnergyBoundCertificate
    (State : Type)
    (evolve : State → ℝ → State)
    (Energy : State → ℝ) : Prop :=
  ∃ lam : ℝ,
    0 < lam ∧
    ∀ D : State,
      ∀ t : ℝ,
        0 ≤ t →
          Energy (evolve D t) ≤ Energy D * Real.exp (-lam * t)

def EntropyControlCertificate
    (State : Type)
    (evolve : State → ℝ → State)
    (Entropy : State → ℝ)
    (D : State) : Prop :=
  ∃ rate : ℝ,
    0 < rate ∧
    ∀ t : ℝ,
      0 ≤ t →
        Entropy (evolve D t) ≤ Entropy D * Real.exp (-rate * t)

def UniformEntropyControlCertificate
    (State : Type)
    (evolve : State → ℝ → State)
    (Entropy : State → ℝ) : Prop :=
  ∃ lam : ℝ,
    0 < lam ∧
    ∀ D : State,
      ∀ t : ℝ,
        0 ≤ t →
          Entropy (evolve D t) ≤ Entropy D * Real.exp (-lam * t)

theorem energyBound_from_lyapunovDecay
    {State : Type}
    {evolve : State → ℝ → State}
    {Energy : State → ℝ}
    {D : State}
    (h : LyapunovDecayCertificate State evolve Energy D) :
    PointwiseEnergyBoundCertificate State evolve Energy D := by
  exact h

theorem uniformEnergyBound_from_uniformLyapunovDecay
    {State : Type}
    {evolve : State → ℝ → State}
    {Energy : State → ℝ}
    (h : UniformLyapunovDecayCertificate State evolve Energy) :
    UniformEnergyBoundCertificate State evolve Energy := by
  exact h

theorem entropyControl_from_lyapunovDecay_sameFunctional
    {State : Type}
    {evolve : State → ℝ → State}
    {Entropy : State → ℝ}
    {D : State}
    (h : LyapunovDecayCertificate State evolve Entropy D) :
    EntropyControlCertificate State evolve Entropy D := by
  exact h

theorem uniformEntropyControl_from_uniformLyapunovDecay_sameFunctional
    {State : Type}
    {evolve : State → ℝ → State}
    {Entropy : State → ℝ}
    (h : UniformLyapunovDecayCertificate State evolve Entropy) :
    UniformEntropyControlCertificate State evolve Entropy := by
  exact h

end Frontier
end Chronos
