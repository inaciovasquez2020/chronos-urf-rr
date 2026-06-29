/-
  Conditional SIDFH Omega00-to-flat-curve surface.

  This file does not derive the weak-field Omega00 asymptotic from the bridge
  tensor.  It records the bounded consequence that, once the Omega00 asymptotic,
  far-field balance, circular-orbit law, and a derivation rule are supplied, the
  flat-rotation limit follows and can be attached to the existing conditional
  gravity-recovery package.
-/

import Chronos.Frontier.SIDFHGravityProofConditional

namespace Chronos
namespace Frontier

universe u

/--
A rule saying that the weak-field Omega00 asymptotic, the far-field equation
balance, and the circular-orbit law imply the desired flat-rotation limit.

The rule is explicit because the repository has not derived the sign, factor,
or field-equation balance from the proposed bridge tensor.
-/
structure SIDFHFlatCurveDerivationRule
    (Omega00WeakFieldAsymptotic : Prop)
    (FarFieldEquationBalance : Prop)
    (CircularOrbitLaw : Prop)
    (FlatRotationCurveLimit : Prop) : Prop where
  deriveFlatRotation :
    Omega00WeakFieldAsymptotic →
    FarFieldEquationBalance →
    CircularOrbitLaw →
    FlatRotationCurveLimit

/--
Given the current conditional gravity obligations plus a circular-orbit law and
an explicit flat-curve derivation rule, the flat-rotation limit follows.
-/
theorem sidfhFlatRotationLimit_from_gravity_obligations
    {ι : SIDFHIndexSurface.{u}}
    {S : SIDFHSourceSurface ι}
    {Omega00WeakFieldAsymptotic : Prop}
    {FarFieldEquationBalance : Prop}
    {NewtonianRecovery : Prop}
    {LensingCompatibility : Prop}
    {PerturbativeStability : Prop}
    {BoundaryMatching : Prop}
    {CircularOrbitLaw : Prop}
    {FlatRotationCurveLimit : Prop}
    (hG :
      SIDFHGravityRecoveryObligations ι S
        Omega00WeakFieldAsymptotic
        FarFieldEquationBalance
        NewtonianRecovery
        LensingCompatibility
        PerturbativeStability
        BoundaryMatching)
    (hCircular : CircularOrbitLaw)
    (hRule :
      SIDFHFlatCurveDerivationRule
        Omega00WeakFieldAsymptotic
        FarFieldEquationBalance
        CircularOrbitLaw
        FlatRotationCurveLimit) :
    FlatRotationCurveLimit :=
  hRule.deriveFlatRotation
    hG.omega00WeakFieldAsymptotic
    hG.farFieldEquationBalance
    hCircular

/--
The existing conditional gravity-recovery package together with the derived
flat-rotation limit.
-/
structure SIDFHGravityRecoveryWithFlatCurveConditional
    (ι : SIDFHIndexSurface.{u})
    (S : SIDFHSourceSurface ι)
    (Omega00WeakFieldAsymptotic : Prop)
    (FarFieldEquationBalance : Prop)
    (NewtonianRecovery : Prop)
    (LensingCompatibility : Prop)
    (PerturbativeStability : Prop)
    (BoundaryMatching : Prop)
    (FlatRotationCurveLimit : Prop) : Prop where
  gravityRecovery :
    SIDFHGravityRecoveryConditional ι S
      Omega00WeakFieldAsymptotic
      FarFieldEquationBalance
      NewtonianRecovery
      LensingCompatibility
      PerturbativeStability
      BoundaryMatching
  flatRotationCurveLimit : FlatRotationCurveLimit

/--
Conditional package theorem: all gravity-recovery obligations plus an explicit
Omega00/far-field/circular-orbit derivation rule produce a conditional recovery
package carrying the flat-rotation limit.
-/
theorem sidfhGravityRecoveryWithFlatCurveConditional_from_obligations
    {ι : SIDFHIndexSurface.{u}}
    {S : SIDFHSourceSurface ι}
    {Omega00WeakFieldAsymptotic : Prop}
    {FarFieldEquationBalance : Prop}
    {NewtonianRecovery : Prop}
    {LensingCompatibility : Prop}
    {PerturbativeStability : Prop}
    {BoundaryMatching : Prop}
    {CircularOrbitLaw : Prop}
    {FlatRotationCurveLimit : Prop}
    (hG :
      SIDFHGravityRecoveryObligations ι S
        Omega00WeakFieldAsymptotic
        FarFieldEquationBalance
        NewtonianRecovery
        LensingCompatibility
        PerturbativeStability
        BoundaryMatching)
    (hCircular : CircularOrbitLaw)
    (hRule :
      SIDFHFlatCurveDerivationRule
        Omega00WeakFieldAsymptotic
        FarFieldEquationBalance
        CircularOrbitLaw
        FlatRotationCurveLimit) :
    SIDFHGravityRecoveryWithFlatCurveConditional ι S
      Omega00WeakFieldAsymptotic
      FarFieldEquationBalance
      NewtonianRecovery
      LensingCompatibility
      PerturbativeStability
      BoundaryMatching
      FlatRotationCurveLimit :=
  {
    gravityRecovery :=
      sidfhGravityRecoveryConditional_from_obligations hG
    flatRotationCurveLimit :=
      sidfhFlatRotationLimit_from_gravity_obligations hG hCircular hRule
  }

/--
Boundary marker: the current repository still does not derive the Omega00
weak-field asymptotic from the proposed bridge tensor.
-/
def omega00WeakFieldAsymptoticDerivedFromBridgeTensor : Prop :=
  False

end Frontier
end Chronos
