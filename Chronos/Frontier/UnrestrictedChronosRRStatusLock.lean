import Chronos.Frontier.UnrestrictedChronosRRObstructionRegistry

namespace Chronos.Frontier

/--
Status marker for unrestricted Chronos-RR.

The only repository-native status certified here is frontier-open.
-/
inductive UnrestrictedChronosRRStatus where
  | frontierOpen
  deriving DecidableEq, Repr

def unrestrictedChronosRRStatusLock : UnrestrictedChronosRRStatus :=
  UnrestrictedChronosRRStatus.frontierOpen

def UnrestrictedChronosRRStatusLockedOpen : Prop :=
  unrestrictedChronosRRStatusLock = UnrestrictedChronosRRStatus.frontierOpen ∧
    unrestrictedChronosRRObstructionRegistry.Nonempty

theorem unrestricted_chronos_rr_status_lock_from_obstruction_registry :
    UnrestrictedChronosRRStatusLockedOpen := by
  constructor
  · rfl
  · exact unrestricted_chronos_rr_obstruction_registry_nonempty

def RepositoryNativeConditionalClosurePreservesUnrestrictedOpenStatus
    (_h : RepositoryNativeChronosRRConditionalClosure) : Prop :=
  UnrestrictedChronosRRStatusLockedOpen

theorem repository_native_conditional_closure_preserves_unrestricted_open_status
    (h : RepositoryNativeChronosRRConditionalClosure) :
    RepositoryNativeConditionalClosurePreservesUnrestrictedOpenStatus h := by
  exact unrestricted_chronos_rr_status_lock_from_obstruction_registry

theorem canonical_repository_native_conditional_closure_preserves_unrestricted_open_status :
    RepositoryNativeConditionalClosurePreservesUnrestrictedOpenStatus
      canonical_repository_native_chronos_rr_conditional_closure := by
  exact repository_native_conditional_closure_preserves_unrestricted_open_status
    canonical_repository_native_chronos_rr_conditional_closure

end Chronos.Frontier
