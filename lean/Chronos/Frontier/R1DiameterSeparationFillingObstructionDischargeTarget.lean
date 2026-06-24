import Chronos.Frontier.R1ConcreteNewsteinFGLToNativeMapInputContract
import Chronos.Frontier.R1R2R3FiniteDataPromotionAssumptions

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
A finite-data promotion assumption conditionally supplies the diameter-separation
filling-obstruction discharge target for the concrete Newstein/FGL source object.

This does not prove the promotion assumption.
-/
def r1_diameter_separation_filling_obstruction_discharge_target_from_finite_data_promotion_assumption
    (x : R1ConcreteNewsteinFGLGeometrySourceObject)
    (hR2 : R2FiniteDataToGeneralProofPromotionAssumption) :
    R1DiameterSeparationFillingObstructionDischargeTarget where
  source := x
  r1DiameterSeparationFillingObstruction :=
    DiameterSeparationFillingObstructionProofTarget
  diameterSeparationFillingObstructionEvidence :=
    r2_native_target_from_finite_data_promotion_assumption hR2

theorem r1_diameter_separation_filling_obstruction_discharge_target_from_finite_data_promotion_assumption_target_eq
    (x : R1ConcreteNewsteinFGLGeometrySourceObject)
    (hR2 : R2FiniteDataToGeneralProofPromotionAssumption) :
    (r1_diameter_separation_filling_obstruction_discharge_target_from_finite_data_promotion_assumption x hR2).r1DiameterSeparationFillingObstruction =
      DiameterSeparationFillingObstructionProofTarget := by
  rfl

/--
The active boundary is that diameter-separation filling obstruction has not yet
been discharged for the concrete Newstein/FGL source object.
-/
def r1_diameter_separation_filling_obstruction_discharge_target_boundary : String :=
  "NO_DISCHARGED_R1_DIAMETER_SEPARATION_FILLING_OBSTRUCTION_FOR_CONCRETE_NEWSTEIN_FGL_SOURCE_OBJECT"

end Frontier
end Chronos
