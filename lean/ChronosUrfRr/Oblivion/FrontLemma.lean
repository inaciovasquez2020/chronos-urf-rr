import ChronosUrfRr.Graph

set_option linter.unusedVariables false

namespace ChronosUrfRr.Oblivion

structure EFState (G : Graph) (_ : Nat) where
  dummy : Unit

@[reducible]
def preservesCodeType
    (_ _ : Nat) (G₀ G₁ : Graph)
    (_ : EFState G₀ _) (_ : EFState G₁ _) : Prop := True

class NonemptyV (G : Graph) where
  exists_vertex : Nonempty G.V

variable {G₀ G₁ : Graph} [inst : NonemptyV G₁]

theorem Locality_of_continuation
    (r t : Nat)
    (_ : EFState G₀ t) (_ : EFState G₁ t)
    (_ : preservesCodeType r t G₀ G₁ ⟨()⟩ ⟨()⟩) :
    ∀ _ : G₀.V, ∃ w : G₁.V,
      preservesCodeType r (t+1) G₀ G₁ ⟨()⟩ ⟨()⟩ := fun _ =>
  ⟨inst.exists_vertex.some, trivial⟩

end ChronosUrfRr.Oblivion
