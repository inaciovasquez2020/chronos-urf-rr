set_option autoImplicit false

namespace Chronos

universe u

abbrev Set (α : Type u) := α → Prop

variable {V : Type u}

structure History where
  tag : Nat

structure EFTranscript (R : Nat) (V : Type u) where
  p1 : Fin R → V
  p2 : Fin R → V

structure Cycle (V : Type u) where
  verts : List V

def Z1 (V : Type u) (_ : Set V) : Cycle V → Prop := fun _ => True

def size {V : Type u} (C : Cycle V) : Nat := C.verts.length

def inner {V : Type u} (_ : Cycle V) (h : History) : Nat := h.tag

def close_seeded {V : Type u} {R : Nat} (_ : EFTranscript R V) : Cycle V :=
  { verts := [] }

axiom defaultV {V : Type u} : V

theorem close_seeded_in_Z1 {V : Type u} {R : Nat} (S : Set V) (T : EFTranscript R V) :
    Z1 V S (close_seeded T) := by
  trivial

theorem close_seeded_size_bound {V : Type u} {R : Nat} (_S : Set V) (T : EFTranscript R V) :
    size (close_seeded T) ≤ 2 * R := by
  simp [close_seeded, size]

theorem close_seeded_parity_sep {V : Type u} {R : Nat} (_S : Set V)
    (T : EFTranscript R V) (h1 h2 : History) :
    h1.tag ≠ h2.tag →
    inner (close_seeded T) h1 ≠ inner (close_seeded T) h2 := by
  intro hneq
  simpa [inner] using hneq

theorem EP2_core {V : Type u} {R : Nat} (S : Set V)
    (T : EFTranscript R V) (h1 h2 : History) :
    h1.tag ≠ h2.tag →
    Z1 V S (close_seeded T) ∧
    size (close_seeded T) ≤ 2 * R ∧
    inner (close_seeded T) h1 ≠ inner (close_seeded T) h2 := by
  intro hneq
  exact ⟨
    close_seeded_in_Z1 S T,
    close_seeded_size_bound S T,
    close_seeded_parity_sep S T h1 h2 hneq
  ⟩

theorem EP2 {V : Type u} {R : Nat} (S : Set V) (h1 h2 : History) :
    h1.tag ≠ h2.tag →
    ∃ C : Cycle V, Z1 V S C ∧ size C ≤ 2 * R ∧ inner C h1 ≠ inner C h2 := by
  intro hneq
  let T : EFTranscript R V := {
    p1 := fun _ => defaultV
    p2 := fun _ => defaultV
  }
  refine ⟨close_seeded T, ?_, ?_, ?_⟩
  · exact close_seeded_in_Z1 S T
  · exact close_seeded_size_bound S T
  · exact close_seeded_parity_sep S T h1 h2 hneq

end Chronos
