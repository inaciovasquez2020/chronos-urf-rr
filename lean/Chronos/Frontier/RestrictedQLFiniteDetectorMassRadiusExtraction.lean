import Mathlib
import Chronos.Frontier.RestrictedQLMassRadiusGateMonotonicity

namespace Chronos
namespace Frontier

variable {DetectorId : Type*} [Fintype DetectorId] [DecidableEq DetectorId]

/-- Sum of masses over active finite detectors. -/
def activeMass (mass : DetectorId → Nat) (active : DetectorId → Bool) : Nat :=
  (Finset.univ.filter (fun d => active d = true)).sum mass

/-- Finite detector extraction into the restricted quasi-local mass-radius sample. -/
def finiteDetectorMassRadiusExtraction
    (mass radius : DetectorId → Nat)
    (active : DetectorId → Bool)
    (activeRadiusFloor : Nat) :
    RestrictedQLMassRadiusSample :=
  { massRadius := activeMass mass active,
    concentrationRadius := activeRadiusFloor }

/-- Gate from supplied active-radius floor bound. -/
theorem finiteDetectorExtraction_gate_of_active_floor_le_mass
    (mass radius : DetectorId → Nat)
    (active : DetectorId → Bool)
    (activeRadiusFloor : Nat)
    (h : activeRadiusFloor ≤ activeMass mass active) :
    restrictedQLCollapseGate
      (finiteDetectorMassRadiusExtraction mass radius active activeRadiusFloor) := by
  dsimp [restrictedQLCollapseGate, finiteDetectorMassRadiusExtraction]
  exact h

/-- Active mass is monotone under pointwise detector-mass increase. -/
theorem finiteDetectorExtraction_activeMass_mono
    (mass mass' : DetectorId → Nat)
    (active : DetectorId → Bool)
    (hMass : ∀ d, mass d ≤ mass' d) :
    activeMass mass active ≤ activeMass mass' active := by
  dsimp [activeMass]
  exact Finset.sum_le_sum (fun d _ => hMass d)

/-- Extracted gate is preserved under pointwise detector-mass increase. -/
theorem finiteDetectorExtraction_gate_mono_mass
    (mass mass' radius : DetectorId → Nat)
    (active : DetectorId → Bool)
    (activeRadiusFloor : Nat)
    (hGate : restrictedQLCollapseGate
      (finiteDetectorMassRadiusExtraction mass radius active activeRadiusFloor))
    (hMass : ∀ d, mass d ≤ mass' d) :
    restrictedQLCollapseGate
      (finiteDetectorMassRadiusExtraction mass' radius active activeRadiusFloor) := by
  have hMono : activeMass mass active ≤ activeMass mass' active :=
    finiteDetectorExtraction_activeMass_mono mass mass' active hMass
  dsimp [restrictedQLCollapseGate, finiteDetectorMassRadiusExtraction] at hGate ⊢
  exact Nat.le_trans hGate hMono

end Frontier
end Chronos
