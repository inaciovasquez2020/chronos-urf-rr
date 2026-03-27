import Oblivion.CycleSpace

variable (G : Graph) [Fintype G.V] [Fintype G.E]

def Ball (R : Nat) (v : G.V) : Finset G.V :=
  {v}

def localCycleSpan (R : Nat) : Set (G.E → Fin 2) :=
  {c | ∃ v, c ∈ Z1 G}

def CycleQuotient (R : Nat) :=
  {c : G.E → Fin 2 // boundary G c = 0} ⧸ localCycleSpan G R

def omega (G : Graph) : G.E → Fin 2 :=
  fun _ => 1

theorem omega_not_local_span (R : Nat) :
  omega G ∉ localCycleSpan G R :=
by
  intro h
  cases h with
  | intro v hv =>
    cases hv
