import Chronos.Frontier.RestrictedAdmissibleDissipationSurface

namespace Chronos
namespace Frontier

def RestrictedRateThickCoercivitySurface
    (State : Type)
    (evolve : State → ℝ → State)
    (CoerciveQuantity : State → ℝ)
    (Admissible : State → Prop) : Prop :=
  ∃ lam : ℝ,
    0 < lam ∧
    ∀ D : State,
      Admissible D →
      ∀ t : ℝ,
        0 ≤ t →
          CoerciveQuantity (evolve D t) ≤
            CoerciveQuantity D * Real.exp (-lam * t)

def RestrictedDissipationToRateThickCoercivitySurface
    (State : Type)
    (evolve : State → ℝ → State)
    (Dissipation : State → ℝ)
    (Admissible : State → Prop) : Prop :=
  RestrictedAdmissibleDissipationSurface State evolve Dissipation Admissible →
    RestrictedRateThickCoercivitySurface State evolve Dissipation Admissible

theorem restrictedRateThickCoercivity_from_restrictedAdmissibleDissipation
    {State : Type}
    {evolve : State → ℝ → State}
    {Dissipation : State → ℝ}
    {Admissible : State → Prop}
    (h : RestrictedAdmissibleDissipationSurface State evolve Dissipation Admissible) :
    RestrictedRateThickCoercivitySurface State evolve Dissipation Admissible := by
  exact h

theorem restrictedDissipationToRateThickCoercivity_surface
    {State : Type}
    {evolve : State → ℝ → State}
    {Dissipation : State → ℝ}
    {Admissible : State → Prop} :
    RestrictedDissipationToRateThickCoercivitySurface
      State evolve Dissipation Admissible := by
  intro h
  exact restrictedRateThickCoercivity_from_restrictedAdmissibleDissipation h

theorem restrictedRateThickCoercivity_from_uniformEntropyControl
    {State : Type}
    {evolve : State → ℝ → State}
    {Entropy : State → ℝ}
    {Admissible : State → Prop}
    (h : UniformEntropyControlCertificate State evolve Entropy) :
    RestrictedRateThickCoercivitySurface State evolve Entropy Admissible := by
  exact
    restrictedRateThickCoercivity_from_restrictedAdmissibleDissipation
      (restrictedAdmissibleDissipation_from_uniformEntropyControl h)

theorem restrictedRateThickCoercivity_from_uniformLyapunovDecay_sameFunctional
    {State : Type}
    {evolve : State → ℝ → State}
    {Entropy : State → ℝ}
    {Admissible : State → Prop}
    (h : UniformLyapunovDecayCertificate State evolve Entropy) :
    RestrictedRateThickCoercivitySurface State evolve Entropy Admissible := by
  exact
    restrictedRateThickCoercivity_from_restrictedAdmissibleDissipation
      (restrictedAdmissibleDissipation_from_uniformLyapunovDecay_sameFunctional h)

end Frontier
end Chronos
