import Mathlib
import Chronos.Frontier.ComputedActiveRadiusMinimum

namespace Chronos
namespace Frontier

variable {DetectorId : Type*} [Fintype DetectorId]

/--
Default active-radius floor.

If active radius values are nonempty, use the computed finite minimum.
If there are no active radius values, use the explicit default floor `0`.
-/
def defaultActiveRadiusFloor
    (radius : DetectorId → Nat)
    (active : DetectorId → Bool) : Nat :=
  if h : (activeRadiusValues radius active).Nonempty then
    computedActiveRadiusMinimum radius active h
  else
    0

/-- On the nonempty branch, the default floor is the computed active-radius minimum. -/
theorem defaultActiveRadiusFloor_eq_computed_of_nonempty
    (radius : DetectorId → Nat)
    (active : DetectorId → Bool)
    (hNonempty : (activeRadiusValues radius active).Nonempty) :
    defaultActiveRadiusFloor radius active =
      computedActiveRadiusMinimum radius active hNonempty := by
  dsimp [defaultActiveRadiusFloor]
  rw [dif_pos hNonempty]

/-- On the empty branch, the default floor is zero. -/
theorem defaultActiveRadiusFloor_eq_zero_of_empty
    (radius : DetectorId → Nat)
    (active : DetectorId → Bool)
    (hEmpty : ¬ (activeRadiusValues radius active).Nonempty) :
    defaultActiveRadiusFloor radius active = 0 := by
  dsimp [defaultActiveRadiusFloor]
  rw [dif_neg hEmpty]

/-- If there are no active detectors, then the active-radius value set is empty. -/
theorem activeRadiusValues_empty_of_no_active
    (radius : DetectorId → Nat)
    (active : DetectorId → Bool)
    (hNoActive : activeDetectors active = ∅) :
    activeRadiusValues radius active = ∅ := by
  dsimp [activeRadiusValues]
  rw [hNoActive]
  simp

/-- If there are no active detectors, then active mass is zero. -/
theorem activeMass_eq_zero_of_no_active
    (mass : DetectorId → Nat)
    (active : DetectorId → Bool)
    (hNoActive : activeDetectors active = ∅) :
    activeMass mass active = 0 := by
  dsimp [activeMass, activeDetectors] at hNoActive ⊢
  rw [hNoActive]
  simp

/-- If there are no active detectors, then the default active-radius floor is zero. -/
theorem defaultActiveRadiusFloor_eq_zero_of_no_active
    (radius : DetectorId → Nat)
    (active : DetectorId → Bool)
    (hNoActive : activeDetectors active = ∅) :
    defaultActiveRadiusFloor radius active = 0 := by
  apply defaultActiveRadiusFloor_eq_zero_of_empty
  rw [activeRadiusValues_empty_of_no_active radius active hNoActive]
  simp

/-- Gate extraction using the default active-radius floor. -/
theorem finiteDetectorExtraction_gate_of_default_floor_le_mass
    (mass radius : DetectorId → Nat)
    (active : DetectorId → Bool)
    (h : defaultActiveRadiusFloor radius active ≤ activeMass mass active) :
    restrictedQLCollapseGate
      (finiteDetectorMassRadiusExtraction
        mass radius active
        (defaultActiveRadiusFloor radius active)) :=
  finiteDetectorExtraction_gate_of_active_floor_le_mass
    mass radius active
    (defaultActiveRadiusFloor radius active)
    h

/--
If there are no active detectors, the default floor and active mass are both zero,
so the restricted extraction gate holds trivially.
-/
theorem finiteDetectorExtraction_no_active_default_gate
    (mass radius : DetectorId → Nat)
    (active : DetectorId → Bool)
    (hNoActive : activeDetectors active = ∅) :
    restrictedQLCollapseGate
      (finiteDetectorMassRadiusExtraction
        mass radius active
        (defaultActiveRadiusFloor radius active)) := by
  have hFloor : defaultActiveRadiusFloor radius active = 0 :=
    defaultActiveRadiusFloor_eq_zero_of_no_active radius active hNoActive
  have hMass : activeMass mass active = 0 :=
    activeMass_eq_zero_of_no_active mass active hNoActive
  exact finiteDetectorExtraction_gate_of_default_floor_le_mass
    mass radius active
    (by
      rw [hFloor, hMass])

end Frontier
end Chronos
