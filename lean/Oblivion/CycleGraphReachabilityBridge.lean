import Oblivion.CycleWalkReachabilityBridge

namespace Oblivion.CycleGraphBridge

open Oblivion.CycleWalkBridge

/-- One clockwise or counterclockwise cycle edge. -/
def cycleAdj (n : Nat) (u v : Int) : Prop :=
  ∃ b : Bool, v = (u + signedStep b) % (n : Int)

/-- Reachability by exactly k graph edges. -/
inductive cyclePath (n : Nat) : Nat → Int → Int → Prop
  | nil (v : Int) : cyclePath n 0 v v
  | snoc {k : Nat} {u v w : Int} :
      cyclePath n k u v →
      cycleAdj n v w →
      cyclePath n (k + 1) u w

/-- Reachability within r graph edges. -/
def graphBall (n r root : Nat) (v : Int) : Prop :=
  ∃ k : Nat, k ≤ r ∧
    cyclePath n k (cyclePoint n root 0) v

private theorem cyclePoint_step
    (n root : Nat) (a : Int) (b : Bool) :
    (cyclePoint n root a + signedStep b) % (n : Int) =
      cyclePoint n root (signedStep b + a) := by
  unfold cyclePoint
  calc
    (((root : Int) + a) % (n : Int) + signedStep b) % (n : Int) =
        ((root : Int) + a + signedStep b) % (n : Int) :=
      Int.emod_add_emod _ _ _
    _ = ((root : Int) + (signedStep b + a)) % (n : Int) := by
      congr 1
      omega

/-- Convert a graph path into its signed edge sequence. -/
private theorem cyclePath_to_steps_aux
    (n root : Nat) {k : Nat} {u v : Int}
    (h : cyclePath n k u v) :
    ∀ a : Int, u = cyclePoint n root a →
      ∃ steps : List Bool,
        steps.length = k ∧
        v = cyclePoint n root (walkOffset steps + a) := by
  induction h with
  | nil u =>
      intro a hu
      refine ⟨[], rfl, ?_⟩
      simpa [walkOffset] using hu
  | @snoc k u v w hpath hedge ih =>
      intro a hu
      obtain ⟨steps, hlen, hv⟩ := ih a hu
      obtain ⟨b, hstep⟩ := hedge
      refine ⟨b :: steps, ?_, ?_⟩
      · simp only [List.length_cons, hlen, Nat.succ_eq_add_one]
      · rw [hstep, hv]
        change
          (cyclePoint n root (walkOffset steps + a) + signedStep b) %
              (n : Int) =
            cyclePoint n root ((signedStep b + walkOffset steps) + a)
        calc
          (cyclePoint n root (walkOffset steps + a) + signedStep b) %
                (n : Int) =
              cyclePoint n root (signedStep b + (walkOffset steps + a)) :=
            cyclePoint_step n root (walkOffset steps + a) b
          _ = cyclePoint n root ((signedStep b + walkOffset steps) + a) := by
            congr 1
            omega

private theorem cyclePath_to_steps
    (n root : Nat) {k : Nat} {v : Int}
    (h : cyclePath n k (cyclePoint n root 0) v) :
    ∃ steps : List Bool,
      steps.length = k ∧
      v = cyclePoint n root (walkOffset steps) := by
  obtain ⟨steps, hlen, hv⟩ :=
    cyclePath_to_steps_aux n root h 0 rfl
  refine ⟨steps, hlen, ?_⟩
  simpa using hv

/-- Convert a signed edge sequence into a graph path. -/
private theorem steps_to_cyclePath
    (n root : Nat) (steps : List Bool) :
    cyclePath n steps.length (cyclePoint n root 0)
      (cyclePoint n root (walkOffset steps)) := by
  induction steps with
  | nil =>
      exact cyclePath.nil _
  | cons b tail ih =>
      have hedge :
          cycleAdj n (cyclePoint n root (walkOffset tail))
            (cyclePoint n root (walkOffset (b :: tail))) := by
        refine ⟨b, ?_⟩
        change cyclePoint n root (signedStep b + walkOffset tail) =
          (cyclePoint n root (walkOffset tail) + signedStep b) %
            (n : Int)
        exact (cyclePoint_step n root (walkOffset tail) b).symm
      simpa only [List.length_cons, Nat.succ_eq_add_one] using
        (cyclePath.snoc ih hedge)

/-- Actual graph reachability equals signed-walk reachability. -/
theorem graphBall_iff_walkBall
    (n r root : Nat) (v : Int) :
    graphBall n r root v ↔ walkBall n r root v := by
  constructor
  · rintro ⟨k, hk, hpath⟩
    obtain ⟨steps, hlen, hv⟩ :=
      cyclePath_to_steps n root hpath
    exact ⟨steps, by omega, hv⟩
  · rintro ⟨steps, hlen, hv⟩
    refine ⟨steps.length, hlen, ?_⟩
    rw [hv]
    exact steps_to_cyclePath n root steps

/-- Actual graph reachability equals the arc ball. -/
theorem graphBall_iff_arcBall
    (n r root : Nat) (v : Int) :
    graphBall n r root v ↔ arcBall n r root v := by
  exact (graphBall_iff_walkBall n r root v).trans
    (walkBall_iff_arcBall n r root v)

end Oblivion.CycleGraphBridge
