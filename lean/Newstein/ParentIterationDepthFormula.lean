import Mathlib
import Newstein.ParentDepthDecrement

namespace Newstein

class HasRootFixed : Prop where
  root_in_ball : inBall_R root_G
  root_fixed : parent_G root_G = root_G
  root_dist_refl : d_T root_G root_G = 0
  depth_zero_only_at_root : ∀ x, inBall_R x → depth_G x = 0 → x = root_G

def parentIter_G : Nat → α → α
  | 0, x => x
  | j + 1, x => parent_G (parentIter_G j x)

lemma parentIter_inBall
  (hP : HasParentDistStep) :
  ∀ {x : α}, inBall_R x → ∀ j : Nat, inBall_R (parentIter_G j x)
  | x, hx, 0 => by
      simpa [parentIter_G] using hx
  | x, hx, j + 1 => by
      simpa [parentIter_G] using hP.parent_in_ball (parentIter_G j x) (parentIter_inBall hP hx j)

theorem ParentIterationDepthFormula
  (hM : HasMetricDepthCoincidence)
  (hP : HasParentDistStep)
  (hR : HasRootFixed) :
  ∀ x, inBall_R x → ∀ j : Nat, depth_G (parentIter_G j x) = Nat.max (depth_G x - j) 0 := by
  intro x hx j
  induction j with
  | zero =>
      simp [parentIter_G]
  | succ j ih =>
      let y := parentIter_G j x
      have hyBall : inBall_R y := by
        dsimp [y]
        simpa using parentIter_inBall (α := α) hP hx j
      have hyFormula : depth_G y = Nat.max (depth_G x - j) 0 := by
        dsimp [y]
        simpa using ih
      by_cases hy0 : depth_G y = 0
      · have hyRoot : y = root_G := hR.depth_zero_only_at_root y hyBall hy0
        subst hyRoot
        have hsub0 : depth_G x - j = 0 := by
          have : Nat.max (depth_G x - j) 0 = 0 := by
            rw [← hyFormula, hy0]
          simpa using this
        have hxle : depth_G x ≤ j := by
          omega
        have hsuc0 : Nat.max (depth_G x - (j + 1)) 0 = 0 := by
          have : depth_G x - (j + 1) = 0 := by
            exact Nat.sub_eq_zero_of_le (Nat.le_trans hxle (Nat.le_succ j))
          simp [this]
        have hrootDepth : depth_G root_G = 0 := by
          rw [hM.metric_depth_coincidence root_G hR.root_in_ball, hR.root_dist_refl]
        simpa [parentIter_G, hR.root_fixed, hrootDepth, hsuc0]
      · have hyNeRoot : y ≠ root_G := by
          intro hyRoot
          apply hy0
          rw [hyRoot, hM.metric_depth_coincidence root_G hR.root_in_ball, hR.root_dist_refl]
        have hdec : depth_G (parent_G y) = depth_G y - 1 := by
          exact ParentDepthDecrement (α := α) hM hP y hyNeRoot hyBall
        have hyFormula' : depth_G y = depth_G x - j := by
          simpa using hyFormula
        have hstep : depth_G (parent_G y) = depth_G x - (j + 1) := by
          rw [hdec, hyFormula']
          omega
        simpa [parentIter_G, y] using hstep

end Newstein
