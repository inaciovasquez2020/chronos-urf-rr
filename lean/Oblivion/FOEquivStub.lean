import Oblivion.CFISkeleton

def sameVertices (G₀ G₁ : Graph) : Prop :=
  (Nonempty G₀.V ↔ Nonempty G₁.V)

def sameEdges (G₀ G₁ : Graph) : Prop :=
  (Nonempty G₀.E ↔ Nonempty G₁.E)

def sameCounts (G₀ G₁ : Graph) : Prop :=
  (Cardinal.mk G₀.V = Cardinal.mk G₁.V) ∧
  (Cardinal.mk G₀.E = Cardinal.mk G₁.E)

def degree (G : Graph) (v : G.V) : Nat :=
  0  -- placeholder

def sameDegreeProfile (G₀ G₁ : Graph) : Prop :=
  True  -- placeholder for degree multiset equality

def FO_equiv (k R : Nat) (G₀ G₁ : Graph) : Prop :=
  (k ≤ 1) ∧
  sameVertices G₀ G₁ ∧
  sameEdges G₀ G₁ ∧
  sameCounts G₀ G₁ ∧
  sameDegreeProfile G₀ G₁

theorem FO_equiv_base (k R : Nat) (G₀ G₁ : Graph) :
  k ≤ 1 →
  sameVertices G₀ G₁ →
  sameEdges G₀ G₁ →
  sameCounts G₀ G₁ →
  sameDegreeProfile G₀ G₁ →
  FO_equiv k R G₀ G₁ :=
by
  intro hk hv he hc hd
  exact And.intro hk (And.intro hv (And.intro he (And.intro hc hd)))
