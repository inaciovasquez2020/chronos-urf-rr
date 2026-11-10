import Oblivion.CycleArcBallWindowBridge
import Oblivion.CycleGraphReachabilityBridge

namespace Oblivion.CycleGraphBridge

/-- The induced cycle-graph reachability ball equals its modular vertex window.
This composes previously proved graph-path/arc and arc/window equivalences.
It does not identify the window edges with a separate graph library's edge type. -/
theorem graphBall_iff_window (n r root : Nat) (v : Int) :
    graphBall n r root v ↔
      ∃ j : Nat, j ≤ 2 * r ∧
        v = Oblivion.CycleArcBridge.windowPoint n r root j := by
  calc
    graphBall n r root v ↔ Oblivion.CycleWalkBridge.arcBall n r root v :=
      graphBall_iff_arcBall n r root v
    _ ↔ Oblivion.CycleArcBridge.arcBall n r root v := Iff.rfl
    _ ↔ ∃ j : Nat, j ≤ 2 * r ∧
        v = Oblivion.CycleArcBridge.windowPoint n r root j :=
      Oblivion.CycleArcBridge.arcBall_iff_window n r root v

end Oblivion.CycleGraphBridge
