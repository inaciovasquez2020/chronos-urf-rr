import Mathlib.Data.Real.Basic
import Mathlib.Tactic

namespace Chronos
namespace Frontier
namespace FPz1

variable {Obj Wit : Type}

def RateSpectrumIsolation
    (ChronosAdmissible : Obj → Prop)
    (SemanticRankRateWitness : Obj → Wit → Prop)
    (rankRate : Wit → ℝ) : Prop :=
  ∃ lam0 : ℝ, lam0 > 0 ∧
    ∀ X ρ,
      ChronosAdmissible X →
      SemanticRankRateWitness X ρ →
      rankRate ρ > 0 →
      rankRate ρ ≥ lam0

def InverseNatRateSequence
    (ChronosAdmissible : Obj → Prop)
    (SemanticRankRateWitness : Obj → Wit → Prop)
    (rankRate : Wit → ℝ) : Prop :=
  ∀ n : ℕ, n ≥ 1 →
    ∃ X ρ,
      ChronosAdmissible X ∧
      SemanticRankRateWitness X ρ ∧
      rankRate ρ = (1 : ℝ) / (n : ℝ)

theorem inverseNatRateSequence_refutes_rateSpectrumIsolation
    (ChronosAdmissible : Obj → Prop)
    (SemanticRankRateWitness : Obj → Wit → Prop)
    (rankRate : Wit → ℝ)
    (hseq :
      InverseNatRateSequence
        ChronosAdmissible
        SemanticRankRateWitness
        rankRate) :
    ¬ RateSpectrumIsolation
        ChronosAdmissible
        SemanticRankRateWitness
        rankRate := by
  intro hIso
  rcases hIso with ⟨lam0, hlam0pos, hbound⟩
  obtain ⟨n, hn⟩ := exists_nat_one_div_lt hlam0pos
  have hn1 : n + 1 ≥ 1 := Nat.succ_le_succ (Nat.zero_le n)
  rcases hseq (n + 1) hn1 with ⟨X, ρ, hAdm, hWit, hrank⟩
  have hratepos : rankRate ρ > 0 := by
    rw [hrank]
    positivity
  have hlower : rankRate ρ ≥ lam0 :=
    hbound X ρ hAdm hWit hratepos
  have hupper : rankRate ρ < lam0 := by
    rw [hrank]
    simpa [Nat.cast_add_one] using hn
  linarith

end FPz1
end Frontier
end Chronos
