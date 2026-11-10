import Init

/-!
Research candidate only. NOT compiler-verified. Replaces the summary-only
LocalEquiv with independent local gauge equivalence on the oriented edge
windows of actual induced radius-r balls of C_n, under 3 <= n and 2*r+1 < n.

A path window has 2*r edges and 2*r+1 vertices. Its local gauge is a
function of path position; different root windows may choose different gauges.
The window-to-SimpleGraph.ball identification is mathematical here, not a
separately formalized Lean isomorphism.
-/

namespace Oblivion

abbrev BaseEdge := Nat × Nat

structure LabeledCFI where
  localSummary : Nat
  transportBit : BaseEdge → Bool

def fundamentalCycleXorAux (n : Nat) (F : LabeledCFI) : Nat → Bool → Bool
  | 0, acc => acc
  | Nat.succ j, acc =>
      let e : BaseEdge := (j, (j + 1) % n)
      fundamentalCycleXorAux n F j (xor acc (F.transportBit e))

def PhiH (n : Nat) (F : LabeledCFI) : Bool :=
  fundamentalCycleXorAux n F n false

def UntwistedCFI (n : Nat) : LabeledCFI :=
  ⟨n, fun _ => false⟩

def SingleTwistCFI (n : Nat) (e₀ : BaseEdge) : LabeledCFI :=
  ⟨n, fun e => decide (e = e₀)⟩

/-- The jth oriented edge of the induced radius-r cycle ball at root.
    Its vertices occur in the order root-r,...,root+r (mod n).
    Under 3 <= n and 2*r+1 < n this is a proper path. -/
def radiusWindowEdge (n r root j : Nat) : BaseEdge :=
  let u := (root + n - r + j) % n
  (u, (u + 1) % n)

/-- Vertex gauge along an oriented path: g(0)=0, and each step integrates
    the difference of the two edge connections. -/
def radiusPathGauge (n r root : Nat) (G H : LabeledCFI) : Nat → Bool
  | 0 => false
  | Nat.succ j =>
      xor (radiusPathGauge n r root G H j)
        (xor (G.transportBit (radiusWindowEdge n r root j))
             (H.transportBit (radiusWindowEdge n r root j)))

private theorem radiusPathGauge_step
    (n r root : Nat) (G H : LabeledCFI) (j : Nat) :
    xor (radiusPathGauge n r root G H j)
        (radiusPathGauge n r root G H (j + 1)) =
    xor (G.transportBit (radiusWindowEdge n r root j))
        (H.transportBit (radiusWindowEdge n r root j)) := by
  change xor (radiusPathGauge n r root G H j)
      (xor (radiusPathGauge n r root G H j)
        (xor (G.transportBit (radiusWindowEdge n r root j))
             (H.transportBit (radiusWindowEdge n r root j)))) = _
  cases h₀ : radiusPathGauge n r root G H j <;>
    cases h₁ : G.transportBit (radiusWindowEdge n r root j) <;>
    cases h₂ : H.transportBit (radiusWindowEdge n r root j) <;>
    simp [h₀, h₁, h₂]

/-- Genuine independent radius-r gauge equivalence. The witness at each
    root is a gauge on the 2*r+1 path vertices; it need not agree on overlaps
    with the gauges chosen at other roots. -/
def LocalEquiv (n r : Nat) (G H : LabeledCFI) : Prop :=
  G.localSummary = n ∧ H.localSummary = n ∧
  3 ≤ n ∧ 2 * r + 1 < n ∧
  ∀ root : Nat, root < n →
    ∃ g : Nat → Bool, ∀ j : Nat, j < 2 * r →
      xor (G.transportBit (radiusWindowEdge n r root j))
          (H.transportBit (radiusWindowEdge n r root j)) =
      xor (g j) (g (j + 1))

theorem localEquiv_untwisted_singleTwist
    (n r : Nat) (hn : 3 ≤ n) (hr : 2 * r + 1 < n) :
    LocalEquiv n r (UntwistedCFI n) (SingleTwistCFI n (0, 1)) := by
  refine ⟨rfl, rfl, hn, hr, ?_⟩
  intro root _
  refine ⟨radiusPathGauge n r root (UntwistedCFI n)
      (SingleTwistCFI n (0, 1)), ?_⟩
  intro j _
  exact (radiusPathGauge_step n r root
    (UntwistedCFI n) (SingleTwistCFI n (0, 1)) j).symm

private theorem fold_untwisted (n j : Nat) (acc : Bool) :
    fundamentalCycleXorAux n (UntwistedCFI n) j acc = acc := by
  induction j generalizing acc with
  | zero => rfl
  | succ j ih =>
      simpa [fundamentalCycleXorAux, UntwistedCFI] using (ih acc)

theorem PhiH_untwisted_zero (n : Nat) :
    PhiH n (UntwistedCFI n) = false := by
  simpa [PhiH] using (fold_untwisted n n false)

private theorem fold_singleTwist
    (n : Nat) (hn : 2 ≤ n) (j : Nat) (acc : Bool) :
    fundamentalCycleXorAux n (SingleTwistCFI n (0, 1)) j acc =
      xor acc (decide (0 < j)) := by
  induction j generalizing acc with
  | zero =>
      simp [fundamentalCycleXorAux]
  | succ j ih =>
      cases j with
      | zero =>
          have hmod : 1 % n = 1 := Nat.mod_eq_of_lt (by omega)
          simp [fundamentalCycleXorAux, SingleTwistCFI, hmod]
      | succ k =>
          have hstep :
              (SingleTwistCFI n (0, 1)).transportBit
                (Nat.succ k, (Nat.succ k + 1) % n) = false := by
            simp [SingleTwistCFI]
          have hfold :
              fundamentalCycleXorAux n (SingleTwistCFI n (0, 1))
                (Nat.succ (Nat.succ k)) acc =
              fundamentalCycleXorAux n (SingleTwistCFI n (0, 1))
                (Nat.succ k) acc := by
            change fundamentalCycleXorAux n (SingleTwistCFI n (0, 1))
                (Nat.succ k)
                (xor acc ((SingleTwistCFI n (0, 1)).transportBit
                  (Nat.succ k, (Nat.succ k + 1) % n))) =
              fundamentalCycleXorAux n (SingleTwistCFI n (0, 1))
                (Nat.succ k) acc
            rw [hstep]
            cases acc <;> rfl
          rw [hfold]
          simpa using (ih acc)

theorem PhiH_singleTwist_one (n : Nat) (hn : 2 ≤ n) :
    PhiH n (SingleTwistCFI n (0, 1)) = true := by
  have hp : 0 < n := by omega
  simpa [PhiH, hp] using (fold_singleTwist n hn n false)

theorem locality_holonomy_separation
    (n r : Nat) (hn : 3 ≤ n) (hr : 2 * r + 1 < n) :
    ∃ G H : LabeledCFI,
      LocalEquiv n r G H ∧ PhiH n G ≠ PhiH n H := by
  refine ⟨UntwistedCFI n, SingleTwistCFI n (0, 1), ?_, ?_⟩
  · exact localEquiv_untwisted_singleTwist n r hn hr
  · rw [PhiH_untwisted_zero, PhiH_singleTwist_one n (by omega)]
    decide

end Oblivion