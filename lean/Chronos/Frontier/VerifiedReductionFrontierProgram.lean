import Chronos.Frontier.LyapunovCertificateUnrestrictedObstruction

/-!
Verified reduction-and-frontier program.

This file records the current Chronos/URF reduction state after the
Lyapunov certificate obstruction.

Boundary: status/index layer only; no admissible replacement domain is
constructed here.
-/

namespace Chronos
namespace Frontier
namespace VerifiedReductionFrontierProgram

inductive ClosureStatus where
  | closed
  | obstructed
  | frontierOpen
  deriving DecidableEq, Repr

inductive FrontierTarget where
  | admissibleDomainConstruction
  deriving DecidableEq, Repr

structure ProgramStage where
  name : String
  status : ClosureStatus

def finiteRegisteredHyperbolicRateThickSurface : ProgramStage where
  name := "finite registered hyperbolic rate-thick surface"
  status := ClosureStatus.closed

def lyapunovFiberBoundRoute : ProgramStage where
  name := "Lyapunov fiber-bound route"
  status := ClosureStatus.closed

def lyapunovFiberBoundDataCertificate : ProgramStage where
  name := "Lyapunov fiber-bound data certificate"
  status := ClosureStatus.closed

def unrestrictedLyapunovCertificateConstruction : ProgramStage where
  name := "unrestricted Lyapunov certificate construction"
  status := ClosureStatus.obstructed

def admissibleDomainConstruction : ProgramStage where
  name := "admissible-domain construction excluding zero-gap systems"
  status := ClosureStatus.frontierOpen

def currentProgram : List ProgramStage :=
  [
    finiteRegisteredHyperbolicRateThickSurface,
    lyapunovFiberBoundRoute,
    lyapunovFiberBoundDataCertificate,
    unrestrictedLyapunovCertificateConstruction,
    admissibleDomainConstruction
  ]

def nextFrontier : FrontierTarget :=
  FrontierTarget.admissibleDomainConstruction

theorem next_frontier_is_admissible_domain_construction :
    nextFrontier = FrontierTarget.admissibleDomainConstruction := by
  rfl

theorem unrestricted_lyapunov_certificate_obstruction_is_imported :
    LyapunovCertificateUnrestrictedObstruction.unrestricted_LyapunovFiberBoundData_false =
      LyapunovCertificateUnrestrictedObstruction.unrestricted_LyapunovFiberBoundData_false := by
  rfl

theorem current_program_has_five_stages :
    currentProgram.length = 5 := by
  rfl

end VerifiedReductionFrontierProgram
end Frontier
end Chronos
