import Mathlib.Data.Real.Basic

namespace Chronos
namespace Frontier
namespace FPz1

variable {Obj Wit : Type}

def RateSpectrumIsolation
    (ChronosAdmissible : Obj → Prop)
    (SemanticRankRateWitness : Obj → Wit → Prop)
    (rankRate : Wit → ℝ) : Prop :=
  ∃ lam0 : ℝ, lam0 > 0 ∧
    ∀ X ρ,
      ChronosAdmissible X →
      SemanticRankRateWitness X ρ →
      rankRate ρ > 0 →
      rankRate ρ ≥ lam0

def EntropyFaithfulLowerEnvelope
    (ChronosAdmissible : Obj → Prop)
    (SemanticRankRateWitness : Obj → Wit → Prop)
    (rankRate : Wit → ℝ)
    (FiberEntropyMass : Obj → Wit → ℝ) : Prop :=
  ∀ lam : ℝ, lam > 0 →
    ∃ eps : ℝ, eps > 0 ∧
      ∀ X ρ,
        ChronosAdmissible X →
        SemanticRankRateWitness X ρ →
        rankRate ρ ≥ lam →
        FiberEntropyMass X ρ ≥ eps

def QuantitativeEntropyFaithfulSemanticFiberizationUnrestricted
    (ChronosAdmissible : Obj → Prop)
    (SemanticRankRateWitness : Obj → Wit → Prop)
    (rankRate : Wit → ℝ)
    (FiberEntropyMass : Obj → Wit → ℝ) : Prop :=
  ∃ eps : ℝ, eps > 0 ∧
    ∀ X ρ,
      ChronosAdmissible X →
      SemanticRankRateWitness X ρ →
      rankRate ρ > 0 →
      FiberEntropyMass X ρ ≥ eps

def DepthBridgeUnrestricted
    (ChronosAdmissible : Obj → Prop)
    (SemanticRankRateWitness : Obj → Wit → Prop)
    (rankRate : Wit → ℝ)
    (FiberEntropyMass : Obj → Wit → ℝ)
    (ChronosRRConclusion : Obj → Prop) : Prop :=
  QuantitativeEntropyFaithfulSemanticFiberizationUnrestricted
      ChronosAdmissible
      SemanticRankRateWitness
      rankRate
      FiberEntropyMass →
    ∀ X,
      ChronosAdmissible X →
      ChronosRRConclusion X

def ChronosRRUnrestricted
    (ChronosAdmissible : Obj → Prop)
    (ChronosRRConclusion : Obj → Prop) : Prop :=
  ∀ X,
    ChronosAdmissible X →
    ChronosRRConclusion X

theorem rateSpectrumIsolation_and_lowerEnvelope_to_quantitativeUnrestricted
    (ChronosAdmissible : Obj → Prop)
    (SemanticRankRateWitness : Obj → Wit → Prop)
    (rankRate : Wit → ℝ)
    (FiberEntropyMass : Obj → Wit → ℝ)
    (hIso :
      RateSpectrumIsolation
        ChronosAdmissible
        SemanticRankRateWitness
        rankRate)
    (hEnvelope :
      EntropyFaithfulLowerEnvelope
        ChronosAdmissible
        SemanticRankRateWitness
        rankRate
        FiberEntropyMass) :
    QuantitativeEntropyFaithfulSemanticFiberizationUnrestricted
      ChronosAdmissible
      SemanticRankRateWitness
      rankRate
      FiberEntropyMass := by
  rcases hIso with ⟨lam0, hlam0pos, hgap⟩
  rcases hEnvelope lam0 hlam0pos with ⟨eps, hepspos, hbound⟩
  refine ⟨eps, hepspos, ?_⟩
  intro X ρ hAdm hWit hrpos
  exact hbound X ρ hAdm hWit (hgap X ρ hAdm hWit hrpos)

theorem fpz1_conditional_unrestricted_route
    (ChronosAdmissible : Obj → Prop)
    (SemanticRankRateWitness : Obj → Wit → Prop)
    (rankRate : Wit → ℝ)
    (FiberEntropyMass : Obj → Wit → ℝ)
    (ChronosRRConclusion : Obj → Prop)
    (hIso :
      RateSpectrumIsolation
        ChronosAdmissible
        SemanticRankRateWitness
        rankRate)
    (hEnvelope :
      EntropyFaithfulLowerEnvelope
        ChronosAdmissible
        SemanticRankRateWitness
        rankRate
        FiberEntropyMass)
    (hDepth :
      DepthBridgeUnrestricted
        ChronosAdmissible
        SemanticRankRateWitness
        rankRate
        FiberEntropyMass
        ChronosRRConclusion) :
    ChronosRRUnrestricted
      ChronosAdmissible
      ChronosRRConclusion := by
  exact hDepth
    (rateSpectrumIsolation_and_lowerEnvelope_to_quantitativeUnrestricted
      ChronosAdmissible
      SemanticRankRateWitness
      rankRate
      FiberEntropyMass
      hIso
      hEnvelope)

end FPz1
end Frontier
end Chronos
