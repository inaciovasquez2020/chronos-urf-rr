import Chronos.Frontier.LongChordExclusionConcreteInputSurface
import Chronos.Frontier.DiameterSeparationFillingConcreteInputSurface
import Chronos.Frontier.UniformLocalTypeCapacityConcreteInputSurface

namespace Chronos
namespace Frontier

def ConcreteR1R2R3InputSurfacesReceipt : Prop :=
  LongChordExclusionProofTarget ∧
    DiameterSeparationFillingObstructionProofTarget ∧
      UniformLocalTypeCapacityProofTarget

theorem concrete_r1_r2_r3_input_surfaces_receipt :
    ConcreteR1R2R3InputSurfacesReceipt := by
  exact ⟨
    ⟨LongChordExclusionConcreteInputSurface⟩,
    ⟨⟨DiameterSeparationFillingConcreteInputSurface⟩,
      ⟨UniformLocalTypeCapacityConcreteInputSurface⟩⟩⟩

end Frontier
end Chronos
