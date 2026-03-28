-- replace axiom with counting lemma

theorem incidence_cycle_even_column_degree
  (A : Matrix (Fin m) (Fin n) F2)
  (C : IncidenceCycle A) :
  ∀ j : Fin n,
    Even (C.rows.countP (fun i => rowHitsColumn A i j)) := by
  intro j
  -- each column j appears paired via step₁ and step₂
  -- each occurrence counted twice
  refine ⟨_, ?_⟩
  -- missing: formal count decomposition
  sorry
