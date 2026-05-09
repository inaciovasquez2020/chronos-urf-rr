import Chronos.Frontier.RealChronosAdmissible

theorem zero_arity_representation
    (C : ChronosCarrierData) (h0 : C.arity = 0) :
    ∃ s i : Nat, C = { arity := 0, stratum := s, index := i } := by
  cases C with
  | mk arity stratum index =>
      simp at h0
      rw [h0]
      exists stratum, index
      rfl
