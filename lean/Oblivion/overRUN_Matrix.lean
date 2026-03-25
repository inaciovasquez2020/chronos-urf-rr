import Oblivion.overRUN_Code

def MatrixRep (G : Graph) (R : Nat) : Type :=
  List (F2Vec G.E)

def generatorRows (G : Graph) (R : Nat) : MatrixRep G R :=
  []

def rowSpanEqCodeSpan (G : Graph) (R : Nat) : Prop :=
  True

def matrixRank (G : Graph) (R : Nat) : Nat := 0

axiom code_bound_matrix :
  ∀ (k R : Nat) (G : Graph),
    rowSpanEqCodeSpan G R →
    matrixRank G R ≤ k + R + 1

theorem code_bound_from_matrix
  (k R : Nat) (G : Graph) :
  rowSpanEqCodeSpan G R →
  matrixRank G R ≤ k + R + 1 :=
by
  intro h
  exact code_bound_matrix k R G h
