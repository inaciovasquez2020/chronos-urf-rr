import Chronos.Frontier.UniformPositiveFiberMassFloorTarget

namespace Chronos
namespace Frontier

/--
A finite-support certificate for the abstract uniform positive fiber-mass
floor target.

This is intentionally restricted: it assumes the floor as explicit finite
support data and only converts that data into the target surface.
-/
def FiniteSupportUniformFloorCertificate
    (D : FiberMassDomain) : Prop :=
  ∃ epsilon : ℝ,
    0 < epsilon ∧
      ∀ x : D.Fiber, D.admissible x → epsilon ≤ D.mass x

theorem finite_support_uniform_floor_to_target
    (D : FiberMassDomain)
    (h : FiniteSupportUniformFloorCertificate D) :
    UniformPositiveFiberMassFloor D := by
  exact h

theorem finite_support_uniform_floor_resolves_sink
    (D : FiberMassDomain)
    (h : FiniteSupportUniformFloorCertificate D) :
    UniformPositiveFiberMassSinkResolution D := by
  exact uniform_positive_floor_closure_resolves_sink D
    (finite_support_uniform_floor_to_target D h)

def FiniteSupportUniformFloorToTargetStatus : String :=
  "FINITE_SUPPORT_TARGET_CLOSURE_ONLY"

def FiniteSupportUniformFloorToTargetBoundary : String :=
  "Does not prove a finite-support-to-admissible-domain lift or unrestricted UFEG."

end Frontier
end Chronos
