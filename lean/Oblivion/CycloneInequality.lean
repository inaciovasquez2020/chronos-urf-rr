import Oblivion.CycloneRankInvariant
import Oblivion.ParityKernelDifference

variable (G : Graph) [Fintype G.E]

def G0 := ParityKernelDifference.G0 G
def G1 := ParityKernelDifference.G1 G

theorem cyclone_inequality :
  I (G0 G) ≠ I (G1 G) :=
by
  exact ParityKernelDifference.parity_kernel_difference G
