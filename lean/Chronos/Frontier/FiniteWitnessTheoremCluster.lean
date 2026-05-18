namespace Chronos
namespace Frontier
namespace FiniteWitnessTheoremCluster

abbrev FiniteWitnessCarrier (n : Nat) := Fin n

structure FiniteWitnessCertificate {n : Nat}
    (P : FiniteWitnessCarrier n → Prop) where
  witness : FiniteWitnessCarrier n
  proof : P witness

theorem finite_carrier_nonempty_of_positive
    (n : Nat) (hn : 0 < n) :
    Nonempty (FiniteWitnessCarrier n) := by
  exact ⟨⟨0, hn⟩⟩

theorem certificate_to_exists
    {n : Nat} {P : FiniteWitnessCarrier n → Prop}
    (c : FiniteWitnessCertificate P) :
    ∃ i : FiniteWitnessCarrier n, P i := by
  exact ⟨c.witness, c.proof⟩

theorem exists_to_certificate_nonempty
    {n : Nat} {P : FiniteWitnessCarrier n → Prop}
    (h : ∃ i : FiniteWitnessCarrier n, P i) :
    Nonempty (FiniteWitnessCertificate P) := by
  rcases h with ⟨i, hi⟩
  exact ⟨⟨i, hi⟩⟩

theorem certificate_nonempty_iff_exists
    {n : Nat} {P : FiniteWitnessCarrier n → Prop} :
    Nonempty (FiniteWitnessCertificate P) ↔
      ∃ i : FiniteWitnessCarrier n, P i := by
  constructor
  · intro h
    rcases h with ⟨c⟩
    exact certificate_to_exists c
  · intro h
    exact exists_to_certificate_nonempty h

def certificate_map
    {n : Nat}
    {P Q : FiniteWitnessCarrier n → Prop}
    (hPQ : ∀ i : FiniteWitnessCarrier n, P i → Q i)
    (c : FiniteWitnessCertificate P) :
    FiniteWitnessCertificate Q :=
  ⟨c.witness, hPQ c.witness c.proof⟩

theorem certificate_map_nonempty
    {n : Nat}
    {P Q : FiniteWitnessCarrier n → Prop}
    (hPQ : ∀ i : FiniteWitnessCarrier n, P i → Q i)
    (h : Nonempty (FiniteWitnessCertificate P)) :
    Nonempty (FiniteWitnessCertificate Q) := by
  rcases h with ⟨c⟩
  exact ⟨certificate_map hPQ c⟩

theorem exists_map
    {n : Nat}
    {P Q : FiniteWitnessCarrier n → Prop}
    (hPQ : ∀ i : FiniteWitnessCarrier n, P i → Q i)
    (h : ∃ i : FiniteWitnessCarrier n, P i) :
    ∃ i : FiniteWitnessCarrier n, Q i := by
  rcases h with ⟨i, hi⟩
  exact ⟨i, hPQ i hi⟩

def true_certificate_of_positive
    (n : Nat) (hn : 0 < n) :
    FiniteWitnessCertificate
      (fun _ : FiniteWitnessCarrier n => True) :=
  ⟨⟨0, hn⟩, True.intro⟩

theorem true_certificate_nonempty_of_positive
    (n : Nat) (hn : 0 < n) :
    Nonempty
      (FiniteWitnessCertificate
        (fun _ : FiniteWitnessCarrier n => True)) := by
  exact ⟨true_certificate_of_positive n hn⟩

theorem true_exists_of_positive
    (n : Nat) (hn : 0 < n) :
    ∃ _ : FiniteWitnessCarrier n, True := by
  exact certificate_to_exists (true_certificate_of_positive n hn)

end FiniteWitnessTheoremCluster
end Frontier
end Chronos
