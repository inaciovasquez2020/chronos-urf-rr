import Chronos.Frontier.R1NativeCounterexampleCoherentRestriction

namespace Chronos.Frontier

/--
Native admissibility package for the R1 coherence-promotion frontier.

This is intentionally an OPEN package predicate. It records the native
admissibility input that would have to imply
`RepositoryNativeR1LongChordCoherence` in order to promote coherent R1 from
an external/restricted ingredient to a native consequence.
-/
def NativeAdmissibilityPackage : Prop :=
  True

/--
The exact OPEN promotion target:

native admissibility should imply repository-native R1 long-chord coherence.
-/
def R1NativeCoherencePromotionTarget : Prop :=
  NativeAdmissibilityPackage → RepositoryNativeR1LongChordCoherence

/--
The exact OPEN counterexample target:

native admissibility holds while R1 long-chord coherence fails.
-/
def R1NativeCoherenceCounterexampleTarget : Prop :=
  NativeAdmissibilityPackage ∧ ¬ RepositoryNativeR1LongChordCoherence

/--
OPEN missing lemma.

This is deliberately stated as a proposition, not proved. Proving this is
the remaining R1 native-promotion problem after unrestricted native R1 was
refuted by `R1UnrestrictedNativeLongChordExclusionFalse`.
-/
def NativeAdmissibility_implies_R1LongChordCoherence_OPEN : Prop :=
  NativeAdmissibilityPackage → RepositoryNativeR1LongChordCoherence

/--
OPEN refutation target.

A proof of this proposition would show that R1 coherence is not derivable
from the currently supplied native admissibility package.
-/
def NativeAdmissibility_R1LongChordCoherence_counterexample_OPEN : Prop :=
  NativeAdmissibilityPackage ∧ ¬ RepositoryNativeR1LongChordCoherence

/--
No-promotion guard.

This file only localizes the R1 coherence promotion problem. It does not
prove R1 promotion, R2, R3, NON_FACTORISATION, Chronos-RR, H4.1/FGL,
P vs NP, or any Clay problem.
-/
def R1NativeCoherencePromotionBoundary : String :=
  "R1_COHERENCE_PROMOTION_TARGET_OPEN_ONLY"

end Chronos.Frontier
