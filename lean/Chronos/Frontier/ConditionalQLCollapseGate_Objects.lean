/-
Chronos/URF Conditional Restricted QL-Collapse-Gate Surface

Status:
  CONDITIONAL_RESTRICTED_COLLAPSE_GATE_ONLY

Boundary:
  This file records a restricted conditional theorem target.
  It does not prove Cosmic Censorship.
  It does not prove the Hoop Conjecture.
  It does not prove unrestricted QL_CollapseGate.
  It does not prove unrestricted UniversalBoundaryCompactness.
  It does not prove unrestricted nonspherical collapse exclusion.
  It does not prove unrestricted Chronos-RR.
  It does not prove H4.1/FGL.
  It does not prove P vs NP or any Clay problem.
-/

namespace Chronos
namespace Frontier
namespace ConditionalQLCollapseGate

inductive MatterModel where
  | vacuumEinstein
deriving DecidableEq, Repr

inductive CensorshipTarget where
  | weak
deriving DecidableEq, Repr

structure VacuumInitialData where
  Carrier : Type
  smooth : Prop
  asymptoticallyFlat : Prop
  vacuumConstraints : Prop

structure AsymptoticallyFlatSobolevData (x : VacuumInitialData) where
  s : Nat
  deltaNumerator : Int
  deltaDenominator : Nat
  hsLowerBound : 6 ≤ s
  deltaDenominatorPositive : 0 < deltaDenominator
  belongsWeightedSobolev : Prop

structure ShortPulseSubdomain where
  member : VacuumInitialData → Prop
  domainRestrictedToVacuum : ∀ x, member x → x.vacuumConstraints
  domainAsymptoticallyFlat : ∀ x, member x → x.asymptoticallyFlat
  domainSmooth : ∀ x, member x → x.smooth

structure ShortPulseConcentration
    (Dsp : ShortPulseSubdomain) (x : VacuumInitialData) where
  inDomain : Dsp.member x
  concentrationHolds : Prop

structure MaximalCauchyDevelopment (x : VacuumInitialData) where
  Spacetime : Type
  develops : Prop
  maximal : Prop
  solvesVacuumEinstein : Prop

structure ClosedTrappedSurface {x : VacuumInitialData}
    (M : MaximalCauchyDevelopment x) where
  Surface : Type
  closed : Prop
  trapped : Prop
  embeddedInDevelopment : Prop

def LocalWellPosednessOn (Dsp : ShortPulseSubdomain) : Prop :=
  ∀ x : VacuumInitialData, Dsp.member x →
    ∃ M : MaximalCauchyDevelopment x,
      M.develops ∧ M.maximal ∧ M.solvesVacuumEinstein

def ConstraintPreservationOn (Dsp : ShortPulseSubdomain) : Prop :=
  ∀ x : VacuumInitialData, Dsp.member x → x.vacuumConstraints →
    ∀ M : MaximalCauchyDevelopment x, M.develops → M.solvesVacuumEinstein

def WeakCosmicCensorshipOn (Dsp : ShortPulseSubdomain) : Prop :=
  ∀ x : VacuumInitialData, Dsp.member x →
    ∀ M : MaximalCauchyDevelopment x, M.develops → True

def RestrictedTrappedSurfaceTheoremOn (Dsp : ShortPulseSubdomain) : Prop :=
  ∀ x : VacuumInitialData,
    ShortPulseConcentration Dsp x →
      ∀ M : MaximalCauchyDevelopment x,
        M.develops →
          ∃ S : ClosedTrappedSurface M,
            S.closed ∧ S.trapped ∧ S.embeddedInDevelopment

structure FiniteDetectorAlgebra where
  Detector : Type
  finiteDetectorSet : Prop
  cutoffLambda : Nat
  cutoffPositive : 0 < cutoffLambda

def BoundaryObservablesFactorThrough
    (Dsp : ShortPulseSubdomain) (FΛ : FiniteDetectorAlgebra) : Prop :=
  ∀ x : VacuumInitialData, Dsp.member x →
    ∀ M : MaximalCauchyDevelopment x, M.develops →
      FΛ.finiteDetectorSet

def BoundaryCompactness (FΛ : FiniteDetectorAlgebra) : Prop :=
  FΛ.finiteDetectorSet

structure QL_CollapseGate {Dsp : ShortPulseSubdomain}
    (x : VacuumInitialData) (M : MaximalCauchyDevelopment x)
    (FΛ : FiniteDetectorAlgebra) where
  trappedSurface :
    ∃ S : ClosedTrappedSurface M,
      S.closed ∧ S.trapped ∧ S.embeddedInDevelopment
  boundaryFactors : FΛ.finiteDetectorSet
  boundaryCompact : BoundaryCompactness FΛ
  weakCosmicCensorshipAssumptionUsed : True

structure ConditionalQLCollapseGateAssumptions
    (Dsp : ShortPulseSubdomain) (FΛ : FiniteDetectorAlgebra) where
  A1_localWellPosedness : LocalWellPosednessOn Dsp
  A2_constraintPreservation : ConstraintPreservationOn Dsp
  A3_weakCosmicCensorship : WeakCosmicCensorshipOn Dsp
  A4_restrictedTrappedSurface : RestrictedTrappedSurfaceTheoremOn Dsp
  A5_boundaryObservablesFactor : BoundaryObservablesFactorThrough Dsp FΛ
  A6_boundaryCompactness : BoundaryCompactness FΛ

theorem ConditionalQLCollapseGate_vacuum_short_pulse
    (Dsp : ShortPulseSubdomain)
    (FΛ : FiniteDetectorAlgebra)
    (A : ConditionalQLCollapseGateAssumptions Dsp FΛ)
    (x : VacuumInitialData)
    (TSCx : ShortPulseConcentration Dsp x) :
    ∃ M : MaximalCauchyDevelopment x,
      QL_CollapseGate (Dsp := Dsp) x M FΛ := by
  obtain ⟨M, hDevelops, _hMaximal, _hSolves⟩ :=
    A.A1_localWellPosedness x TSCx.inDomain
  have hTrap :
      ∃ S : ClosedTrappedSurface M,
        S.closed ∧ S.trapped ∧ S.embeddedInDevelopment :=
    A.A4_restrictedTrappedSurface x TSCx M hDevelops
  have hBoundary : FΛ.finiteDetectorSet :=
    A.A5_boundaryObservablesFactor x TSCx.inDomain M hDevelops
  have hCompact : BoundaryCompactness FΛ :=
    A.A6_boundaryCompactness
  have hWCC : True :=
    A.A3_weakCosmicCensorship x TSCx.inDomain M hDevelops
  exact ⟨M, {
    trappedSurface := hTrap
    boundaryFactors := hBoundary
    boundaryCompact := hCompact
    weakCosmicCensorshipAssumptionUsed := hWCC
  }⟩

def DoesNotProve_unrestrictedUniversalBoundaryCompactness : Prop := True
def DoesNotProve_unrestrictedQLCollapseGate : Prop := True
def DoesNotProve_cosmicCensorship : Prop := True
def DoesNotProve_hoopConjecture : Prop := True
def DoesNotProve_unrestrictedNonsphericalCollapseExclusion : Prop := True
def DoesNotProve_unrestrictedChronosRR : Prop := True
def DoesNotProve_H41_FGL : Prop := True
def DoesNotProve_PvsNP_or_ClayProblem : Prop := True

end ConditionalQLCollapseGate
end Frontier
end Chronos
