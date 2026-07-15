import Mathlib

namespace Chronos.Frontier

def quznorModePairEnergy (A B : ℂ) : ℝ :=
  Complex.normSq A + Complex.normSq B

def quznorThreeModeMu2
    (A2 B2 A3 B3 A4 B4 : ℂ) : ℝ :=
  16 * quznorModePairEnergy A2 B2 +
  81 * quznorModePairEnergy A3 B3 +
  256 * quznorModePairEnergy A4 B4

def quznorSecondDerivativeFourierEnergy
    (A2 B2 A3 B3 A4 B4 : ℂ) : ℝ :=
  quznorModePairEnergy
      ((-4 : ℂ) * A2) ((-4 : ℂ) * B2) +
  quznorModePairEnergy
      ((-9 : ℂ) * A3) ((-9 : ℂ) * B3) +
  quznorModePairEnergy
      ((-16 : ℂ) * A4) ((-16 : ℂ) * B4)

theorem quznor_three_mode_mu2_eq_second_derivative_fourier_energy
    (A2 B2 A3 B3 A4 B4 : ℂ) :
    quznorThreeModeMu2 A2 B2 A3 B3 A4 B4 =
      quznorSecondDerivativeFourierEnergy A2 B2 A3 B3 A4 B4 := by
  simp [
    quznorThreeModeMu2,
    quznorSecondDerivativeFourierEnergy,
    quznorModePairEnergy,
    Complex.normSq_mul
  ]
  ring

end Chronos.Frontier
