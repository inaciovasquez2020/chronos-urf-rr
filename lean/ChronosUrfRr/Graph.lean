structure Graph where
  V : Type
  E : Type
  src : E → V
  dst : E → V

def Connected (G : Graph) : Prop := True

def girth (G : Graph) : Nat := 0

def beta1 (G : Graph) : Nat := 0

def ball (G : Graph) (v : G.V) (R : Nat) : Type := Unit

def IsTree (T : Type) : Prop := True

def FO_equiv_R (k R : Nat) (G₀ G₁ : Graph) : Prop := True

def BallIso (G₀ G₁ : Graph) (v₀ : G₀.V) (v₁ : G₁.V) (R : Nat) : Prop := True
