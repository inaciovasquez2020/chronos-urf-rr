import Init

/-!
Cycle arc-ball/window identification in an integer residue coordinate.
This does not import any of the repository's placeholder graph-ball modules.
Mathematical identification of arc-ball with graph-reachability ball is a
separate obligation, not claimed by this module.
-/

namespace Oblivion.CycleArcBridge

/-- The residue vertex reached from `root` by a signed displacement. -/
def cyclePoint (n root : Nat) (offset : Int) : Int :=
  ((root : Int) + offset) % (n : Int)

/-- The union of the two oriented arcs of length at most `r`. -/
def arcBall (n r root : Nat) (v : Int) : Prop :=
  ∃ d : Nat, d ≤ r ∧
    (v = cyclePoint n root (d : Int) ∨
     v = cyclePoint n root (-(d : Int)))

/-- Vertex in position `j` of the oriented path window. -/
def windowPoint (n r root j : Nat) : Int :=
  cyclePoint n root ((j : Int) - (r : Int))

/-- Every bounded arc displacement occurs at a bounded path-window index. -/
theorem arcBall_implies_window
    (n r root : Nat) (v : Int) (hv : arcBall n r root v) :
    ∃ j : Nat, j ≤ 2 * r ∧ v = windowPoint n r root j := by
  rcases hv with ⟨d, hd, hforward | hbackward⟩
  · refine ⟨r + d, by omega, ?_⟩
    have harg : ((r + d : Nat) : Int) - (r : Int) = (d : Int) := by omega
    simpa only [windowPoint, harg] using hforward
  · refine ⟨r - d, by omega, ?_⟩
    have harg : ((r - d : Nat) : Int) - (r : Int) = -(d : Int) := by omega
    simpa only [windowPoint, harg] using hbackward

/-- Every path-window vertex is within at most `r` arc steps of the root. -/
theorem window_implies_arcBall
    (n r root j : Nat) (hj : j ≤ 2 * r) :
    arcBall n r root (windowPoint n r root j) := by
  by_cases h : j ≤ r
  · refine ⟨r - j, by omega, Or.inr ?_⟩
    have harg : (j : Int) - (r : Int) = -((r - j : Nat) : Int) := by omega
    simp only [windowPoint, harg]
  · have h' : r ≤ j := by omega
    refine ⟨j - r, by omega, Or.inl ?_⟩
    have harg : (j : Int) - (r : Int) = ((j - r : Nat) : Int) := by omega
    simp only [windowPoint, harg]

/-- Exact membership equivalence for the arc-distance neighborhood. -/
theorem arcBall_iff_window
    (n r root : Nat) (v : Int) :
    arcBall n r root v ↔
      ∃ j : Nat, j ≤ 2 * r ∧ v = windowPoint n r root j := by
  constructor
  · exact arcBall_implies_window n r root v
  · rintro ⟨j, hj, rfl⟩
    exact window_implies_arcBall n r root j hj

end Oblivion.CycleArcBridge
