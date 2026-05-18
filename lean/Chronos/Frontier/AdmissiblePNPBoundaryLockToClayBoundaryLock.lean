import Chronos.Frontier.AdmissibleH41FGLToPNPBoundaryLock

/-!
Admissible P vs NP boundary lock to Clay boundary lock.

This file closes only a boundary-lock transport theorem. It records that an
admissible P vs NP boundary lock can be carried into an explicit
`ClayStatus.frontier_open` certificate.

It does not solve or refute P vs NP, any Clay problem, Chronos-RR, H4.1/FGL,
or any unrestricted theorem target.
-/

namespace Chronos.Frontier

inductive ClayStatus where
  | frontier_open
deriving DecidableEq, Repr

structure ClayBoundaryLockTarget (M : FiberMassData) where
  pnp_boundary_lock : Nonempty (PNPBoundaryLockTarget M)
  status : ClayStatus
  status_locked : status = ClayStatus.frontier_open

def PNPBoundaryLockToClayBoundaryLockBridge
    (M : FiberMassData) : Prop :=
  Nonempty (PNPBoundaryLockTarget M) →
  Nonempty (ClayBoundaryLockTarget M)

theorem clayBoundaryLockTarget_from_pnpBoundaryLockTarget
    (M : FiberMassData)
    (h : Nonempty (PNPBoundaryLockTarget M)) :
    Nonempty (ClayBoundaryLockTarget M) := by
  exact ⟨⟨h, ClayStatus.frontier_open, rfl⟩⟩

theorem PNPBoundaryLockToClayBoundaryLockBridge_solved
    (M : FiberMassData) :
    PNPBoundaryLockToClayBoundaryLockBridge M := by
  intro h
  exact clayBoundaryLockTarget_from_pnpBoundaryLockTarget M h

def AdmissiblePNPBoundaryLockToClayBoundaryLock : Prop :=
  ∀ A : AdmissibleFiberMassData,
    Nonempty (PNPBoundaryLockTarget A.data) →
    Nonempty (ClayBoundaryLockTarget A.data)

theorem AdmissiblePNPBoundaryLockToClayBoundaryLock_solved :
    AdmissiblePNPBoundaryLockToClayBoundaryLock := by
  intro A hA
  exact clayBoundaryLockTarget_from_pnpBoundaryLockTarget A.data hA

def AdmissibleClayBoundaryLockTarget : Prop :=
  ∀ A : AdmissibleFiberMassData,
    Nonempty (ClayBoundaryLockTarget A.data)

theorem AdmissibleClayBoundaryLockTarget_solved :
    AdmissibleClayBoundaryLockTarget := by
  intro A
  exact clayBoundaryLockTarget_from_pnpBoundaryLockTarget
    A.data (AdmissiblePNPBoundaryLockTarget_solved A)

theorem clay_boundary_status_frontier_open
    (A : AdmissibleFiberMassData)
    (h : Nonempty (ClayBoundaryLockTarget A.data)) :
    ∃ T : ClayBoundaryLockTarget A.data,
      T.status = ClayStatus.frontier_open := by
  rcases h with ⟨T⟩
  exact ⟨T, T.status_locked⟩

end Chronos.Frontier
