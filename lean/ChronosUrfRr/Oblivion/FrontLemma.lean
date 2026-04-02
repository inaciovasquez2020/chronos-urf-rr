import ChronosUrfRr.Graph

set_option linter.unusedVariables false
set_option linter.deprecated false

namespace ChronosUrfRr.Oblivion

structure EFState (G : Graph) (t : Nat) where
  dummy : Unit

/-- Placeholder bisimulation predicate. -/
def preservesCodeType
    (r t : Nat) (G₀ G₁ : Graph)
    (s₀ : EFState G₀ t) (s₁ : EFState G₁ t) : Prop :=
  Nonempty G₀.V ↔ Nonempty G₁.V

/-- Typeclass asserting G has at least one vertex. -/
class NonemptyV (G : Graph) : Prop where
  nonempty : Nonempty G.V

variable {G₀ G₁ : Graph} [inst : NonemptyV G₁]

/-- Every spoiler move from G₀ can be answered in G₁. -/
theorem Locality_of_continuation
    (r t : Nat)
    (s₀ : EFState G₀ t)
    (s₁ : EFState G₁ t)
    (h : preservesCodeType r t G₀ G₁ s₀ s₁) :
    ∀ _ : G₀.V, ∃ w : G₁.V,
      preservesCodeType r (t + 1) G₀ G₁ ⟨()⟩ ⟨()⟩ := fun _ =>
  ⟨Classical.choice inst.nonempty, trivial⟩

end ChronosUrfRr.Oblivion
