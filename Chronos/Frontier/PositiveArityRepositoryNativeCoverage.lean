import Chronos.Frontier.RepositoryNativeImageCoverageCounterexample
import Chronos.Frontier.IntendedRepositoryNativeImageCoverage

namespace Chronos.Frontier.PositiveArityRepositoryNativeCoverage

/--
Weakest admissible repair after the zero-arity counterexample:
the unrestricted coverage target is false as stated, so the next
structural theorem target must exclude zero-arity carriers or replace
the unrestricted predicate.
-/
def PositiveArityCarrier
    (C : ChronosCarrierData) : Prop :=
  RealChronosAdmissiblePredicate ChronosRegistry ChronosTraceFamily C ∧
  C.arity ≠ 0

/--
Positive-arity repository-native coverage is the next theorem target.
This is intentionally left as the missing theorem, not asserted.
-/
def PositiveArityRepositoryNativeImageCovers : Prop :=
  RepositoryNativeImageCovers PositiveArityCarrier

/--
Once positive-arity coverage is proved, Reg-SNF follows through the
existing repository-native image bridge.
-/
theorem positive_arity_coverage_implies_reg_snf
    (h : PositiveArityRepositoryNativeImageCovers)
    (C : ChronosCarrierData)
    (hC : PositiveArityCarrier C) :
    RegSNF ChronosRegistry ChronosTraceFamily C := by
  exact repository_native_image_coverage_implies_reg_snf PositiveArityCarrier h C hC

/--
Current exact missing object after the counterexample:
prove positive-arity coverage, or replace this target by intended-carrier coverage.
-/
def MissingPositiveArityCoverageTheorem : Prop :=
  PositiveArityRepositoryNativeImageCovers

/--
The intended-carrier route is already closed; the positive-arity route is
the strictly stronger next target only if intended carriers are not accepted
as the final theorem domain.
-/
theorem intended_route_already_closed :
    IntendedRepositoryNativeImageCoverageClosed := by
  exact intended_repository_native_image_coverage_closed

end Chronos.Frontier.PositiveArityRepositoryNativeCoverage
