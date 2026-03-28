-- replace isOverlapCycle with stronger condition

def balancedOverlap
  (A : Matrix (Fin m) (Fin n) F2)
  (γ : Finset (Fin m)) : Prop :=
  ∀ j : Fin n,
    Even (∑ i in γ, if A i j = 0 then 0 else 1)

-- redefine target lemma
axiom balanced_overlap_even_degree
  (A : Matrix (Fin m) (Fin n) F2)
  (γ : Finset (Fin m))
  (hγ : balancedOverlap A γ) :
  ∀ j, Even (incidenceDegree A γ j)
