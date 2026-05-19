import Chronos.Frontier.RestrictedEntropyDissipationCertificate

namespace Chronos
namespace Frontier

def RestrictedAdmissibleDissipationSurface
    (State : Type)
    (evolve : State → ℝ → State)
    (Dissipation : State → ℝ)
    (Admissible : State → Prop) : Prop :=
  ∃ lam : ℝ,
    0 < lam ∧
    ∀ D : State,
      Admissible D →
      ∀ t : ℝ,
        0 ≤ t →
          Dissipation (evolve D t) ≤ Dissipation D * Real.exp (-lam * t)

theorem restrictedAdmissibleDissipation_from_restrictedEntropyDissipation
    {State : Type}
    {evolve : State → ℝ → State}
    {Entropy : State → ℝ}
    {Admissible : State → Prop}
    (h : RestrictedEntropyDissipationCertificate State evolve Entropy Admissible) :
    RestrictedAdmissibleDissipationSurface State evolve Entropy Admissible := by
  exact h

theorem restrictedAdmissibleDissipation_from_uniformEntropyControl
    {State : Type}
    {evolve : State → ℝ → State}
    {Entropy : State → ℝ}
    {Admissible : State → Prop}
    (h : UniformEntropyControlCertificate State evolve Entropy) :
    RestrictedAdmissibleDissipationSurface State evolve Entropy Admissible := by
  exact
    restrictedAdmissibleDissipation_from_restrictedEntropyDissipation
      (restrictedEntropyDissipation_from_uniformEntropyControl h)

theorem restrictedAdmissibleDissipation_from_uniformLyapunovDecay_sameFunctional
    {State : Type}
    {evolve : State → ℝ → State}
    {Entropy : State → ℝ}
    {Admissible : State → Prop}
    (h : UniformLyapunovDecayCertificate State evolve Entropy) :
    RestrictedAdmissibleDissipationSurface State evolve Entropy Admissible := by
  exact
    restrictedAdmissibleDissipation_from_restrictedEntropyDissipation
      (restrictedEntropyDissipation_from_uniformLyapunovDecay_sameFunctional h)

end Frontier
end Chronos
