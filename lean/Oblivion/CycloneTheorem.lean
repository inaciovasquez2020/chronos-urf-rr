import Oblivion.CycloneWitness
import Oblivion.CycloneInequality
import Oblivion.CFIDuplicatorComplete
import Oblivion.EFEquiv

variable (G : Graph) [Fintype G.V] [Fintype G.E] [DecidableEq G.V]

def G0 := CycloneWitness.G0 G
def G1 := CycloneWitness.G1 G

theorem Cyclone :
  ∃ G₀ G₁, FO_equiv (G₀ := G₀) (G₁ := G₁) 2 2 ∧ I G₀ ≠ I G₁ :=
by
  refine ⟨G0 G, G1 G, ?_, ?_⟩
  · unfold FO_equiv
    exact CFIDuplicatorComplete.duplicator_strategy_complete (G := G) 2 2
  · exact CycloneInequality.cyclone_inequality G
