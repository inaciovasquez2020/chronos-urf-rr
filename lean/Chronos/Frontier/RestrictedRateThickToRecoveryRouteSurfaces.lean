import Chronos.Frontier.RestrictedDissipationToRateThickCoercivitySurface

namespace Chronos
namespace Frontier

def RestrictedUniversalFiberEntropyGapRoute
    (State : Type)
    (evolve : State → ℝ → State)
    (GapQuantity : State → ℝ)
    (Admissible : State → Prop) : Prop :=
  ∃ lam : ℝ,
    0 < lam ∧
    ∀ D : State,
      Admissible D →
      ∀ t : ℝ,
        0 ≤ t →
          GapQuantity (evolve D t) ≤
            GapQuantity D * Real.exp (-lam * t)

def RestrictedChronosRRRecoveryBridge
    (State : Type)
    (evolve : State → ℝ → State)
    (RankQuantity : State → ℝ)
    (Admissible : State → Prop) : Prop :=
  ∃ lam : ℝ,
    0 < lam ∧
    ∀ D : State,
      Admissible D →
      ∀ t : ℝ,
        0 ≤ t →
          RankQuantity (evolve D t) ≤
            RankQuantity D * Real.exp (-lam * t)

def RestrictedH41FGLRecoveryBridge
    (State : Type)
    (evolve : State → ℝ → State)
    (FGLQuantity : State → ℝ)
    (Admissible : State → Prop) : Prop :=
  ∃ lam : ℝ,
    0 < lam ∧
    ∀ D : State,
      Admissible D →
      ∀ t : ℝ,
        0 ≤ t →
          FGLQuantity (evolve D t) ≤
            FGLQuantity D * Real.exp (-lam * t)

theorem restrictedUniversalFiberEntropyGapRoute_from_restrictedRateThickCoercivity
    {State : Type}
    {evolve : State → ℝ → State}
    {Q : State → ℝ}
    {Admissible : State → Prop}
    (h : RestrictedRateThickCoercivitySurface State evolve Q Admissible) :
    RestrictedUniversalFiberEntropyGapRoute State evolve Q Admissible := by
  exact h

theorem restrictedChronosRRRecoveryBridge_from_restrictedUniversalFiberEntropyGapRoute
    {State : Type}
    {evolve : State → ℝ → State}
    {Q : State → ℝ}
    {Admissible : State → Prop}
    (h : RestrictedUniversalFiberEntropyGapRoute State evolve Q Admissible) :
    RestrictedChronosRRRecoveryBridge State evolve Q Admissible := by
  exact h

theorem restrictedH41FGLRecoveryBridge_from_restrictedChronosRRRecoveryBridge
    {State : Type}
    {evolve : State → ℝ → State}
    {Q : State → ℝ}
    {Admissible : State → Prop}
    (h : RestrictedChronosRRRecoveryBridge State evolve Q Admissible) :
    RestrictedH41FGLRecoveryBridge State evolve Q Admissible := by
  exact h

theorem restrictedChronosRRRecoveryBridge_from_restrictedRateThickCoercivity
    {State : Type}
    {evolve : State → ℝ → State}
    {Q : State → ℝ}
    {Admissible : State → Prop}
    (h : RestrictedRateThickCoercivitySurface State evolve Q Admissible) :
    RestrictedChronosRRRecoveryBridge State evolve Q Admissible := by
  exact
    restrictedChronosRRRecoveryBridge_from_restrictedUniversalFiberEntropyGapRoute
      (restrictedUniversalFiberEntropyGapRoute_from_restrictedRateThickCoercivity h)

theorem restrictedH41FGLRecoveryBridge_from_restrictedRateThickCoercivity
    {State : Type}
    {evolve : State → ℝ → State}
    {Q : State → ℝ}
    {Admissible : State → Prop}
    (h : RestrictedRateThickCoercivitySurface State evolve Q Admissible) :
    RestrictedH41FGLRecoveryBridge State evolve Q Admissible := by
  exact
    restrictedH41FGLRecoveryBridge_from_restrictedChronosRRRecoveryBridge
      (restrictedChronosRRRecoveryBridge_from_restrictedRateThickCoercivity h)

theorem restrictedRecoveryRoute_from_uniformEntropyControl
    {State : Type}
    {evolve : State → ℝ → State}
    {Entropy : State → ℝ}
    {Admissible : State → Prop}
    (h : UniformEntropyControlCertificate State evolve Entropy) :
    RestrictedH41FGLRecoveryBridge State evolve Entropy Admissible := by
  exact
    restrictedH41FGLRecoveryBridge_from_restrictedRateThickCoercivity
      (restrictedRateThickCoercivity_from_uniformEntropyControl h)

theorem restrictedRecoveryRoute_from_uniformLyapunovDecay_sameFunctional
    {State : Type}
    {evolve : State → ℝ → State}
    {Entropy : State → ℝ}
    {Admissible : State → Prop}
    (h : UniformLyapunovDecayCertificate State evolve Entropy) :
    RestrictedH41FGLRecoveryBridge State evolve Entropy Admissible := by
  exact
    restrictedH41FGLRecoveryBridge_from_restrictedRateThickCoercivity
      (restrictedRateThickCoercivity_from_uniformLyapunovDecay_sameFunctional h)

end Frontier
end Chronos
