import Chronos.Frontier.ConcreteR1R2R3InputSurfacesReceipt
import Chronos.Frontier.NonFactorisationConcreteInputSurface

namespace Chronos
namespace Frontier

def ConcreteR1R2R3NonFactorisationInputSurfacesReceipt : Prop :=
  ConcreteR1R2R3InputSurfacesReceipt ∧
    NonFactorisationProofTarget

theorem concrete_r1_r2_r3_nonfactorisation_input_surfaces_receipt :
    ConcreteR1R2R3NonFactorisationInputSurfacesReceipt := by
  exact ⟨
    concrete_r1_r2_r3_input_surfaces_receipt,
    ⟨NonFactorisationConcreteInputSurface⟩⟩

end Frontier
end Chronos
