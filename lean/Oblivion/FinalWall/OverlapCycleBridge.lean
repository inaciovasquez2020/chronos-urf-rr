-- add directly below columnIncidence

def incidenceDegree
  (A : Matrix (Fin m) (Fin n) F2)
  (γ : Finset (Fin m))
  (j : Fin n) : ℕ :=
  columnIncidence A γ j

-- key structural conjecture (stronger form)
axiom overlap_cycle_even_degree
  (A : Matrix (Fin m) (Fin n) F2)
  (γ : Finset (Fin m))
  (hγ : isOverlapCycle A γ) :
  ∀ j, Even (incidenceDegree A γ j)
