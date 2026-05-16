import Chronos.Frontier.BulkToBoundaryNuclearitySoundness

namespace Chronos
namespace Frontier

universe u

/--
Finite detector algebra interface.

This records the finite detector-algebra input without asserting that such an
algebra has been constructed from unrestricted Einstein--matter dynamics.
-/
def FiniteDetectorAlgebra (DetectorAlgebra : Type u) : Prop :=
  Nonempty DetectorAlgebra

/--
Open frontier: finite detector algebra supplies the same uniform
bulk-to-boundary compactness translation required by
`BulkToBoundaryNuclearitySoundness`.

This is intentionally represented as a Prop-level theorem target, not as a
primitive assumption and not as an unconditional proof from finite detector data.
-/
def BoundaryNuclearityFromFiniteDetectorAlgebra : Prop :=
  ∀ (Spacetime BoundaryAlgebra BoundaryState : Type u),
    BoundaryNuclearity BoundaryAlgebra →
    BulkDeformationPushforwardCompact_wstar Spacetime BoundaryState

/--
Conditional bridge only.

If the finite-detector-algebra nuclearity frontier is supplied, then the
bulk-to-boundary nuclearity soundness frontier is available.
-/
theorem boundary_nuclearity_from_finite_detector_algebra_implies_bulk_to_boundary_nuclearity_soundness
    (h : BoundaryNuclearityFromFiniteDetectorAlgebra.{u}) :
    BulkToBoundaryNuclearitySoundness.{u} :=
by
  intro Spacetime BoundaryAlgebra BoundaryState hBoundary
  exact h Spacetime BoundaryAlgebra BoundaryState hBoundary

end Frontier
end Chronos
