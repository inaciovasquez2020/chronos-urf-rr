import Chronos.Frontier.R1NativeCoherencePromotionTarget

namespace Chronos.Frontier

/--
Repository-native R1 long-chord coherence is refuted by the already formalized
unrestricted long-chord witness.

Reason:

* `R1CoherentLongChordExclusionProofTarget_proved` gives
  `RepositoryNativeR1LongChordCoherence → NoRepositoryNativeLongChordWitness`.
* `R1UnrestrictedNativeLongChordExclusionFalse` gives
  `¬ NoRepositoryNativeLongChordWitness`.

Therefore `RepositoryNativeR1LongChordCoherence` is impossible under the
current native long-chord definitions.
-/
theorem RepositoryNativeR1LongChordCoherence_refuted :
    ¬ RepositoryNativeR1LongChordCoherence := by
  intro h
  exact R1UnrestrictedNativeLongChordExclusionFalse
    (R1CoherentLongChordExclusionProofTarget_proved h)

/--
The counterexample target from `R1NativeCoherencePromotionTarget` is now closed.

Since `NativeAdmissibilityPackage` is the open/package placeholder `True`, the
formal content is the refutation of `RepositoryNativeR1LongChordCoherence`.
-/
theorem R1NativeCoherenceCounterexampleTarget_proved :
    R1NativeCoherenceCounterexampleTarget := by
  constructor
  · trivial
  · exact RepositoryNativeR1LongChordCoherence_refuted

/--
Status marker.

This does not repair R1 coherence. It proves that the current native package
does not imply R1 coherence; the coherence condition must be strengthened,
renamed, restricted, or supplied externally.
-/
def R1NativeCoherenceRefutationStatus : String :=
  "REPOSITORY_NATIVE_R1_LONG_CHORD_COHERENCE_REFUTED"

end Chronos.Frontier
