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


lemma sigma_explicit
  {A : Matrix (Fin m) (Fin n) F2}
  (C : IncidenceCycle A) :
  Function.Involutive (sigma C) :=
by
  intro k
  ext
  simp [sigma, Nat.add_mod, Nat.mod_mod]

lemma sigma_preserves_visits_explicit
  {A : Matrix (Fin m) (Fin n) F2}
  (C : IncidenceCycle A)
  (j : Fin n) :
  ∀ k, k ∈ visits C j → sigma C k ∈ visits C j :=
by
  intro k hk
  classical
  simp [visits] at *
  rcases Finset.mem_filter.mp hk with ⟨_, hk⟩
  have h₁ := C.step₁ k.1 k.2
  have h₂ := C.step₂ k.1 k.2
  simp [sigma]
  exact Finset.mem_filter.mpr ⟨by simp, by simpa using hk⟩

lemma sigma_no_fixed_explicit
  {A : Matrix (Fin m) (Fin n) F2}
  (C : IncidenceCycle A)
  (j : Fin n) :
  ∀ k, k ∈ visits C j → sigma C k ≠ k :=
by
  intro k hk h
  have := congrArg Fin.val h
  simp [sigma] at this
  exact Nat.succ_ne_self _ this

lemma column_index_row_hit_bijection_explicit
  {A : Matrix (Fin m) (Fin n) F2}
  (C : IncidenceCycle A)
  (j : Fin n) :
  (visits C j).card = (rowHitsAt C j).card :=
by
  classical
  simp [visits, rowHitsAt, List.countP_eq_length_filter]


theorem incidence_cycle_even_column_degree_final
  {A : Matrix (Fin m) (Fin n) F2}
  (C : IncidenceCycle A) :
  ∀ j : Fin n,
    Even (C.rows.countP (fun i => rowHitsColumn A i j)) :=
by
  intro j
  classical

  have hσ :
    Function.Involutive (sigma C) :=
    sigma_explicit C

  have hPres :
    ∀ k, k ∈ visits C j → sigma C k ∈ visits C j :=
    sigma_preserves_visits_explicit C j

  have hNoFix :
    ∀ k, k ∈ visits C j → sigma C k ≠ k :=
    sigma_no_fixed_explicit C j

  have hEvenVisits :
    Even ((visits C j).card) :=
    Finset.card_eq_two_mul_card_quotient
      (visits C j) (sigma C) hσ hNoFix hPres

  have hEq₁ :
    (visits C j).card = (rowHitsAt C j).card :=
    column_index_row_hit_bijection_explicit C j

  have hEq₂ :
    (rowHitsAt C j).card =
      C.rows.countP (fun i => rowHitsColumn A i j) := by
    simp [rowHitsAt, List.countP_eq_length_filter]

  rw [hEq₁, hEq₂] at hEvenVisits
  exact hEvenVisits

