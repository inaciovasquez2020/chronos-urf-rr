namespace Oblivion

abbrev BaseEdge := Nat × Nat

structure LabeledCFI where
  transportBit : BaseEdge → Bool

def fundamentalCycleXor (n : Nat) (F : LabeledCFI) : Bool :=
  let rec go (i : Nat) (acc : Bool) :=
    match i with
    | 0 => acc
    | Nat.succ j =>
        let e : BaseEdge := (j, (j + 1) % n)
        go j (xor acc (F.transportBit e))
  go n false

def PhiH (n : Nat) (F : LabeledCFI) : Bool :=
  fundamentalCycleXor n F

theorem gadgetRelabeling_preserves_PhiH
  (n : Nat) (F F' : LabeledCFI)
  (h : ∀ e, F.transportBit e = F'.transportBit e) :
  PhiH n F = PhiH n F' := by
  unfold PhiH fundamentalCycleXor
  simp [h]

def UntwistedCFI : LabeledCFI :=
  ⟨fun _ => false⟩

def SingleTwistCFI (e₀ : BaseEdge) : LabeledCFI :=
  ⟨fun e => decide (e = e₀)⟩

end Oblivion
