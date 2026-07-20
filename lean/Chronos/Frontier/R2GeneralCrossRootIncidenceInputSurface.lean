import Chronos.Frontier.R1R2R3IsolatedTargetsConditionalClosure
import Chronos.Frontier.R2GeneralCrossRootIncidenceTarget

namespace Chronos
namespace Frontier

namespace R2GeneralCrossRootIncidenceSystem

/--
Any nonvacuous general cross-root incidence theorem produces an R2 obstruction
input surface.

This bridge no longer depends on the finite triangulated-cylinder enumeration:
the finite packet is only one possible instance of the abstract system.
-/
def obstructionInputSurface
    (S : R2GeneralCrossRootIncidenceSystem)
    (hTarget : S.NonvacuousTarget) :
    DiameterSeparationFillingObstructionInputSurface where
  Configuration := S.Chain
  DiameterSeparated := S.boundaryMatches
  Fillable := fun chain => ¬ S.CrossRootWitness chain
  obstruction := by
    intro chain hBoundary hNoCrossRootWitness
    exact hNoCrossRootWitness (hTarget.2 chain hBoundary)

/--
The general cross-root theorem supplies a nonempty R2 obstruction-input
surface.
-/
theorem obstructionInputSurface_nonempty
    (S : R2GeneralCrossRootIncidenceSystem)
    (hTarget : S.NonvacuousTarget) :
    Nonempty DiameterSeparationFillingObstructionInputSurface :=
  ⟨S.obstructionInputSurface hTarget⟩

end R2GeneralCrossRootIncidenceSystem

/--
Concrete specialization of the general bridge to the checked finite incidence
packet.
-/
def r2IncidenceGeneralCrossRootInputSurface :
    DiameterSeparationFillingObstructionInputSurface :=
  r2IncidenceGeneralCrossRootSystem.obstructionInputSurface
    r2_incidence_general_cross_root_target

theorem r2_incidence_general_cross_root_input_surface_nonempty :
    Nonempty DiameterSeparationFillingObstructionInputSurface :=
  ⟨r2IncidenceGeneralCrossRootInputSurface⟩

/--
A nonvacuous theorem for any general cross-root incidence system is sufficient
for the repository's current R2 native obstruction proof target.
-/
theorem general_cross_root_incidence_to_r2_native_obstruction_target
    (S : R2GeneralCrossRootIncidenceSystem)
    (hTarget : S.NonvacuousTarget) :
    DiameterSeparationFillingObstructionProofTarget :=
  S.obstructionInputSurface_nonempty hTarget

/--
The checked finite incidence packet now reaches the repository's current R2
native obstruction proof target through the general geometric bridge.
-/
theorem r2_incidence_packet_reaches_native_obstruction_target :
    DiameterSeparationFillingObstructionProofTarget :=
  general_cross_root_incidence_to_r2_native_obstruction_target
    r2IncidenceGeneralCrossRootSystem
    r2_incidence_general_cross_root_target

end Frontier
end Chronos
