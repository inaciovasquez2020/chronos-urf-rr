namespace Chronos.Frontier.Gravity

structure NonSphericalStabilityInput where
  sphericalState : Type
  nonsphericalState : Type
  sphericalEntropyMass : sphericalState → Nat
  nonsphericalEntropyMass : nonsphericalState → Nat
  transfer : nonsphericalState → sphericalState
  perturbativeStabilityModulus : Nat
  modulusPositive : perturbativeStabilityModulus > 0
  stabilityLowerBound :
    ∀ y : nonsphericalState,
      nonsphericalEntropyMass y ≥ perturbativeStabilityModulus
  sphericalGap : Prop

def NonSphericalStabilityTransfer (I : NonSphericalStabilityInput) : Prop :=
  I.sphericalGap →
    ∃ ε : Nat, ε > 0 ∧ ∀ y : I.nonsphericalState, I.nonsphericalEntropyMass y ≥ ε

theorem nonspherical_stability_transfer_conditional
    (I : NonSphericalStabilityInput) :
    NonSphericalStabilityTransfer I := by
  intro _hgap
  exact ⟨I.perturbativeStabilityModulus, I.modulusPositive, I.stabilityLowerBound⟩

end Chronos.Frontier.Gravity
