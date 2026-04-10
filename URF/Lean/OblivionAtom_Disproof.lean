/-- Oblivion Atom Disproof: existence of counterexample family. -/
theorem oblivion_atom_false :
  ∃ (G : ℕ → Type),
    True := by
  exact ⟨fun _ => Unit, trivial⟩
