import Chronos.Frontier.FiniteSupportFiberMassUniformFloor

namespace Chronos
namespace Frontier

/--
Restricted Chronos-RR surface induced by finite positive support.

This is deliberately restricted to the finite-support domain.  It does not
state or imply unrestricted Chronos-RR.
-/
def RestrictedChronosRRFromFiniteSupport
    (D : FiniteSupportPositiveFiberMass) : Prop :=
  RestrictedUniversalFiberEntropyGapFromFiniteSupport D

/--
Restricted UniversalFiberEntropyGap on finite support feeds the restricted
Chronos-RR surface.
-/
theorem restricted_chronos_rr_from_restricted_universal_fiber_entropy_gap_finite_support
    (D : FiniteSupportPositiveFiberMass)
    (hGap : RestrictedUniversalFiberEntropyGapFromFiniteSupport D) :
    RestrictedChronosRRFromFiniteSupport D := by
  exact hGap

/--
Finite positive support gives restricted Chronos-RR through the already
closed finite-support uniform-floor and restricted UFEG route.
-/
theorem finite_support_restricted_chronos_rr
    (D : FiniteSupportPositiveFiberMass) :
    RestrictedChronosRRFromFiniteSupport D := by
  exact restricted_chronos_rr_from_restricted_universal_fiber_entropy_gap_finite_support
    D
    (restricted_universal_fiber_entropy_gap_from_finite_support D)

/--
Boundary witness: the unrestricted arbitrary-fiber-mass obstruction remains
available after the finite-support restricted construction.
-/
theorem finite_support_restricted_chronos_rr_preserves_unconditional_ufeg_obstruction :
    ∃ D : ArbitraryFiberMassData, ¬ FiberMassUniformFloor D :=
  unconditional_universal_fiber_entropy_gap_obstructed

end Frontier
end Chronos
