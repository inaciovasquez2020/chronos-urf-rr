import Oblivion.overRUN

-- Boolean vector as F₂ model
def F2Vec (E : Type) := E → Bool

-- vector addition (XOR)
def xorVec {E} (a b : F2Vec E) : F2Vec E :=
  fun e => Bool.xor (a e) (b e)

-- zero vector
def zeroVec {E} : F2Vec E := fun _ => false

-- Local codewords (cycle indicators, placeholder)
def localCode (G : Graph) (R : Nat) : Type :=
  Σ v : G.V, F2Vec G.E

-- Global code
def globalCode (G : Graph) : Type :=
  F2Vec G.E

-- Generator map (projection)
def encode (G : Graph) (R : Nat) :
  localCode G R → globalCode G :=
  fun x => x.2

-- Span closure (placeholder)
def inSpan {E} (S : Set (F2Vec E)) (v : F2Vec E) : Prop :=
  True

-- Dimension placeholder
def codeDim {E : Type} (S : Set (F2Vec E)) : Nat := 0

-- Image of generators
def codeImage (G : Graph) (R : Nat) : Set (F2Vec G.E) :=
  {w | ∃ x : localCode G R, encode G R x = w}

-- Target bound
axiom code_bound :
  ∀ (k R : Nat) (G : Graph),
    codeDim (codeImage G R) ≤ k + R + 1
