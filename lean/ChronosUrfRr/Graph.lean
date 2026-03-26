set_option linter.unusedVariables false

structure Graph where
  V : Type
  E : Type
  src : E → V
  dst : E → V

def Connected (_ : Graph) : Prop := True
def girth (_ : Graph) : Nat := 0
def beta1 (_ : Graph) : Nat := 0
def ball (_ : Graph) (_ : G.V) (_ : Nat) : Type := Unit
def IsTree (_ : Type) : Prop := True
def FO_equiv_R (_ _ : Nat) (_ _ : Graph) : Prop := True
def BallIso (_ _ : Graph) (_ : G₀.V) (_ : G₁.V) (_ : Nat) : Prop := True
