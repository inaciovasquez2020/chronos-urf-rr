import Mathlib
import Chronos.Frontier.RestrictedQLFiniteDetectorMassRadiusExtraction

namespace Chronos
namespace Frontier

variable {DetectorId : Type*} [Fintype DetectorId]

/-- The finite set of active detectors. -/
def activeDetectors (active : DetectorId → Bool) : Finset DetectorId :=
  Finset.univ.filter (fun d => active d = true)

/-- The finite set of active detector-radius values. -/
def activeRadiusValues
    (radius : DetectorId → Nat)
    (active : DetectorId → Bool) : Finset Nat :=
  (activeDetectors active).image radius

/--
Computed minimum active radius.

This is defined only under an explicit nonempty-radius-values certificate.
The empty-active-detector default is intentionally not handled here.
-/
def computedActiveRadiusMinimum
    (radius : DetectorId → Nat)
    (active : DetectorId → Bool)
    (hNonempty : (activeRadiusValues radius active).Nonempty) : Nat :=
  (activeRadiusValues radius active).min' hNonempty

/-- An active detector contributes its radius to the active-radius value set. -/
theorem active_radius_mem_values_of_active
    (radius : DetectorId → Nat)
    (active : DetectorId → Bool)
    (d : DetectorId)
    (hActive : active d = true) :
    radius d ∈ activeRadiusValues radius active := by
  dsimp [activeRadiusValues, activeDetectors]
  exact Finset.mem_image.mpr ⟨d, by simp [hActive], rfl⟩

/-- The computed active-radius minimum is below every active detector radius. -/
theorem computedActiveRadiusMinimum_le_active_radius
    (radius : DetectorId → Nat)
    (active : DetectorId → Bool)
    (hNonempty : (activeRadiusValues radius active).Nonempty)
    (d : DetectorId)
    (hActive : active d = true) :
    computedActiveRadiusMinimum radius active hNonempty ≤ radius d := by
  dsimp [computedActiveRadiusMinimum]
  exact Finset.min'_le
    (activeRadiusValues radius active)
    (radius d)
    (active_radius_mem_values_of_active radius active d hActive)

/--
Gate extraction using the computed finite active-radius minimum.

This replaces the previously supplied explicit active-radius floor with the
computed finite minimum, under a nonempty active-radius-values certificate.
-/
theorem finiteDetectorExtraction_gate_of_computed_min_le_mass
    (mass radius : DetectorId → Nat)
    (active : DetectorId → Bool)
    (hNonempty : (activeRadiusValues radius active).Nonempty)
    (hMassGate :
      computedActiveRadiusMinimum radius active hNonempty ≤ activeMass mass active) :
    restrictedQLCollapseGate
      (finiteDetectorMassRadiusExtraction
        mass radius active
        (computedActiveRadiusMinimum radius active hNonempty)) :=
  finiteDetectorExtraction_gate_of_active_floor_le_mass
    mass radius active
    (computedActiveRadiusMinimum radius active hNonempty)
    hMassGate

/--
The computed-minimum extracted gate is preserved under pointwise detector-mass
increase.
-/
theorem finiteDetectorExtraction_computed_min_gate_mono_mass
    (mass mass' radius : DetectorId → Nat)
    (active : DetectorId → Bool)
    (hNonempty : (activeRadiusValues radius active).Nonempty)
    (hGate : restrictedQLCollapseGate
      (finiteDetectorMassRadiusExtraction
        mass radius active
        (computedActiveRadiusMinimum radius active hNonempty)))
    (hMass : ∀ d, mass d ≤ mass' d) :
    restrictedQLCollapseGate
      (finiteDetectorMassRadiusExtraction
        mass' radius active
        (computedActiveRadiusMinimum radius active hNonempty)) :=
  finiteDetectorExtraction_gate_mono_mass
    mass mass' radius active
    (computedActiveRadiusMinimum radius active hNonempty)
    hGate hMass

end Frontier
end Chronos
