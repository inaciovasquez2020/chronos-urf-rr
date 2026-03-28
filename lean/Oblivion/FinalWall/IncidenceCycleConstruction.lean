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

theorem visits_even
  {A : Matrix (Fin m) (Fin n) F2}
  (C : IncidenceCycle A)
  (j : Fin n)
  (hσ :
    ∃ σ : Fin C.cols.length → Fin C.cols.length,
      Function.Involutive σ ∧
      (∀ k, k ∈ visits C j → σ k ∈ visits C j) ∧
      (∀ k, k ∈ visits C j → σ k ≠ k)
  ) :
  Even ((visits C j).card) :=
by
  classical
  rcases hσ with ⟨σ, hInv, hPres, hNoFix⟩
  exact
    Finset.card_eq_two_mul_card_quotient
      (visits C j) σ hInv hNoFix hPres

