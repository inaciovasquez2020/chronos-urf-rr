/-
Chronos/URF Gravity Open Problem Lock

Status:
  OPEN_PROBLEM_LOCK_ONLY

Purpose:
  Preserve the conditional boundary of ConditionalQLCollapseGate.

Locked boundaries:
  A3 remains an assumption.
  A4 remains a restricted trapped-surface replacement.
  QL_CollapseGate remains conditional on A1--A6.
  UniversalBoundaryCompactness remains replaced by BoundaryCompactness(FΛ).

This file is a status-lock artifact only.
-/

namespace Chronos
namespace Frontier
namespace GravityOpenProblemLock

inductive GravityBoundaryStatus where
  | openProblemLockOnly
deriving DecidableEq, Repr

inductive GravityLockedItem where
  | A3WeakCosmicCensorshipAssumption
  | A4RestrictedTrappedSurfaceReplacement
  | QLCollapseGateConditionalOnly
  | BoundaryCompactnessFiniteDetectorOnly
deriving DecidableEq, Repr

structure OpenProblemLock where
  status : GravityBoundaryStatus
  keepsA3AsAssumption : Prop
  keepsA4AsRestrictedReplacement : Prop
  keepsQLGateConditional : Prop
  keepsUniversalBoundaryCompactnessReplaced : Prop

def gravityOpenProblemLock : OpenProblemLock where
  status := GravityBoundaryStatus.openProblemLockOnly
  keepsA3AsAssumption := True
  keepsA4AsRestrictedReplacement := True
  keepsQLGateConditional := True
  keepsUniversalBoundaryCompactnessReplaced := True

theorem gravity_open_problem_lock_preserves_A3 :
    gravityOpenProblemLock.keepsA3AsAssumption := by
  trivial

theorem gravity_open_problem_lock_preserves_A4 :
    gravityOpenProblemLock.keepsA4AsRestrictedReplacement := by
  trivial

theorem gravity_open_problem_lock_preserves_conditional_gate :
    gravityOpenProblemLock.keepsQLGateConditional := by
  trivial

theorem gravity_open_problem_lock_preserves_boundary_replacement :
    gravityOpenProblemLock.keepsUniversalBoundaryCompactnessReplaced := by
  trivial

end GravityOpenProblemLock
end Frontier
end Chronos
