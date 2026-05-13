import Chronos.Frontier.ChronosRRRepositoryNativeConditionalClosure

namespace Chronos.Frontier

/--
Registry of remaining obstructions separating the repository-native
conditional Chronos-RR surface from unrestricted Chronos-RR.
-/
inductive UnrestrictedChronosRRObstruction where
  | missingUnrestrictedDepthBridge
  | missingUnrestrictedUniversalFiberEntropyGap
  | missingSemanticRankRateToFiberEntropySoundness
  | repositoryNativeOnly
  deriving DecidableEq, Repr

def unrestrictedChronosRRObstructionRegistry :
    List UnrestrictedChronosRRObstruction :=
  [
    UnrestrictedChronosRRObstruction.missingUnrestrictedDepthBridge,
    UnrestrictedChronosRRObstruction.missingUnrestrictedUniversalFiberEntropyGap,
    UnrestrictedChronosRRObstruction.missingSemanticRankRateToFiberEntropySoundness,
    UnrestrictedChronosRRObstruction.repositoryNativeOnly
  ]

theorem unrestricted_chronos_rr_obstruction_registry_nonempty :
    unrestrictedChronosRRObstructionRegistry.Nonempty := by
  simp [unrestrictedChronosRRObstructionRegistry]

def RepositoryNativeConditionalClosureHasRemainingUnrestrictedObstruction
    (_h : RepositoryNativeChronosRRConditionalClosure) : Prop :=
  unrestrictedChronosRRObstructionRegistry.Nonempty

theorem repository_native_conditional_closure_has_remaining_unrestricted_obstruction
    (h : RepositoryNativeChronosRRConditionalClosure) :
    RepositoryNativeConditionalClosureHasRemainingUnrestrictedObstruction h := by
  exact unrestricted_chronos_rr_obstruction_registry_nonempty

theorem canonical_repository_native_conditional_closure_has_remaining_unrestricted_obstruction :
    RepositoryNativeConditionalClosureHasRemainingUnrestrictedObstruction
      canonical_repository_native_chronos_rr_conditional_closure := by
  exact repository_native_conditional_closure_has_remaining_unrestricted_obstruction
    canonical_repository_native_chronos_rr_conditional_closure

end Chronos.Frontier
