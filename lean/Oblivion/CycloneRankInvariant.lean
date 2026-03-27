import Oblivion.CycleSpace
import Oblivion.CFI2Lift

open Classical

universe u

noncomputable section

def cycleSpaceRank (G : Graph) [Fintype G.E] : Nat :=
  Module.finrank (Fin 2) (G.E → Fin 2)

def parityKernelRank (G : Graph) [Fintype G.E] : Nat :=
  Module.finrank (Fin 2) {c : G.E → Fin 2 // boundary G c = 0}

def I (G : Graph) [Fintype G.E] : Nat :=
  parityKernelRank G
