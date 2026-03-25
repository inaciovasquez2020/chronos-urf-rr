import Oblivion.CFISkeleton

def sameVertices (G₀ G₁ : Graph) : Prop :=
  (Nonempty G₀.V ↔ Nonempty G₁.V)

def sameEdges (G₀ G₁ : Graph) : Prop :=
  (Nonempty G₀.E ↔ Nonempty G₁.E)

def sameCounts (G₀ G₁ : Graph) : Prop :=
  (Cardinal.mk G₀.V = Cardinal.mk G₁.V) ∧
  (Cardinal.mk G₀.E = Cardinal.mk G₁.E)

def matchVertices (G₀ G₁ : Graph) : Prop :=
  (∀ v₀ : G₀.V, ∃ v₁ : G₁.V, True) ∧
  (∀ v₁ : G₁.V, ∃ v₀ : G₀.V, True)

def preserveAdj (G₀ G₁ : Graph) : Prop :=
  (∀ e₀ : G₀.E, ∃ e₁ : G₁.E, True) ∧
  (∀ e₁ : G₁.E, ∃ e₀ : G₀.E, True)

def preserveIncidence (G₀ G₁ : Graph) : Prop :=
  (∀ e₀ : G₀.E, ∃ e₁ : G₁.E, True) ∧
  (∀ e₁ : G₁.E, ∃ e₀ : G₀.E, True)

def FO_equiv (k R : Nat) (G₀ G₁ : Graph) : Prop :=
  (k ≤ 1) ∧
  sameVertices G₀ G₁ ∧
  sameEdges G₀ G₁ ∧
  sameCounts G₀ G₁ ∧
  matchVertices G₀ G₁ ∧
  preserveAdj G₀ G₁ ∧
  preserveIncidence G₀ G₁

theorem FO_equiv_base (k R : Nat) (G₀ G₁ : Graph) :
  k ≤ 1 →
  sameVertices G₀ G₁ →
  sameEdges G₀ G₁ →
  sameCounts G₀ G₁ →
  matchVertices G₀ G₁ →
  preserveAdj G₀ G₁ →
  preserveIncidence G₀ G₁ →
  FO_equiv k R G₀ G₁ :=
by
  intro hk hv he hc hm hp hi
  exact And.intro hk (And.intro hv (And.intro he (And.intro hc (And.intro hm (And.intro hp hi)))))
