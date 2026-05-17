import Mathlib.Data.Real.Basic
import Mathlib.Data.Fin.Basic
import Mathlib.Tactic

namespace FiniteRegisteredHyperbolicRateThickAssembly

abbrev Lam := ℝ

def BinaryKappaAdmissible (lam : Lam) : Prop :=
  0 < lam ∧ lam ≤ (1 / 2 : ℝ)

def binaryKappaCandidate (lam : Lam) : ℝ :=
  lam * (1 - lam)

structure UniformlyHyperbolicAdmissibleSystem where
  lam : Lam
  entropyMass : ℝ
  lam_admissible : BinaryKappaAdmissible lam

structure FiniteHyperbolicRegistry (n : Nat) where
  system : Fin n → UniformlyHyperbolicAdmissibleSystem

def RegisteredSystem
    {n : Nat}
    (R : FiniteHyperbolicRegistry n)
    (X : UniformlyHyperbolicAdmissibleSystem) : Prop :=
  ∃ i : Fin n, X = R.system i

def alpha_hyp (epsilon : ℝ) : ℝ :=
  4 * epsilon

def RegisteredRatioStabilitySlack
    {n : Nat}
    (R : FiniteHyperbolicRegistry n)
    (alpha : ℝ) : Prop :=
  ∀ X : UniformlyHyperbolicAdmissibleSystem,
    RegisteredSystem R X →
    alpha * binaryKappaCandidate X.lam ≤ X.entropyMass

def RegisteredUniformFiberMassFloor
    {n : Nat}
    (R : FiniteHyperbolicRegistry n)
    (epsilon : ℝ) : Prop :=
  ∀ X : UniformlyHyperbolicAdmissibleSystem,
    RegisteredSystem R X →
    epsilon ≤ X.entropyMass

structure RegisteredEntropyMinimumDominationCertificate
    {n : Nat}
    (R : FiniteHyperbolicRegistry n)
    (alpha : ℝ) : Prop where
  alpha_pos : 0 < alpha
  ratio_stability : RegisteredRatioStabilitySlack R alpha

structure RegisteredUniformFiberMassCertificate
    {n : Nat}
    (R : FiniteHyperbolicRegistry n)
    (epsilon : ℝ) : Prop where
  epsilon_pos : 0 < epsilon
  uniform_floor : RegisteredUniformFiberMassFloor R epsilon

def RegisteredRateThickFiberCoercivity
    {n : Nat}
    (R : FiniteHyperbolicRegistry n) : Prop :=
  ∃ alpha epsilon : ℝ,
    RegisteredEntropyMinimumDominationCertificate R alpha ∧
    RegisteredUniformFiberMassCertificate R epsilon

def RegisteredHyperbolicUniversalFiberEntropyGap
    {n : Nat}
    (R : FiniteHyperbolicRegistry n) : Prop :=
  ∃ epsilon : ℝ,
    0 < epsilon ∧
    RegisteredUniformFiberMassFloor R epsilon

lemma binaryKappaCandidate_le_quarter (lam : ℝ) :
    binaryKappaCandidate lam ≤ (1 / 4 : ℝ) := by
  unfold binaryKappaCandidate
  nlinarith [sq_nonneg (lam - (1 / 2 : ℝ))]

theorem alpha_hyp_pos
    {epsilon : ℝ}
    (hepsilon : 0 < epsilon) :
    0 < alpha_hyp epsilon := by
  unfold alpha_hyp
  nlinarith

theorem FiniteRegisteredRatioStability_from_uniform_floor
    {n : Nat}
    (R : FiniteHyperbolicRegistry n)
    (epsilon : ℝ)
    (hepsilon : 0 < epsilon)
    (hFloor :
      ∀ i : Fin n,
        epsilon ≤ (R.system i).entropyMass) :
    RegisteredRatioStabilitySlack R (alpha_hyp epsilon) := by
  intro X hX
  rcases hX with ⟨i, rfl⟩
  have hk :
      binaryKappaCandidate (R.system i).lam ≤ (1 / 4 : ℝ) :=
    binaryKappaCandidate_le_quarter (R.system i).lam
  have hcoef_nonneg : 0 ≤ 4 * epsilon := by
    nlinarith [hepsilon]
  have hmul :
      (4 * epsilon) * binaryKappaCandidate (R.system i).lam
        ≤ (4 * epsilon) * (1 / 4 : ℝ) :=
    mul_le_mul_of_nonneg_left hk hcoef_nonneg
  have hright :
      (4 * epsilon) * (1 / 4 : ℝ) = epsilon := by
    ring
  calc
    alpha_hyp epsilon * binaryKappaCandidate (R.system i).lam
        = (4 * epsilon) * binaryKappaCandidate (R.system i).lam := by rfl
    _ ≤ (4 * epsilon) * (1 / 4 : ℝ) := hmul
    _ = epsilon := hright
    _ ≤ (R.system i).entropyMass := hFloor i

theorem FiniteRegisteredUniformFloor_from_index_floor
    {n : Nat}
    (R : FiniteHyperbolicRegistry n)
    (epsilon : ℝ)
    (hFloor :
      ∀ i : Fin n,
        epsilon ≤ (R.system i).entropyMass) :
    RegisteredUniformFiberMassFloor R epsilon := by
  intro X hX
  rcases hX with ⟨i, rfl⟩
  exact hFloor i

theorem FiniteRegisteredDominationCertificate
    {n : Nat}
    (R : FiniteHyperbolicRegistry n)
    (epsilon : ℝ)
    (hepsilon : 0 < epsilon)
    (hFloor :
      ∀ i : Fin n,
        epsilon ≤ (R.system i).entropyMass) :
    RegisteredEntropyMinimumDominationCertificate R (alpha_hyp epsilon) := by
  exact {
    alpha_pos := alpha_hyp_pos hepsilon
    ratio_stability :=
      FiniteRegisteredRatioStability_from_uniform_floor R epsilon hepsilon hFloor
  }

theorem FiniteRegisteredUniformMassCertificate
    {n : Nat}
    (R : FiniteHyperbolicRegistry n)
    (epsilon : ℝ)
    (hepsilon : 0 < epsilon)
    (hFloor :
      ∀ i : Fin n,
        epsilon ≤ (R.system i).entropyMass) :
    RegisteredUniformFiberMassCertificate R epsilon := by
  exact {
    epsilon_pos := hepsilon
    uniform_floor :=
      FiniteRegisteredUniformFloor_from_index_floor R epsilon hFloor
  }

theorem FiniteRegisteredRateThickFiberCoercivityAssembly
    {n : Nat}
    (R : FiniteHyperbolicRegistry n)
    (epsilon : ℝ)
    (hepsilon : 0 < epsilon)
    (hFloor :
      ∀ i : Fin n,
        epsilon ≤ (R.system i).entropyMass) :
    RegisteredRateThickFiberCoercivity R := by
  exact ⟨
    alpha_hyp epsilon,
    epsilon,
    FiniteRegisteredDominationCertificate R epsilon hepsilon hFloor,
    FiniteRegisteredUniformMassCertificate R epsilon hepsilon hFloor
  ⟩

theorem FiniteRegisteredUniversalGap_from_rate_thick_coercivity
    {n : Nat}
    (R : FiniteHyperbolicRegistry n)
    (h : RegisteredRateThickFiberCoercivity R) :
    RegisteredHyperbolicUniversalFiberEntropyGap R := by
  rcases h with ⟨alpha, epsilon, hDom, hMass⟩
  exact ⟨epsilon, hMass.epsilon_pos, hMass.uniform_floor⟩

theorem FiniteRegisteredHyperbolicRateThickUniversalGapAssembly
    {n : Nat}
    (R : FiniteHyperbolicRegistry n)
    (epsilon : ℝ)
    (hepsilon : 0 < epsilon)
    (hFloor :
      ∀ i : Fin n,
        epsilon ≤ (R.system i).entropyMass) :
    RegisteredHyperbolicUniversalFiberEntropyGap R := by
  exact FiniteRegisteredUniversalGap_from_rate_thick_coercivity R
    (FiniteRegisteredRateThickFiberCoercivityAssembly R epsilon hepsilon hFloor)

end FiniteRegisteredHyperbolicRateThickAssembly
