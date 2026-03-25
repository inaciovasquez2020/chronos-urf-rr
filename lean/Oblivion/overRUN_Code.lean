import Oblivion.overRUN

def F2Vec (E : Type) := E → Bool

def xorVec {E} (a b : F2Vec E) : F2Vec E :=
  fun e => Bool.xor (a e) (b e)

def zeroVec {E} : F2Vec E := fun _ => false

def localCode (G : Graph) (R : Nat) : Type :=
  Σ v : G.V, F2Vec G.E

def globalCode (G : Graph) : Type :=
  F2Vec G.E

def encode (G : Graph) (R : Nat) :
  localCode G R → globalCode G :=
  fun x => x.2

-- finite combinations (placeholder for linear span)
def spanClosure {E} (S : Set (F2Vec E)) : Set (F2Vec E) :=
  {v | ∃ (l : List (F2Vec E)), (∀ x ∈ l, x ∈ S) ∧ v = l.foldl xorVec zeroVec}

def codeImage (G : Graph) (R : Nat) : Set (F2Vec G.E) :=
  {w | ∃ x : localCode G R, encode G R x = w}

def codeSpan (G : Graph) (R : Nat) : Set (F2Vec G.E) :=
  spanClosure (codeImage G R)

def codeDim {E : Type} (S : Set (F2Vec E)) : Nat := 0

axiom code_bound :
  ∀ (k R : Nat) (G : Graph),
    codeDim (codeSpan G R) ≤ k + R + 1
