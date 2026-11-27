import CommonFutureVolume

open MeasureTheory
open scoped ENNReal

namespace Chronos.FourEvent

example (a b T : ℝ) (ha : 0 < a) (hb : 0 ≤ b) (hT : a + b < T) :
    (volume : Measure Event) (axialLens a b T) =
      ENNReal.ofReal (Real.pi * (T + 2 * a) * ((T - a)^2 - b^2)^2 / (24 * T)) := by
  rw [axialLens_volume_eq_lintegral]
  unfold axialWidth
  done

end Chronos.FourEvent
