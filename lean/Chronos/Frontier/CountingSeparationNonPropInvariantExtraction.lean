import Chronos.Frontier.CountingToMassUnderNonPropInvariant

namespace Chronos.Frontier

/--
Weakest remaining bridge after `CountingToMassUnderNonPropInvariant`.

This states the exact missing theorem-level object needed to turn ordinary
counting separation into the NonProp-invariant form already sufficient for
fiber mass balance.
-/
structure CountingSeparationNonPropInvariantInput where
  α : Type
  countingFiberSeparationFromNonProp : Prop
  nonPropInvariant : Prop
  extraction : countingFiberSeparationFromNonProp → nonPropInvariant

def CountingSeparationSuppliesNonPropInvariant
    (I : CountingSeparationNonPropInvariantInput) : Prop :=
  I.countingFiberSeparationFromNonProp → I.nonPropInvariant

theorem counting_separation_supplies_nonprop_invariant
    (I : CountingSeparationNonPropInvariantInput) :
    CountingSeparationSuppliesNonPropInvariant I :=
  I.extraction

/--
Composes the newly isolated extraction bridge with the already-verified
counting-to-mass-under-NonProp-invariant bridge.
-/
structure CountingSeparationToMassViaNonPropInvariantInput where
  countingFiberSeparationFromNonProp : Prop
  nonPropInvariant : Prop
  fiberMassBalanceFromNonProp : Prop
  extraction : countingFiberSeparationFromNonProp → nonPropInvariant
  counting_to_mass_under_invariant :
    countingFiberSeparationFromNonProp →
    nonPropInvariant →
    fiberMassBalanceFromNonProp

def CountingSeparationToMassViaNonPropInvariant
    (I : CountingSeparationToMassViaNonPropInvariantInput) : Prop :=
  I.countingFiberSeparationFromNonProp → I.fiberMassBalanceFromNonProp

theorem counting_separation_to_mass_via_nonprop_invariant
    (I : CountingSeparationToMassViaNonPropInvariantInput) :
    CountingSeparationToMassViaNonPropInvariant I := by
  intro hCounting
  exact I.counting_to_mass_under_invariant hCounting (I.extraction hCounting)

end Chronos.Frontier
