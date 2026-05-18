import Chronos.Frontier.FiniteSupportRestrictedUFEGToRestrictedH41FGL

namespace Chronos
namespace Frontier

/--
End-to-end finite-support restricted route from restricted UFEG to restricted H4.1/FGL.
This is a lock/assembly theorem only for the finite-support admissible restricted domain.
-/
theorem finite_support_restricted_end_to_end_h41_fgl
    (D : FiniteSupportRestrictedUFEGToRestrictedH41FGLData) :
    FiniteSupportRestrictedUFEG D → FiniteSupportRestrictedH41FGL D := by
  exact FiniteSupportRestrictedUFEGToRestrictedH41FGL D

/--
Named terminal lock for the finite-support restricted route.
-/
theorem FiniteSupportRestrictedEndToEndH41FGL
    (D : FiniteSupportRestrictedUFEGToRestrictedH41FGLData) :
    FiniteSupportRestrictedUFEG D → FiniteSupportRestrictedH41FGL D := by
  exact finite_support_restricted_end_to_end_h41_fgl D

end Frontier
end Chronos
