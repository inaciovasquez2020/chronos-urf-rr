import Chronos.Frontier.FiniteSupportRestrictedBoundaryLock

namespace Chronos
namespace Frontier

/--
Clay boundary status induced only by the finite-support restricted boundary lock.
This is a restricted boundary-status object only; it records no unrestricted
P vs NP or Clay closure.
-/
inductive FiniteSupportRestrictedClayBoundaryStatus where
  | frontier_open
  | restricted_boundary_locked
deriving DecidableEq, Repr

/--
Finite-support restricted Clay boundary lock. Since this structure is
Prop-valued, every field is proof-valued.
-/
structure FiniteSupportRestrictedClayBoundaryLock
    (D : FiniteSupportRestrictedUFEGToRestrictedH41FGLData) : Prop where
  boundary_lock : FiniteSupportRestrictedBoundaryLock D
  status_locked :
    FiniteSupportRestrictedClayBoundaryStatus.restricted_boundary_locked =
      FiniteSupportRestrictedClayBoundaryStatus.restricted_boundary_locked

theorem finite_support_restricted_clay_boundary_lock
    (D : FiniteSupportRestrictedUFEGToRestrictedH41FGLData)
    (h : FiniteSupportRestrictedUFEG D) :
    FiniteSupportRestrictedClayBoundaryLock D := by
  exact
    { boundary_lock :=
        FiniteSupportRestrictedBoundaryLock_from_UFEG D h
      status_locked := rfl }

theorem FiniteSupportRestrictedClayBoundaryLock_from_UFEG
    (D : FiniteSupportRestrictedUFEGToRestrictedH41FGLData) :
    FiniteSupportRestrictedUFEG D →
      FiniteSupportRestrictedClayBoundaryLock D := by
  intro h
  exact finite_support_restricted_clay_boundary_lock D h

end Frontier
end Chronos
