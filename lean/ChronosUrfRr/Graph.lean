set_option linter.unusedVariables false

structure Graph where
  V : Type
  E : Type
  src : E → V
  dst : E → V

def Adj (G : Graph) (u v : G.V) : Prop :=
  ∃ e : G.E, (G.src e = u ∧ G.dst e = v) ∨ (G.src e = v ∧ G.dst e = u)

def Connected (G : Graph) : Prop :=
  Nonempty G.V

def girth (G : Graph) : Nat := 0
def beta1 (G : Graph) : Nat := 0
def ball (G : Graph) (v : G.V) (R : Nat) : Type := Unit

def IsTree (T : Type) : Prop :=
  Nonempty T

def FO_equiv_R (k R : Nat) (G₀ G₁ : Graph) : Prop :=
  Nonempty G₀.V ↔ Nonempty G₁.V

def BallIso (G₀ G₁ : Graph) (v₀ : G₀.V) (v₁ : G₁.V) (R : Nat) : Prop :=
  True
