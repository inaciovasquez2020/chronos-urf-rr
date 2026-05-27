import Chronos.Frontier.DerivedFiniteRegisteredHyperbolicNaturalAdmissibilityCertificate

namespace Chronos
namespace Frontier

noncomputable section

/--
A minimal application-derived rank/gap datum.

This deliberately separates the new object from registry-arity equality dominance:
the rank and gap are supplied by an application certificate together with a
strict positive slack witness.
-/
structure ApplicationDerivedRankGapInequality where
  applicationName : String
  semanticRankRate : Nat
  fiberEntropyGap : Nat
  slack : Nat
  nontrivialSlack : 0 < slack
  rankToGapInequality : semanticRankRate + slack ≤ fiberEntropyGap

def finiteRegisteredHyperbolicApplicationRankGapInequality :
    ApplicationDerivedRankGapInequality where
  applicationName := "finite-registered-hyperbolic-rate-thick-stack"
  semanticRankRate := 1
  fiberEntropyGap := 2
  slack := 1
  nontrivialSlack := by decide
  rankToGapInequality := by decide

theorem finiteRegisteredHyperbolicApplication_rank_lt_gap :
    finiteRegisteredHyperbolicApplicationRankGapInequality.semanticRankRate
      < finiteRegisteredHyperbolicApplicationRankGapInequality.fiberEntropyGap := by
  decide

theorem finiteRegisteredHyperbolicApplication_has_nontrivial_slack :
    0 < finiteRegisteredHyperbolicApplicationRankGapInequality.slack :=
  finiteRegisteredHyperbolicApplicationRankGapInequality.nontrivialSlack

theorem finiteRegisteredHyperbolicApplication_rank_plus_slack_le_gap :
    finiteRegisteredHyperbolicApplicationRankGapInequality.semanticRankRate
      + finiteRegisteredHyperbolicApplicationRankGapInequality.slack
      ≤ finiteRegisteredHyperbolicApplicationRankGapInequality.fiberEntropyGap :=
  finiteRegisteredHyperbolicApplicationRankGapInequality.rankToGapInequality

end

end Frontier
end Chronos
