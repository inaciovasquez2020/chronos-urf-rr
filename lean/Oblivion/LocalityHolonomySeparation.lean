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

def LocalEquiv (G H : LabeledCFI) : Prop :=
  G.localSummary = H.localSummary

theorem localEquiv_untwisted_singleTwist
  (n : Nat) (e₀ : BaseEdge) :
  LocalEquiv (UntwistedCFI n) (SingleTwistCFI n e₀) := by
  rfl

theorem PhiH_untwisted_zero
  (n : Nat) :
  PhiH n (UntwistedCFI n) = false := by
  unfold PhiH UntwistedCFI
  simp [fundamentalCycleXorAux]

theorem PhiH_singleTwist_one
  (n : Nat) :
  PhiH (n + 1) (SingleTwistCFI (n + 1) (0, 1)) = true := by
  unfold PhiH SingleTwistCFI
  simp [fundamentalCycleXorAux]

theorem locality_holonomy_separation :
  ∀ n : Nat, ∃ G H : LabeledCFI, LocalEquiv G H ∧ PhiH (n + 1) G ≠ PhiH (n + 1) H := by
  intro n
  refine ⟨UntwistedCFI (n + 1), SingleTwistCFI (n + 1) (0, 1), ?_⟩
  constructor
  · exact localEquiv_untwisted_singleTwist (n + 1) (0, 1)
  · simp [PhiH_untwisted_zero, PhiH_singleTwist_one]

end Oblivion
