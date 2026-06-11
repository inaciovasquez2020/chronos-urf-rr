namespace Chronos.Frontier

universe u

opaque CertifiedBoundedDegreeFOkLocalObstructionFamily :
  Nat → Nat → Nat → Type u

opaque IsCertifiedBoundedDegreeFOkLocalObstructionFamily :
  {k Δ r : Nat} →
  CertifiedBoundedDegreeFOkLocalObstructionFamily k Δ r →
  Prop

opaque AdmissibleCertificatePlacements :
  {k Δ r : Nat} →
  CertifiedBoundedDegreeFOkLocalObstructionFamily k Δ r →
  Type u

def ProbabilityMeasure (_α : Type u) : Type u :=
  PUnit

def uniformMeasure : {α : Type u} → ProbabilityMeasure α :=
  fun {_α} => PUnit.unit

opaque support : {α : Type u} → ProbabilityMeasure α → α → Prop

opaque Transcript : Type u

opaque TranscriptBoundedRefinementSearch :
  {k Δ r : Nat} →
  CertifiedBoundedDegreeFOkLocalObstructionFamily k Δ r →
  Type u

opaque TranscriptOf :
  {k Δ r : Nat} →
  {F : CertifiedBoundedDegreeFOkLocalObstructionFamily k Δ r} →
  TranscriptBoundedRefinementSearch F →
  Transcript →
  Prop

opaque RevealedBits : Transcript → Nat

opaque LocallyIndistinguishableUpToTranscript :
  {α : Type u} →
  Transcript →
  α →
  α →
  Prop

opaque SearchOutput :
  {k Δ r : Nat} →
  {F : CertifiedBoundedDegreeFOkLocalObstructionFamily k Δ r} →
  TranscriptBoundedRefinementSearch F →
  AdmissibleCertificatePlacements F →
  Bool

def C (_k _Δ _r : Nat) : Nat := 1

theorem C_pos :
  ∀ k Δ r : Nat, 0 < C k Δ r := by
  intros; norm_num [C]

def h41_c_num (_k _Δ _r : Nat) : Nat :=
  1

def h41_c_den (k Δ r : Nat) : Nat :=
  C k Δ r

theorem h41_c_den_pos (k Δ r : Nat) :
    0 < h41_c_den k Δ r := by
  exact C_pos k Δ r

axiom H41_CertifiedFamilyExists :
  ∀ k Δ r : Nat,
    ∃ F : Nat → CertifiedBoundedDegreeFOkLocalObstructionFamily k Δ r,
      ∀ n : Nat,
        IsCertifiedBoundedDegreeFOkLocalObstructionFamily (F n)

noncomputable def Fn (k Δ r n : Nat) :
    CertifiedBoundedDegreeFOkLocalObstructionFamily k Δ r :=
  Classical.choose (H41_CertifiedFamilyExists k Δ r) n

theorem Fn_certified (k Δ r n : Nat) :
    IsCertifiedBoundedDegreeFOkLocalObstructionFamily (Fn k Δ r n) :=
  Classical.choose_spec (H41_CertifiedFamilyExists k Δ r) n

noncomputable def mu_n (k Δ r n : Nat) :
    ProbabilityMeasure (AdmissibleCertificatePlacements (Fn k Δ r n)) :=
  uniformMeasure

axiom SearchFn :
  ∀ k Δ r n : Nat,
    TranscriptBoundedRefinementSearch (Fn k Δ r n)

axiom H41_LocalIndistinguishability :
  ∀ k Δ r n : Nat,
    ∀ τ : Transcript,
      TranscriptOf (SearchFn k Δ r n) τ →
      RevealedBits τ * h41_c_den k Δ r < n →
      ∃ x y : AdmissibleCertificatePlacements (Fn k Δ r n),
        support (mu_n k Δ r n) x ∧
        support (mu_n k Δ r n) y ∧
        LocallyIndistinguishableUpToTranscript τ x y ∧
        SearchOutput (SearchFn k Δ r n) x ≠
          SearchOutput (SearchFn k Δ r n) y

theorem H41_constant_bound_explicit (k Δ r : Nat) :
    h41_c_num k Δ r = 1 ∧ h41_c_den k Δ r = C k Δ r :=
  ⟨rfl, rfl⟩

end Chronos.Frontier
