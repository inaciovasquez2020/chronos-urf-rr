import Chronos.Frontier.R1R2R3IsolatedTargetsConditionalClosure
import Chronos.Frontier.R2CrossRootFaceIncidenceObstruction

namespace Chronos
namespace Frontier

def DiameterSeparationFillingConcreteConfiguration : Type :=
  R2IncidenceFaceChain

def DiameterSeparationFillingConcreteDiameterSeparated
    (chain : DiameterSeparationFillingConcreteConfiguration) : Prop :=
  r2IncidenceBoundary2 chain = r2IncidenceCrossRootBoundary

def DiameterSeparationFillingConcreteFillable
    (chain : DiameterSeparationFillingConcreteConfiguration) : Prop :=
  ¬ R2CrossRootFaceIncidenceObstruction chain

theorem diameter_separation_filling_concrete_obstruction :
    ∀ chain,
      DiameterSeparationFillingConcreteDiameterSeparated chain →
      ¬ DiameterSeparationFillingConcreteFillable chain := by
  intro chain hBoundary hLocallyDecomposable
  exact hLocallyDecomposable
    (r2_cross_root_face_incidence_obstruction chain hBoundary)

def DiameterSeparationFillingConcreteInputSurface :
    DiameterSeparationFillingObstructionInputSurface where
  Configuration := DiameterSeparationFillingConcreteConfiguration
  DiameterSeparated := DiameterSeparationFillingConcreteDiameterSeparated
  Fillable := DiameterSeparationFillingConcreteFillable
  obstruction := diameter_separation_filling_concrete_obstruction

end Frontier
end Chronos
