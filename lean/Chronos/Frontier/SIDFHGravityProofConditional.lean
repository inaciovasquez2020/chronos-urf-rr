/-
  Conditional SIDFH gravity-recovery proof surface.

  This file does not prove full gravity recovery.  It proves only the bounded
  implication from the explicit remaining obligations recorded after the
  conserved-source surface.
-/

import Chronos.Frontier.SIDFHConservedSource

namespace Chronos
namespace Frontier

universe u

/--
The explicit remaining hypotheses needed before the SIDFH surface may be used
as a gravity-recovery package.

Each analytic or physical item is a proposition parameter.  This file supplies
no proof of those items; it only prevents them from being hidden.
-/
structure SIDFHGravityRecoveryObligations
    (ι : SIDFHIndexSurface.{u})
    (S : SIDFHSourceSurface ι)
    (Omega00WeakFieldAsymptotic : Prop)
    (FarFieldEquationBalance : Prop)
    (NewtonianRecovery : Prop)
    (LensingCompatibility : Prop)
    (PerturbativeStability : Prop)
    (BoundaryMatching : Prop) : Prop where
  conservedSource : ConservedSIDFHSource ι S
  omega00WeakFieldAsymptotic : Omega00WeakFieldAsymptotic
  farFieldEquationBalance : FarFieldEquationBalance
  newtonianRecovery : NewtonianRecovery
  lensingCompatibility : LensingCompatibility
  perturbativeStability : PerturbativeStability
  boundaryMatching : BoundaryMatching

/--
The conditional gravity-recovery target.

The conservation conclusion is projected into component form, while every
remaining analytic or physical requirement is carried explicitly.
-/
structure SIDFHGravityRecoveryConditional
    (ι : SIDFHIndexSurface.{u})
    (S : SIDFHSourceSurface ι)
    (Omega00WeakFieldAsymptotic : Prop)
    (FarFieldEquationBalance : Prop)
    (NewtonianRecovery : Prop)
    (LensingCompatibility : Prop)
    (PerturbativeStability : Prop)
    (BoundaryMatching : Prop) : Prop where
  conservedDivergence : ∀ ν : ι.Index, S.divergence ν
  omega00WeakFieldAsymptotic : Omega00WeakFieldAsymptotic
  farFieldEquationBalance : FarFieldEquationBalance
  newtonianRecovery : NewtonianRecovery
  lensingCompatibility : LensingCompatibility
  perturbativeStability : PerturbativeStability
  boundaryMatching : BoundaryMatching

/--
Conditional proof surface: if all named obligations are supplied, the
corresponding conditional recovery package follows.

This is the strongest theorem currently justified by the repository boundary.
-/
theorem sidfhGravityRecoveryConditional_from_obligations
    {ι : SIDFHIndexSurface.{u}}
    {S : SIDFHSourceSurface ι}
    {Omega00WeakFieldAsymptotic : Prop}
    {FarFieldEquationBalance : Prop}
    {NewtonianRecovery : Prop}
    {LensingCompatibility : Prop}
    {PerturbativeStability : Prop}
    {BoundaryMatching : Prop}
    (h :
      SIDFHGravityRecoveryObligations ι S
        Omega00WeakFieldAsymptotic
        FarFieldEquationBalance
        NewtonianRecovery
        LensingCompatibility
        PerturbativeStability
        BoundaryMatching) :
    SIDFHGravityRecoveryConditional ι S
      Omega00WeakFieldAsymptotic
      FarFieldEquationBalance
      NewtonianRecovery
      LensingCompatibility
      PerturbativeStability
      BoundaryMatching :=
  {
    conservedDivergence :=
      conservedSIDFHSource_divergence h.conservedSource
    omega00WeakFieldAsymptotic :=
      h.omega00WeakFieldAsymptotic
    farFieldEquationBalance :=
      h.farFieldEquationBalance
    newtonianRecovery :=
      h.newtonianRecovery
    lensingCompatibility :=
      h.lensingCompatibility
    perturbativeStability :=
      h.perturbativeStability
    boundaryMatching :=
      h.boundaryMatching
  }

/--
Boundary marker: this module proves no unconditional gravity theorem from the
current SIDFH surface.
-/
def unconditionalGravityProofFromCurrentSIDFHSurface : Prop :=
  False

end Frontier
end Chronos
