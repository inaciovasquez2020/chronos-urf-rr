structure Graph where
  V : Type
  E : Type
  src : E → V
  dst : E → V

def Connected (_ : Graph) : Prop := True
def girth (_ : Graph) : Nat := 0
def beta1 (_ : Graph) : Nat := 0

def ball (_ : Graph) (_ : _) (_ : Nat) := Unit
def IsTree (_ : _) : Prop := True

def FO_equiv_R (_ _ : Nat) (_ _ : Graph) : Prop := True

def BallIso (_ _ : Graph) (_ _ : _) (_ : Nat) : Prop := True
