import Chronos.Frontier.PositiveArityRepositoryNativeCoverage

namespace Chronos.Frontier.PositiveArityCoverageDecisionLock

/--
Decision object after public-door closure and positive-arity target creation.

Exactly one theorem domain should be selected before further downstream promotion:
1. intended-carrier domain;
2. positive-arity admissible-carrier domain;
3. broadened repository-native domain.
-/
inductive CarrierCoverageDomain where
  | intendedCarrier
  | positiveArity
  | broadenedRepositoryNative
deriving DecidableEq, Repr

/--
The weakest already-closed domain is IntendedChronosCarrier.
-/
def IntendedDomainClosed : Prop :=
  IntendedRepositoryNativeImageCoverageClosed

/--
The next stronger domain is positive-arity admissibility.
This remains the active missing theorem.
-/
def PositiveArityDomainOpen : Prop :=
  MissingPositiveArityCoverageTheorem

/--
The broadest repair route is to broaden the repository-native carrier
notion so that the zero-arity counterexample is absorbed rather than excluded.
This is intentionally recorded as a separate structural option.
-/
def BroadenedRepositoryNativeDomainRequired : Prop :=
  True

/--
Canonical current decision:
do not promote beyond intended-carrier closure unless positive-arity
coverage is proved or the repository-native carrier domain is broadened.
-/
def CurrentAdmissibleDomainDecision : CarrierCoverageDomain :=
  CarrierCoverageDomain.positiveArity

theorem intended_domain_closed :
    IntendedDomainClosed := by
  exact intended_route_already_closed

/--
The active theorem target remains positive-arity repository-native coverage.
-/
theorem current_decision_target_is_positive_arity :
    CurrentAdmissibleDomainDecision = CarrierCoverageDomain.positiveArity := by
  rfl

/--
No downstream theorem promotion is available from this lock alone.
It only records the exact next theorem object.
-/
def NoDownstreamPromotionFromDecisionLock : Prop :=
  True

theorem no_downstream_promotion_from_decision_lock :
    NoDownstreamPromotionFromDecisionLock := by
  trivial

end Chronos.Frontier.PositiveArityCoverageDecisionLock
