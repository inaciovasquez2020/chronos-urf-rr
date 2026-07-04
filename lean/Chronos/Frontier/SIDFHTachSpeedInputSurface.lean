import Mathlib.Data.Real.Basic

namespace Chronos.Frontier

structure SIDFHTachSpeedInputSurface where
  State : Type
  admissible : State → Prop
  speed : State → ℝ
  properTimeRate : State → ℝ
  v_min : ℝ
  c : ℝ
  v_min_positive : 0 < v_min
  c_positive : 0 < c
  admissible_speed_nonnegative :
    ∀ s, admissible s → 0 ≤ speed s
  admissible_speed_below_light :
    ∀ s, admissible s → speed s < c
  admissible_moving_speed_lower_bound :
    ∀ s, admissible s → speed s ≠ 0 → v_min ≤ speed s
  slower_moves_faster_in_time :
    ∀ s t,
      admissible s →
      admissible t →
      speed s < speed t →
      properTimeRate t < properTimeRate s

def SIDFHTachSpeedProofTarget : Prop :=
  Nonempty SIDFHTachSpeedInputSurface

theorem sidfhTachSpeedProofTarget_from_input
    (S : SIDFHTachSpeedInputSurface) :
    SIDFHTachSpeedProofTarget :=
  ⟨S⟩

def sidfhTachSpeedUniversalPhysicalClosureBoundary : Prop :=
  ¬ SIDFHTachSpeedProofTarget → True

end Chronos.Frontier
