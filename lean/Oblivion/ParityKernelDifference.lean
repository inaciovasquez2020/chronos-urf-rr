import Oblivion.CycloneRankInvariant
import Oblivion.CFI2Lift

variable (G : Graph) [Fintype G.E]

def sigma0 : G.E → Bool := fun _ => false
def sigma1 : G.E → Bool := fun _ => true

def G0 := twist G sigma0
def G1 := twist G sigma1

theorem parity_kernel_difference :
  I (G0 G) ≠ I (G1 G) :=
by
  unfold I parityKernelRank
  intro h
  exact False.elim (by cases h)
