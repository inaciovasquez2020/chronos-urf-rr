import Chronos.Frontier.AdmissiblePNPBoundaryLockToClayBoundaryLock

/-!
Terminal admissible boundary-chain certificate.

This file packages the completed admissible chain:

  AdmissibleFiberMassData
    → RateThickFiberCoercivityTarget
    → UniversalFiberEntropyGapTarget
    → ChronosRRTarget
    → H41FGLTarget
    → PNPBoundaryLockTarget
    → ClayBoundaryLockTarget

as a final boundary certificate.

It does not promote `ClayStatus.frontier_open` to a solved Clay theorem.
-/

namespace Chronos.Frontier

def TerminalAdmissibleBoundaryChainCertificate : Prop :=
  ∀ A : AdmissibleFiberMassData,
    ∃ C : ClayBoundaryLockTarget A.data,
      C.status = ClayStatus.frontier_open

theorem terminalCertificate_from_clayBoundaryLockTarget
    (A : AdmissibleFiberMassData)
    (h : Nonempty (ClayBoundaryLockTarget A.data)) :
    ∃ C : ClayBoundaryLockTarget A.data,
      C.status = ClayStatus.frontier_open := by
  rcases h with ⟨C⟩
  exact ⟨C, C.status_locked⟩

theorem TerminalAdmissibleBoundaryChainCertificate_solved :
    TerminalAdmissibleBoundaryChainCertificate := by
  intro A
  exact terminalCertificate_from_clayBoundaryLockTarget
    A (AdmissibleClayBoundaryLockTarget_solved A)

inductive TerminalBoundaryChainStatus where
  | boundary_certificate_closed
  | theorem_promotion_blocked
deriving DecidableEq, Repr

structure TerminalBoundaryChainAudit where
  certificate : TerminalAdmissibleBoundaryChainCertificate
  pnp_status : PNPStatus
  pnp_status_locked : pnp_status = PNPStatus.frontier_open
  clay_status : ClayStatus
  clay_status_locked : clay_status = ClayStatus.frontier_open
  terminal_status : TerminalBoundaryChainStatus
  terminal_status_locked :
    terminal_status = TerminalBoundaryChainStatus.boundary_certificate_closed

theorem TerminalBoundaryChainAudit_solved :
    Nonempty TerminalBoundaryChainAudit := by
  exact ⟨
    { certificate := TerminalAdmissibleBoundaryChainCertificate_solved
      pnp_status := PNPStatus.frontier_open
      pnp_status_locked := rfl
      clay_status := ClayStatus.frontier_open
      clay_status_locked := rfl
      terminal_status := TerminalBoundaryChainStatus.boundary_certificate_closed
      terminal_status_locked := rfl }
  ⟩

end Chronos.Frontier
