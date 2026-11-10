import Init

namespace Oblivion.CycleWalkBridge

def cyclePoint (n root : Nat) (offset : Int) : Int :=
  ((root : Int) + offset) % (n : Int)

def arcBall (n r root : Nat) (v : Int) : Prop :=
  ∃ d : Nat, d ≤ r ∧
    (v = cyclePoint n root (d : Int) ∨
     v = cyclePoint n root (-(d : Int)))

def signedStep : Bool → Int
  | true => 1
  | false => -1

def walkOffset : List Bool → Int
  | [] => 0
  | b :: bs => signedStep b + walkOffset bs

/-- Operational reachability by oriented unit steps. -/
def walkBall (n r root : Nat) (v : Int) : Prop :=
  ∃ steps : List Bool, steps.length ≤ r ∧
    v = cyclePoint n root (walkOffset steps)

theorem walkOffset_bounds (steps : List Bool) :
    -((steps.length : Nat) : Int) ≤ walkOffset steps ∧
      walkOffset steps ≤ (steps.length : Int) := by
  induction steps with
  | nil => simp [walkOffset]
  | cons b t ih =>
      cases b <;>
        simp only [walkOffset, signedStep, List.length_cons] <;>
        omega

def forwardSteps : Nat → List Bool
  | 0 => []
  | k + 1 => true :: forwardSteps k

def backwardSteps : Nat → List Bool
  | 0 => []
  | k + 1 => false :: backwardSteps k

theorem forwardSteps_length (d : Nat) :
    (forwardSteps d).length = d := by
  induction d with
  | zero => rfl
  | succ d ih => simp [forwardSteps, ih]

theorem backwardSteps_length (d : Nat) :
    (backwardSteps d).length = d := by
  induction d with
  | zero => rfl
  | succ d ih => simp [backwardSteps, ih]

theorem forwardSteps_offset (d : Nat) :
    walkOffset (forwardSteps d) = (d : Int) := by
  induction d with
  | zero => rfl
  | succ d ih =>
      change (1 : Int) + walkOffset (forwardSteps d) =
        ((d + 1 : Nat) : Int)
      rw [ih]
      omega

theorem backwardSteps_offset (d : Nat) :
    walkOffset (backwardSteps d) = -(d : Int) := by
  induction d with
  | zero => rfl
  | succ d ih =>
      change (-1 : Int) + walkOffset (backwardSteps d) =
        -((d + 1 : Nat) : Int)
      rw [ih]
      omega

theorem walkBall_implies_arcBall
    (n r root : Nat) (v : Int)
    (hv : walkBall n r root v) :
    arcBall n r root v := by
  rcases hv with ⟨steps, hlen, hv⟩
  obtain ⟨hlow, hhigh⟩ := walkOffset_bounds steps
  by_cases hs : 0 ≤ walkOffset steps
  · refine ⟨(walkOffset steps).toNat, by omega, Or.inl ?_⟩
    have hc :
        (((walkOffset steps).toNat : Nat) : Int) =
          walkOffset steps := by omega
    simpa only [hc] using hv
  · refine ⟨(-walkOffset steps).toNat, by omega, Or.inr ?_⟩
    have hc :
        -((((-walkOffset steps).toNat : Nat) : Int)) =
          walkOffset steps := by omega
    simpa only [hc] using hv

theorem arcBall_implies_walkBall
    (n r root : Nat) (v : Int)
    (hv : arcBall n r root v) :
    walkBall n r root v := by
  rcases hv with ⟨d, hd, hf | hb⟩
  · refine ⟨forwardSteps d, ?_, ?_⟩
    · simpa only [forwardSteps_length] using hd
    · simpa only [forwardSteps_offset] using hf
  · refine ⟨backwardSteps d, ?_, ?_⟩
    · simpa only [backwardSteps_length] using hd
    · simpa only [backwardSteps_offset] using hb

theorem walkBall_iff_arcBall
    (n r root : Nat) (v : Int) :
    walkBall n r root v ↔ arcBall n r root v := by
  constructor
  · exact walkBall_implies_arcBall n r root v
  · exact arcBall_implies_walkBall n r root v

end Oblivion.CycleWalkBridge
