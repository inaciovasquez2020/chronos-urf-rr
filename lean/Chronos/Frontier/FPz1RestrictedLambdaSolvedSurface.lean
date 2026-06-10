import Mathlib.Data.Real.Basic

namespace Chronos
namespace Frontier
namespace FPz1

variable {Obj Wit : Type}

def ChronosAdmissibleLambda
    (ChronosAdmissible : Obj → Prop)
    (SemanticRankRateWitness : Obj → Wit → Prop)
    (rankRate : Wit → ℝ)
    (lam : ℝ) : Obj → Prop :=
  fun X =>
    ChronosAdmissible X ∧
      ∀ ρ,
        SemanticRankRateWitness X ρ →
        rankRate ρ > 0 →
        rankRate ρ ≥ lam

def QuantitativeEntropyFaithfulSemanticFiberizationLambda
    (ChronosAdmissible : Obj → Prop)
    (SemanticRankRateWitness : Obj → Wit → Prop)
    (rankRate : Wit → ℝ)
    (FiberEntropyMass : Obj → Wit → ℝ)
    (lam : ℝ) : Prop :=
  lam > 0 ∧
    ∃ εlam : ℝ, εlam > 0 ∧
      ∀ X ρ,
        ChronosAdmissibleLambda
          ChronosAdmissible
          SemanticRankRateWitness
          rankRate
          lam
          X →
        SemanticRankRateWitness X ρ →
        rankRate ρ > 0 →
        FiberEntropyMass X ρ ≥ εlam

def RestrictedEntropyFaithfulLowerEnvelope
    (ChronosAdmissible : Obj → Prop)
    (SemanticRankRateWitness : Obj → Wit → Prop)
    (rankRate : Wit → ℝ)
    (FiberEntropyMass : Obj → Wit → ℝ) : Prop :=
  ∀ lam : ℝ, lam > 0 →
    ∃ εlam : ℝ, εlam > 0 ∧
      ∀ X ρ,
        ChronosAdmissible X →
        SemanticRankRateWitness X ρ →
        rankRate ρ ≥ lam →
        FiberEntropyMass X ρ ≥ εlam

def DepthBridgeLambda
    (ChronosAdmissible : Obj → Prop)
    (SemanticRankRateWitness : Obj → Wit → Prop)
    (rankRate : Wit → ℝ)
    (FiberEntropyMass : Obj → Wit → ℝ)
    (ChronosRRConclusion : Obj → Prop)
    (lam : ℝ) : Prop :=
  QuantitativeEntropyFaithfulSemanticFiberizationLambda
      ChronosAdmissible
      SemanticRankRateWitness
      rankRate
      FiberEntropyMass
      lam →
    ∀ X,
      ChronosAdmissibleLambda
        ChronosAdmissible
        SemanticRankRateWitness
        rankRate
        lam
        X →
      ChronosRRConclusion X

def ChronosRRLambda
    (ChronosAdmissible : Obj → Prop)
    (SemanticRankRateWitness : Obj → Wit → Prop)
    (rankRate : Wit → ℝ)
    (ChronosRRConclusion : Obj → Prop)
    (lam : ℝ) : Prop :=
  ∀ X,
    ChronosAdmissibleLambda
      ChronosAdmissible
      SemanticRankRateWitness
      rankRate
      lam
      X →
    ChronosRRConclusion X

theorem restrictedRateSpectrumIsolation
    (ChronosAdmissible : Obj → Prop)
    (SemanticRankRateWitness : Obj → Wit → Prop)
    (rankRate : Wit → ℝ)
    {lam : ℝ}
    {X : Obj}
    {ρ : Wit}
    (hX :
      ChronosAdmissibleLambda
        ChronosAdmissible
        SemanticRankRateWitness
        rankRate
        lam
        X)
    (hρ : SemanticRankRateWitness X ρ)
    (hrpos : rankRate ρ > 0) :
    rankRate ρ ≥ lam :=
  hX.2 ρ hρ hrpos

theorem lowerEnvelope_to_quantitativeLambda
    (ChronosAdmissible : Obj → Prop)
    (SemanticRankRateWitness : Obj → Wit → Prop)
    (rankRate : Wit → ℝ)
    (FiberEntropyMass : Obj → Wit → ℝ)
    {lam : ℝ}
    (hlam : lam > 0)
    (hEnvelope :
      RestrictedEntropyFaithfulLowerEnvelope
        ChronosAdmissible
        SemanticRankRateWitness
        rankRate
        FiberEntropyMass) :
    QuantitativeEntropyFaithfulSemanticFiberizationLambda
      ChronosAdmissible
      SemanticRankRateWitness
      rankRate
      FiberEntropyMass
      lam := by
  rcases hEnvelope lam hlam with ⟨εlam, hεpos, hbound⟩
  refine ⟨hlam, εlam, hεpos, ?_⟩
  intro X ρ hX hρ hrpos
  exact hbound X ρ hX.1 hρ (hX.2 ρ hρ hrpos)

theorem fpz1_restricted_lambda_route
    (ChronosAdmissible : Obj → Prop)
    (SemanticRankRateWitness : Obj → Wit → Prop)
    (rankRate : Wit → ℝ)
    (FiberEntropyMass : Obj → Wit → ℝ)
    (ChronosRRConclusion : Obj → Prop)
    {lam : ℝ}
    (hlam : lam > 0)
    (hEnvelope :
      RestrictedEntropyFaithfulLowerEnvelope
        ChronosAdmissible
        SemanticRankRateWitness
        rankRate
        FiberEntropyMass)
    (hDepth :
      DepthBridgeLambda
        ChronosAdmissible
        SemanticRankRateWitness
        rankRate
        FiberEntropyMass
        ChronosRRConclusion
        lam) :
    ChronosRRLambda
      ChronosAdmissible
      SemanticRankRateWitness
      rankRate
      ChronosRRConclusion
      lam := by
  exact hDepth
    (lowerEnvelope_to_quantitativeLambda
      ChronosAdmissible
      SemanticRankRateWitness
      rankRate
      FiberEntropyMass
      hlam
      hEnvelope)

end FPz1
end Frontier
end Chronos
