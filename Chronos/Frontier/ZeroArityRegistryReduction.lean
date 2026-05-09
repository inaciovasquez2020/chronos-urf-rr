import Chronos.Frontier.ZeroArityRepresentation

theorem zero_arity_registry_reduction
    (P : ChronosCarrierData → Prop)
    (hP : ∀ s i : Nat, P { arity := 0, stratum := s, index := i })
    (C : ChronosCarrierData) (h0 : C.arity = 0) :
    P C := by
  rcases zero_arity_representation C h0 with ⟨s, i, rfl⟩
  exact hP s i
