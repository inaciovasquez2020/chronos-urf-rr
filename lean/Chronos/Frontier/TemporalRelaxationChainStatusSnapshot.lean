import Chronos.Frontier.RestrictedRateThickToRecoveryRouteSurfaces

namespace Chronos
namespace Frontier

inductive TemporalRelaxationChainSurfaceStatus where
  | interfaceClosed
  | frontierOpen
  deriving DecidableEq, Repr

def temporalRelaxationChainInterfaceStatus :
    TemporalRelaxationChainSurfaceStatus :=
  TemporalRelaxationChainSurfaceStatus.interfaceClosed

def temporalRelaxationChainTheoremBoundary :
    TemporalRelaxationChainSurfaceStatus :=
  TemporalRelaxationChainSurfaceStatus.frontierOpen

theorem temporalRelaxationChain_interface_closed :
    temporalRelaxationChainInterfaceStatus =
      TemporalRelaxationChainSurfaceStatus.interfaceClosed := by
  rfl

theorem temporalRelaxationChain_theorem_boundary_open :
    temporalRelaxationChainTheoremBoundary =
      TemporalRelaxationChainSurfaceStatus.frontierOpen := by
  rfl

end Frontier
end Chronos
