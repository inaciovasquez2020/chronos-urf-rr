import Chronos.SpectralGap

namespace Chronos

variable {V : Type} [InnerProductSpace ℝ V]

axiom ED : Type → ℕ
axiom Hbits : Type → ℝ

theorem quadratic_lower_bound_of_spectralGap
  (Q : V →ₗ[ℝ] V)
  (hQ : spectralGap Q > 0)
  (x : V) :
  ⟪Q x, x⟫ ≥ spectralGap Q * ‖x‖^2 := by
  exact (spectral_gap_pos_iff_coercive Q).mp hQ |>.2 x

theorem normalization_lower_bound
  (X : Type)
  (Q : V →ₗ[ℝ] V)
  (hQ : spectralGap Q > 0) :
  (spectralGap Q) * (ED X : ℝ) ≥ Hbits X := by
  admit

end Chronos
