import Mathlib.Data.Real.Basic

namespace Chronos
namespace Frontier
namespace FPz1RateThick

variable {Obj Wit : Type}

def RateThickDomain
    (ChronosAdmissible : Obj -> Prop)
    (SemanticRankRateWitness : Obj -> Wit -> Prop)
    (rankRate : Wit -> Real)
    (lam : Real) : Obj -> Prop :=
  fun X =>
    ChronosAdmissible X /\
      forall rho,
        SemanticRankRateWitness X rho ->
        rankRate rho > 0 ->
        rankRate rho >= lam

def EntropyFaithfulLowerEnvelopeAt
    (ChronosAdmissible : Obj -> Prop)
    (SemanticRankRateWitness : Obj -> Wit -> Prop)
    (rankRate : Wit -> Real)
    (FiberEntropyMass : Obj -> Wit -> Real)
    (lam : Real) : Prop :=
  exists eps : Real,
    eps > 0 /\
      forall X rho,
        ChronosAdmissible X ->
        SemanticRankRateWitness X rho ->
        rankRate rho >= lam ->
        FiberEntropyMass X rho >= eps

def EntropyFaithfulLowerEnvelope
    (ChronosAdmissible : Obj -> Prop)
    (SemanticRankRateWitness : Obj -> Wit -> Prop)
    (rankRate : Wit -> Real)
    (FiberEntropyMass : Obj -> Wit -> Real) : Prop :=
  forall lam : Real,
    lam > 0 ->
      EntropyFaithfulLowerEnvelopeAt
        ChronosAdmissible
        SemanticRankRateWitness
        rankRate
        FiberEntropyMass
        lam

def RateDependentUniversalFiberEntropyGap
    (ChronosAdmissible : Obj -> Prop)
    (SemanticRankRateWitness : Obj -> Wit -> Prop)
    (rankRate : Wit -> Real)
    (FiberEntropyMass : Obj -> Wit -> Real)
    (lam : Real) : Prop :=
  lam > 0 /\
    exists eps : Real,
      eps > 0 /\
        forall X rho,
          RateThickDomain
            ChronosAdmissible
            SemanticRankRateWitness
            rankRate
            lam
            X ->
          SemanticRankRateWitness X rho ->
          rankRate rho > 0 ->
          FiberEntropyMass X rho >= eps

theorem rateThickDomain_positive_rate_isolated
    (ChronosAdmissible : Obj -> Prop)
    (SemanticRankRateWitness : Obj -> Wit -> Prop)
    (rankRate : Wit -> Real)
    {lam : Real}
    {X : Obj}
    {rho : Wit}
    (hX :
      RateThickDomain
        ChronosAdmissible
        SemanticRankRateWitness
        rankRate
        lam
        X)
    (hRho : SemanticRankRateWitness X rho)
    (hpos : rankRate rho > 0) :
    rankRate rho >= lam := by
  exact hX.right rho hRho hpos

theorem entropyFaithfulLowerEnvelopeAt_to_rateDependentUniversalFiberEntropyGap
    (ChronosAdmissible : Obj -> Prop)
    (SemanticRankRateWitness : Obj -> Wit -> Prop)
    (rankRate : Wit -> Real)
    (FiberEntropyMass : Obj -> Wit -> Real)
    {lam : Real}
    (hlam : lam > 0)
    (hEnvelope :
      EntropyFaithfulLowerEnvelopeAt
        ChronosAdmissible
        SemanticRankRateWitness
        rankRate
        FiberEntropyMass
        lam) :
    RateDependentUniversalFiberEntropyGap
      ChronosAdmissible
      SemanticRankRateWitness
      rankRate
      FiberEntropyMass
      lam := by
  exact Exists.elim hEnvelope (fun eps h =>
    And.intro hlam
      (Exists.intro eps
        (And.intro h.left
          (by
            intro X rho hX hRho hpos
            exact h.right X rho hX.left hRho (hX.right rho hRho hpos)))))

theorem entropyFaithfulLowerEnvelope_to_rateDependentUniversalFiberEntropyGap
    (ChronosAdmissible : Obj -> Prop)
    (SemanticRankRateWitness : Obj -> Wit -> Prop)
    (rankRate : Wit -> Real)
    (FiberEntropyMass : Obj -> Wit -> Real)
    {lam : Real}
    (hlam : lam > 0)
    (hEnvelope :
      EntropyFaithfulLowerEnvelope
        ChronosAdmissible
        SemanticRankRateWitness
        rankRate
        FiberEntropyMass) :
    RateDependentUniversalFiberEntropyGap
      ChronosAdmissible
      SemanticRankRateWitness
      rankRate
      FiberEntropyMass
      lam := by
  exact
    entropyFaithfulLowerEnvelopeAt_to_rateDependentUniversalFiberEntropyGap
      ChronosAdmissible
      SemanticRankRateWitness
      rankRate
      FiberEntropyMass
      hlam
      (hEnvelope lam hlam)

end FPz1RateThick
end Frontier
end Chronos
