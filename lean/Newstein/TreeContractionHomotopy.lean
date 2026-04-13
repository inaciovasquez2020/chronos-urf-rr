import Mathlib
import Newstein.ParentIterationToRoot

namespace Newstein

theorem TreeContractionHomotopy
  (hM : HasMetricDepthCoincidence)
  (hP : HasParentDistStep)
  (hR : HasRootFixed) :
  ∀ x, inBall_R x → ∃ n : Nat, parentIter_G n x = root_G := by
  intro x hx
  refine ⟨depth_G x, ?_⟩
  exact ParentIterationToRoot (α := α) hM hP hR x hx

end Newstein
