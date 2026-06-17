import Chronos.Frontier.R1ConcreteNewsteinFGLToNativeMapInputContract

namespace Chronos
namespace Frontier

/--
Discharge target for the `r1DiameterSeparationFillingObstruction` field of the
native-map input contract.

This records the weakest current target for diameter-separation filling
obstruction: a concrete source object, a named proposition, and evidence for
that proposition. It does not supply such evidence for any concrete source
object.
-/
structure R1DiameterSeparationFillingObstructionDischargeTarget : Type where
  source : R1ConcreteNewsteinFGLGeometrySourceObject
  r1DiameterSeparationFillingObstruction : Prop
  diameterSeparationFillingObstructionEvidence : r1DiameterSeparationFillingObstruction

/--
The active boundary is that diameter-separation filling obstruction has not yet
been discharged for the concrete Newstein/FGL source object.
-/
def r1_diameter_separation_filling_obstruction_discharge_target_boundary : String :=
  "NO_DISCHARGED_R1_DIAMETER_SEPARATION_FILLING_OBSTRUCTION_FOR_CONCRETE_NEWSTEIN_FGL_SOURCE_OBJECT"

end Frontier
end Chronos
