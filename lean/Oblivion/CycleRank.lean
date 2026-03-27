import Oblivion.CycleSpace

variable (G : Graph)

def numVertices (G : Graph) [Fintype G.V] : Nat :=
Fintype.card G.V

def numEdges (G : Graph) [Fintype G.E] : Nat :=
Fintype.card G.E

def numComponents (G : Graph) : Nat := 1

theorem dim_Z1_formula
  (G : Graph) [Fintype G.V] [Fintype G.E] :
  Fintype.card (Z1 G) = numEdges G - numVertices G + numComponents G :=
by
  admit
