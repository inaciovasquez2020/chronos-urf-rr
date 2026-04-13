import Mathlib
import Newstein.ParentIterationDepthFormula

namespace Newstein

theorem ParentIterationToRoot
  (hM : HasMetricDepthCoincidence)
  (hP : HasParentDistStep)
  (hR : HasRootFixed) :
  ∀ x, inBall_R x → parentIter_G (depth_G x) x = root_G := by
  intro x hx
  have hdepth :
      depth_G (parentIter_G (depth_G x) x) =
        Nat.max (depth_G x - depth_G x) 0 := by
    simpa using ParentIterationDepthFormula (α := α) hM hP hR x hx (depth_G x)
  have hzero :
      depth_G (parentIter_G (depth_G x) x) = 0 := by
    simpa using hdepth
  have hin :
      inBall_R (parentIter_G (depth_G x) x) := by
    simpa using parentIter_inBall (α := α) hP hx (depth_G x)
  exact hR.depth_zero_only_at_root _ hin hzero

end Newstein
