import Mathlib

namespace Chronos.Frontier

theorem quznor_three_mode_vandermonde_inversion
    (S2 S3 S4 : ℝ) :
    let μ0 := S2 + S3 + S4
    let μ1 := 4 * S2 + 9 * S3 + 16 * S4
    let μ2 := 16 * S2 + 81 * S3 + 256 * S4
    S2 =
        (12 / 5 : ℝ) * μ0
          - (5 / 12 : ℝ) * μ1
          + (1 / 60 : ℝ) * μ2 ∧
    S3 =
        -(64 / 35 : ℝ) * μ0
          + (4 / 7 : ℝ) * μ1
          - (1 / 35 : ℝ) * μ2 ∧
    S4 =
        (3 / 7 : ℝ) * μ0
          - (13 / 84 : ℝ) * μ1
          + (1 / 84 : ℝ) * μ2 := by
  dsimp
  constructor
  · ring
  constructor
  · ring
  · ring

end Chronos.Frontier
