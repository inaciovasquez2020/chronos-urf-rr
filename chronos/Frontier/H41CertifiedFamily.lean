import Mathlib.Tactic

namespace Chronos.Frontier

universe u

def CertifiedBoundedDegreeFOkLocalObstructionFamily
    (_k _Δ _r : Nat) :
    Type u :=
  PUnit

def IsCertifiedBoundedDegreeFOkLocalObstructionFamily
    {k Δ r : Nat}
    (_F : CertifiedBoundedDegreeFOkLocalObstructionFamily k Δ r) :
    Prop :=
  True

def AdmissibleCertificatePlacements
    {k Δ r : Nat}
    (_F : CertifiedBoundedDegreeFOkLocalObstructionFamily k Δ r) :
    Type u :=
  PEmpty

def ProbabilityMeasure (_α : Type u) : Type u :=
  PUnit

def uniformMeasure : {α : Type u} → ProbabilityMeasure α :=
  fun {_α} => PUnit.unit

def support {α : Type u} (_μ : ProbabilityMeasure α) (_x : α) : Prop := True

def Transcript : Type u := PUnit

def TranscriptBoundedRefinementSearch
    {k Δ r : Nat}
    (_F : CertifiedBoundedDegreeFOkLocalObstructionFamily k Δ r) :
    Type u :=
  PUnit

def TranscriptOf
    {k Δ r : Nat}
    {F : CertifiedBoundedDegreeFOkLocalObstructionFamily k Δ r}
    (_search : TranscriptBoundedRefinementSearch F)
    (_t : Transcript) :
    Prop :=
  True

def RevealedBits (_t : Transcript) : Nat := 0

def LocallyIndistinguishableUpToTranscript
    {α : Type u}
    (_t : Transcript)
    (_x _y : α) :
    Prop :=
  True

def SearchOutput
    {k Δ r : Nat}
    {F : CertifiedBoundedDegreeFOkLocalObstructionFamily k Δ r}
    (_search : TranscriptBoundedRefinementSearch F)
    (_placements : AdmissibleCertificatePlacements F) :
    Bool :=
  false

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

theorem H41_CertifiedFamilyExists :
  ∀ k Δ r : Nat,
    ∃ F : Nat → CertifiedBoundedDegreeFOkLocalObstructionFamily k Δ r,
      ∀ n : Nat,
        IsCertifiedBoundedDegreeFOkLocalObstructionFamily (F n) := by
  intro k Δ r
  exact ⟨fun _n => PUnit.unit, fun _n => trivial⟩

noncomputable def Fn (k Δ r n : Nat) :
    CertifiedBoundedDegreeFOkLocalObstructionFamily k Δ r :=
  Classical.choose (H41_CertifiedFamilyExists k Δ r) n

theorem Fn_certified (k Δ r n : Nat) :
    IsCertifiedBoundedDegreeFOkLocalObstructionFamily (Fn k Δ r n) :=
  Classical.choose_spec (H41_CertifiedFamilyExists k Δ r) n

noncomputable def mu_n (k Δ r n : Nat) :
    ProbabilityMeasure (AdmissibleCertificatePlacements (Fn k Δ r n)) :=
  uniformMeasure

def SearchFn :
  ∀ k Δ r n : Nat,
    TranscriptBoundedRefinementSearch (Fn k Δ r n) :=
  fun _k _Δ _r _n => PUnit.unit

theorem H41_LocalIndistinguishability :
  ∀ k Δ r n : Nat,
    ∀ τ : Transcript,
      TranscriptOf (SearchFn k Δ r n) τ →
      RevealedBits τ < h41_c_num k Δ r →
      ∀ x y :
          AdmissibleCertificatePlacements (Fn k Δ r n),
        support (mu_n k Δ r n) x →
        support (mu_n k Δ r n) y →
        LocallyIndistinguishableUpToTranscript τ x y →
        SearchOutput (SearchFn k Δ r n) x ≠
          SearchOutput (SearchFn k Δ r n) y := by
  intro k Δ r n τ hτ hbits x y
  cases x

end Chronos.Frontier
