import Chronos.Frontier.UnrestrictedChronosRRStatusLock

namespace Chronos.Frontier

/--
Status marker for unrestricted H4.1/FGL.

The only repository-native status certified here is frontier-open.
-/
inductive H4FGLUnrestrictedStatus where
  | frontierOpen
  deriving DecidableEq, Repr

def h4FGLUnrestrictedStatusLock : H4FGLUnrestrictedStatus :=
  H4FGLUnrestrictedStatus.frontierOpen

def H4FGLUnrestrictedStatusLockedOpen : Prop :=
  h4FGLUnrestrictedStatusLock = H4FGLUnrestrictedStatus.frontierOpen ∧
    UnrestrictedChronosRRStatusLockedOpen

theorem h4fgl_unrestricted_status_lock_from_chronos_rr_status_lock :
    H4FGLUnrestrictedStatusLockedOpen := by
  constructor
  · rfl
  · exact unrestricted_chronos_rr_status_lock_from_obstruction_registry

def RepositoryNativeChronosRRConditionalClosurePreservesH4FGLOpenStatus
    (_h : RepositoryNativeChronosRRConditionalClosure) : Prop :=
  H4FGLUnrestrictedStatusLockedOpen

theorem repository_native_chronos_rr_conditional_closure_preserves_h4fgl_open_status
    (h : RepositoryNativeChronosRRConditionalClosure) :
    RepositoryNativeChronosRRConditionalClosurePreservesH4FGLOpenStatus h := by
  exact h4fgl_unrestricted_status_lock_from_chronos_rr_status_lock

theorem canonical_repository_native_chronos_rr_conditional_closure_preserves_h4fgl_open_status :
    RepositoryNativeChronosRRConditionalClosurePreservesH4FGLOpenStatus
      canonical_repository_native_chronos_rr_conditional_closure := by
  exact repository_native_chronos_rr_conditional_closure_preserves_h4fgl_open_status
    canonical_repository_native_chronos_rr_conditional_closure

end Chronos.Frontier
