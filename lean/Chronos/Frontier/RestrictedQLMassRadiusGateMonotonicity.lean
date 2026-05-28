namespace Chronos
namespace Frontier

/--
A finite, restricted quasi-local mass-radius gate.

This is not a hoop theorem, not cosmic censorship, and not a PDE result.
It is only the local arithmetic gate used by later restricted gravity
certificates: a collapse-gate flag is active when the concentration radius
is bounded by the available quasi-local mass-radius budget.
-/
structure RestrictedQLMassRadiusSample where
  massRadius : Nat
  concentrationRadius : Nat
deriving Repr, DecidableEq

def restrictedQLCollapseGate
    (s : RestrictedQLMassRadiusSample) : Prop :=
  s.concentrationRadius ≤ s.massRadius

/--
Solved local gravity certificate transport:

once the restricted quasi-local mass-radius collapse gate is active,
increasing the available mass-radius budget preserves the gate.
-/
theorem restrictedQLCollapseGate_mono_massRadius
    (s : RestrictedQLMassRadiusSample)
    (newMassRadius : Nat)
    (hGate : restrictedQLCollapseGate s)
    (hMono : s.massRadius ≤ newMassRadius) :
    restrictedQLCollapseGate
      { massRadius := newMassRadius,
        concentrationRadius := s.concentrationRadius } :=
  Nat.le_trans hGate hMono

/--
Zero-budget rigidity for the same restricted gate:
if the available mass-radius budget is zero and the gate is active,
then the concentration radius is forced to be zero.
-/
theorem restrictedQLCollapseGate_zero_mass_rigid
    (s : RestrictedQLMassRadiusSample)
    (hMassZero : s.massRadius = 0)
    (hGate : restrictedQLCollapseGate s) :
    s.concentrationRadius = 0 := by
  cases s with
  | mk massRadius concentrationRadius =>
      dsimp [restrictedQLCollapseGate] at hGate hMassZero ⊢
      rw [hMassZero] at hGate
      exact Nat.eq_zero_of_le_zero hGate

end Frontier
end Chronos
