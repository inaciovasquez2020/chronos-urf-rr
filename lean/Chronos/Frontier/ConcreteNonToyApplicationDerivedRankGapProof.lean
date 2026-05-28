namespace Chronos.Frontier.ConcreteNonToyApplicationDerivedRankGapProof

structure ConcreteNonToyApplication where
  witnessCount : Nat
  rankLowerBound : Nat
  entropyUpperBound : Nat
deriving Repr, DecidableEq

def isNonToyApplication (x : ConcreteNonToyApplication) : Prop :=
  0 < x.witnessCount

def derivedRankGap (x : ConcreteNonToyApplication) : Nat :=
  x.rankLowerBound - x.entropyUpperBound

def hasPositiveDerivedRankGap (x : ConcreteNonToyApplication) : Prop :=
  0 < derivedRankGap x

structure ConcreteNonToyApplicationDerivedRankGapProof where
  app : ConcreteNonToyApplication
  nonToy : isNonToyApplication app
  positiveGap : hasPositiveDerivedRankGap app

theorem concrete_non_toy_application_exports_rank_gap
    (p : ConcreteNonToyApplicationDerivedRankGapProof) :
    hasPositiveDerivedRankGap p.app := p.positiveGap

theorem concrete_non_toy_application_exports_non_toy
    (p : ConcreteNonToyApplicationDerivedRankGapProof) :
    isNonToyApplication p.app := p.nonToy

end Chronos.Frontier.ConcreteNonToyApplicationDerivedRankGapProof
