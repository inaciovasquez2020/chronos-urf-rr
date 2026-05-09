import Chronos.Frontier.ZeroArityRegistryReduction

theorem zero_positive_carrier_case_split
    (P : ChronosCarrierData → Prop)
    (hZero : ∀ s i : Nat, P { arity := 0, stratum := s, index := i })
    (hPositive : ∀ C : ChronosCarrierData, 0 < C.arity → P C)
    (C : ChronosCarrierData) :
    P C := by
  cases Nat.eq_zero_or_pos C.arity with
  | inl h0 =>
      exact zero_arity_registry_reduction P hZero C h0
  | inr hpos =>
      exact hPositive C hpos

theorem zero_positive_carrier_dichotomy
    (C : ChronosCarrierData) :
    (∃ s i : Nat, C = { arity := 0, stratum := s, index := i }) ∨
      0 < C.arity := by
  cases Nat.eq_zero_or_pos C.arity with
  | inl h0 =>
      left
      exact zero_arity_representation C h0
  | inr hpos =>
      right
      exact hpos
