import Oblivion.CycleSpace

variable (G : Graph)

def fundamentalCycle (e : G.E) : C1 G :=
fun e' => if e' = e then 1 else 0

def omega (G : Graph) : C1 G :=
fun e => 1

theorem omega_in_Z1 (G : Graph) :
  omega G ∈ Z1 G :=
by
  refine ⟨omega G, ?_⟩
  funext v
  simp [omega, boundary]

theorem omega_nontrivial (G : Graph) :
  omega G ≠ 0 :=
by
  funext e
  simp [omega]
