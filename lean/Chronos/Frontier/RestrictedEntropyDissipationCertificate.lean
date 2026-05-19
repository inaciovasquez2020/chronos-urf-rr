import Chronos.Frontier.LyapunovDecayEnergyControl

namespace Chronos
namespace Frontier

def RestrictedEntropyDissipationCertificate
    (State : Type)
    (evolve : State → ℝ → State)
    (Entropy : State → ℝ)
    (Admissible : State → Prop) : Prop :=
  ∃ lam : ℝ,
    0 < lam ∧
    ∀ D : State,
      Admissible D →
      ∀ t : ℝ,
        0 ≤ t →
          Entropy (evolve D t) ≤ Entropy D * Real.exp (-lam * t)

theorem restrictedEntropyDissipation_from_uniformEntropyControl
    {State : Type}
    {evolve : State → ℝ → State}
    {Entropy : State → ℝ}
    {Admissible : State → Prop}
    (h : UniformEntropyControlCertificate State evolve Entropy) :
    RestrictedEntropyDissipationCertificate State evolve Entropy Admissible := by
  rcases h with ⟨lam, hlam, hdecay⟩
  exact
    ⟨lam, hlam, by
      intro D hD t ht
      exact hdecay D t ht⟩

theorem restrictedEntropyDissipation_from_uniformLyapunovDecay_sameFunctional
    {State : Type}
    {evolve : State → ℝ → State}
    {Entropy : State → ℝ}
    {Admissible : State → Prop}
    (h : UniformLyapunovDecayCertificate State evolve Entropy) :
    RestrictedEntropyDissipationCertificate State evolve Entropy Admissible := by
  exact
    restrictedEntropyDissipation_from_uniformEntropyControl
      (uniformEntropyControl_from_uniformLyapunovDecay_sameFunctional h)

end Frontier
end Chronos
