import Chronos.Frontier.FiniteSupportRestrictedClayBoundaryLock

namespace Chronos
namespace Frontier

/--
Status-only terminal marker for the finite-support restricted Clay boundary lock.
This records that the restricted Clay boundary status is locked while preserving
all unrestricted frontiers.
-/
structure FiniteSupportRestrictedClayBoundaryStatusLock
    (D : FiniteSupportRestrictedUFEGToRestrictedH41FGLData) : Prop where
  clay_boundary_lock : FiniteSupportRestrictedClayBoundaryLock D
  status_locked :
    FiniteSupportRestrictedClayBoundaryStatus.restricted_boundary_locked =
      FiniteSupportRestrictedClayBoundaryStatus.restricted_boundary_locked

theorem finite_support_restricted_clay_boundary_status_lock
    (D : FiniteSupportRestrictedUFEGToRestrictedH41FGLData)
    (h : FiniteSupportRestrictedUFEG D) :
    FiniteSupportRestrictedClayBoundaryStatusLock D := by
  exact
    { clay_boundary_lock :=
        FiniteSupportRestrictedClayBoundaryLock_from_UFEG D h
      status_locked := rfl }

theorem FiniteSupportRestrictedClayBoundaryStatusLock_from_UFEG
    (D : FiniteSupportRestrictedUFEGToRestrictedH41FGLData) :
    FiniteSupportRestrictedUFEG D →
      FiniteSupportRestrictedClayBoundaryStatusLock D := by
  intro h
  exact finite_support_restricted_clay_boundary_status_lock D h

end Frontier
end Chronos
