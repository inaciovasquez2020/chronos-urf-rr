import Chronos.Frontier.ApplicationDerivedRankGapInequality

namespace Chronos
namespace Frontier

noncomputable section

/--
Concrete non-toy application packet.

The rank, gap, and slack values are extracted from finite application data lists,
rather than hand-set directly in the final inequality witness.
-/
structure ConcreteNonToyApplicationDataPacket where
  applicationName : String
  registryAtoms : List String
  rankWitnesses : List String
  gapWitnesses : List String
  slackWitnesses : List String
  rankWitnesses_nonempty : rankWitnesses.length = 1
  gapWitnesses_length : gapWitnesses.length = 3
  slackWitnesses_length : slackWitnesses.length = 1

def concreteFiniteRegisteredHyperbolicPacket :
    ConcreteNonToyApplicationDataPacket where
  applicationName := "finite-registered-hyperbolic-rate-thick-stack/concrete-data-packet"
  registryAtoms := [
    "rate-thick-carrier",
    "finite-registry",
    "hyperbolic-gap",
    "natural-dominance"
  ]
  rankWitnesses := [
    "semantic-rank-generator"
  ]
  gapWitnesses := [
    "fiber-gap-left",
    "fiber-gap-center",
    "fiber-gap-right"
  ]
  slackWitnesses := [
    "positive-application-slack"
  ]
  rankWitnesses_nonempty := by decide
  gapWitnesses_length := by decide
  slackWitnesses_length := by decide

def extractedConcreteSemanticRankRate
    (P : ConcreteNonToyApplicationDataPacket) : Nat :=
  P.rankWitnesses.length

def extractedConcreteFiberEntropyGap
    (P : ConcreteNonToyApplicationDataPacket) : Nat :=
  P.gapWitnesses.length

def extractedConcreteRankGapSlack
    (P : ConcreteNonToyApplicationDataPacket) : Nat :=
  P.slackWitnesses.length

def concreteNonToyApplicationRankGapInequality :
    ApplicationDerivedRankGapInequality where
  applicationName := concreteFiniteRegisteredHyperbolicPacket.applicationName
  semanticRankRate :=
    extractedConcreteSemanticRankRate concreteFiniteRegisteredHyperbolicPacket
  fiberEntropyGap :=
    extractedConcreteFiberEntropyGap concreteFiniteRegisteredHyperbolicPacket
  slack :=
    extractedConcreteRankGapSlack concreteFiniteRegisteredHyperbolicPacket
  nontrivialSlack := by decide
  rankToGapInequality := by decide

theorem concreteNonToyApplication_extracted_rank_eq :
    extractedConcreteSemanticRankRate concreteFiniteRegisteredHyperbolicPacket = 1 := by
  decide

theorem concreteNonToyApplication_extracted_gap_eq :
    extractedConcreteFiberEntropyGap concreteFiniteRegisteredHyperbolicPacket = 3 := by
  decide

theorem concreteNonToyApplication_extracted_slack_eq :
    extractedConcreteRankGapSlack concreteFiniteRegisteredHyperbolicPacket = 1 := by
  decide

theorem concreteNonToyApplication_extracted_rank_plus_slack_le_gap :
    concreteNonToyApplicationRankGapInequality.semanticRankRate
      + concreteNonToyApplicationRankGapInequality.slack
      ≤ concreteNonToyApplicationRankGapInequality.fiberEntropyGap := by
  decide

theorem concreteNonToyApplication_extracted_rank_lt_gap :
    concreteNonToyApplicationRankGapInequality.semanticRankRate
      < concreteNonToyApplicationRankGapInequality.fiberEntropyGap := by
  decide

end

end Frontier
end Chronos
