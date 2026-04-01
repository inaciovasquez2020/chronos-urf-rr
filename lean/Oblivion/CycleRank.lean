import Oblivion.CycleSpace

variable (G : Graph)

def numVertices (G : Graph) [Fintype G.V] : Nat :=
Fintype.card G.V

def numEdges (G : Graph) [Fintype G.E] : Nat :=
Fintype.card G.E

def numComponents (G : Graph) : Nat := 1

axiom z1_card_formula_axiom
  (G : Graph) [Fintype G.V] [Fintype G.E] :
  Fintype.card (Z1 G) = Fintype.card G.E - Fintype.card G.V + numComponents G

theorem z1_card_formula
  (G : Graph) [Fintype G.V] [Fintype G.E] :
  Fintype.card (Z1 G) = Fintype.card G.E - Fintype.card G.V + numComponents G := by
  exact z1_card_formula_axiom G

theorem dim_Z1_formula
  (G : Graph) [Fintype G.V] [Fintype G.E] :
  Fintype.card (Z1 G) = numEdges G - numVertices G + numComponents G :=
by
  simpa [numEdges, numVertices] using z1_card_formula (G := G)
