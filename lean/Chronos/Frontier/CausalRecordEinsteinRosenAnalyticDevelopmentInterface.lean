import Chronos.Frontier.CausalRecordEinsteinRosenGlobalDevelopmentReduction

namespace Chronos.Frontier

universe u v w

/--
Typed residual form of the selected Einstein--mesh--SIDFH initial-value system.

The intended equations are:

* harmonic-gauge Einstein residual = 0;
* mesh scalar residual = 0;
* SIDFH scalar residual = 0;
* Hamiltonian constraint residual = 0;
* momentum constraint residual = 0.

This structure fixes the equation and solution signatures.  It does not itself
construct the differential operators or prove PDE estimates.
-/
structure EinsteinMeshSIDFHEquationSystem (Time : Type u) where
  State : Type v
  Residual : Type w
  zeroResidual : Residual
  harmonicGaugeEinsteinResidual : Time → State → Residual
  meshScalarResidual : Time → State → Residual
  sidfhScalarResidual : Time → State → Residual
  hamiltonianConstraintResidual : State → Residual
  momentumConstraintResidual : State → Residual
  matchesInitialData : FilledConcreteInitialDataClass → State → Prop
  curvatureBounded : Time → State → Prop
  matterFieldsBounded : Time → State → Prop
  centerSymmetric : Time → State → Prop
  asymptoticFalloff : Time → State → Prop

namespace EinsteinMeshSIDFHEquationSystem

def SatisfiesEvolutionAt
    {Time : Type u}
    (E : EinsteinMeshSIDFHEquationSystem Time)
    (t : Time)
    (x : E.State) : Prop :=
  E.harmonicGaugeEinsteinResidual t x = E.zeroResidual ∧
  E.meshScalarResidual t x = E.zeroResidual ∧
  E.sidfhScalarResidual t x = E.zeroResidual

def SatisfiesConstraints
    {Time : Type u}
    (E : EinsteinMeshSIDFHEquationSystem Time)
    (x : E.State) : Prop :=
  E.hamiltonianConstraintResidual x = E.zeroResidual ∧
  E.momentumConstraintResidual x = E.zeroResidual

end EinsteinMeshSIDFHEquationSystem

/-- A solution on a represented local time slab. -/
structure EinsteinMeshSIDFHLocalSolution
    {Time : Type u}
    (E : EinsteinMeshSIDFHEquationSystem Time) where
  initialData : FilledConcreteInitialDataClass
  initialDataFilled : initialData.isFilled
  initialTime : Time
  finalTime : Time
  IsInSlab : Time → Prop
  initialTime_mem : IsInSlab initialTime
  finalTime_mem : IsInSlab finalTime
  trajectory : Time → E.State
  equations :
    ∀ t, IsInSlab t →
      E.SatisfiesEvolutionAt t (trajectory t)
  initialConstraints :
    E.SatisfiesConstraints (trajectory initialTime)
  initialDataMatch :
    E.matchesInitialData initialData (trajectory initialTime)

namespace EinsteinMeshSIDFHLocalSolution

def SameInitialData
    {Time : Type u}
    {E : EinsteinMeshSIDFHEquationSystem Time}
    (S T : EinsteinMeshSIDFHLocalSolution E) : Prop :=
  S.initialData = T.initialData ∧
  S.initialTime = T.initialTime ∧
  S.trajectory S.initialTime = T.trajectory T.initialTime

def AgreeOnOverlap
    {Time : Type u}
    {E : EinsteinMeshSIDFHEquationSystem Time}
    (S T : EinsteinMeshSIDFHLocalSolution E) : Prop :=
  ∀ t, S.IsInSlab t → T.IsInSlab t →
    S.trajectory t = T.trajectory t

def ContinuationBounds
    {Time : Type u}
    {E : EinsteinMeshSIDFHEquationSystem Time}
    (S : EinsteinMeshSIDFHLocalSolution E) : Prop :=
  ∀ t, S.IsInSlab t →
    E.curvatureBounded t (S.trajectory t) ∧
    E.matterFieldsBounded t (S.trajectory t)

def ExtendsSolution
    {Time : Type u}
    {E : EinsteinMeshSIDFHEquationSystem Time}
    (S T : EinsteinMeshSIDFHLocalSolution E) : Prop :=
  S.initialData = T.initialData ∧
  ∀ t, S.IsInSlab t →
    T.IsInSlab t ∧
    S.trajectory t = T.trajectory t

def PreservesCenterSymmetry
    {Time : Type u}
    {E : EinsteinMeshSIDFHEquationSystem Time}
    (S : EinsteinMeshSIDFHLocalSolution E) : Prop :=
  E.centerSymmetric S.initialTime (S.trajectory S.initialTime) →
  ∀ t, S.IsInSlab t →
    E.centerSymmetric t (S.trajectory t)

def PreservesAsymptoticFalloff
    {Time : Type u}
    {E : EinsteinMeshSIDFHEquationSystem Time}
    (S : EinsteinMeshSIDFHLocalSolution E) : Prop :=
  E.asymptoticFalloff S.initialTime (S.trajectory S.initialTime) →
  ∀ t, S.IsInSlab t →
    E.asymptoticFalloff t (S.trajectory t)

end EinsteinMeshSIDFHLocalSolution

/-- A global solution carrying the estimates needed by the topology route. -/
structure EinsteinMeshSIDFHGlobalSolution
    {Time : Type u}
    (E : EinsteinMeshSIDFHEquationSystem Time) where
  initialData : FilledConcreteInitialDataClass
  initialDataFilled : initialData.isFilled
  initialTime : Time
  trajectory : Time → E.State
  equations :
    ∀ t, E.SatisfiesEvolutionAt t (trajectory t)
  initialConstraints :
    E.SatisfiesConstraints (trajectory initialTime)
  initialDataMatch :
    E.matchesInitialData initialData (trajectory initialTime)
  curvatureBounded :
    ∀ t, E.curvatureBounded t (trajectory t)
  matterFieldsBounded :
    ∀ t, E.matterFieldsBounded t (trajectory t)
  centerSymmetry :
    ∀ t, E.centerSymmetric t (trajectory t)
  asymptoticFalloff :
    ∀ t, E.asymptoticFalloff t (trajectory t)
  globallyHyperbolic : Prop
  globallyHyperbolic_proved : globallyHyperbolic

/--
The exact analytic theorem package still required.

No field below is manufactured by the present repository.  A genuine closure
must instantiate these fields from a Sobolev-space hyperbolic PDE theory.
-/
structure EinsteinMeshSIDFHAnalyticTheoremPackage
    {Time : Type u}
    (E : EinsteinMeshSIDFHEquationSystem Time) where
  localExistence :
    ∀ D : FilledConcreteInitialDataClass,
      D.isFilled →
      ∃ S : EinsteinMeshSIDFHLocalSolution E,
        S.initialData = D
  localUniqueness :
    ∀ S T : EinsteinMeshSIDFHLocalSolution E,
      S.SameInitialData T →
      S.AgreeOnOverlap T
  continuationCriterion :
    ∀ S : EinsteinMeshSIDFHLocalSolution E,
      S.ContinuationBounds →
      ∃ T : EinsteinMeshSIDFHLocalSolution E,
        S.ExtendsSolution T
  centerSymmetryPreservation :
    ∀ S : EinsteinMeshSIDFHLocalSolution E,
      S.PreservesCenterSymmetry
  asymptoticFalloffPreservation :
    ∀ S : EinsteinMeshSIDFHLocalSolution E,
      S.PreservesAsymptoticFalloff
  globalExistenceFromLocalContinuation :
    ∀ D : FilledConcreteInitialDataClass,
      D.isFilled →
      ∃ S : EinsteinMeshSIDFHGlobalSolution E,
        S.initialData = D

theorem localExistence_of_analyticPackage
    {Time : Type u}
    {E : EinsteinMeshSIDFHEquationSystem Time}
    (P : EinsteinMeshSIDFHAnalyticTheoremPackage E)
    (D : FilledConcreteInitialDataClass)
    (hD : D.isFilled) :
    ∃ S : EinsteinMeshSIDFHLocalSolution E,
      S.initialData = D :=
  P.localExistence D hD

theorem localUniqueness_of_analyticPackage
    {Time : Type u}
    {E : EinsteinMeshSIDFHEquationSystem Time}
    (P : EinsteinMeshSIDFHAnalyticTheoremPackage E)
    (S T : EinsteinMeshSIDFHLocalSolution E)
    (hInitial : S.SameInitialData T) :
    S.AgreeOnOverlap T :=
  P.localUniqueness S T hInitial

theorem continuation_of_curvature_and_matter_bounds
    {Time : Type u}
    {E : EinsteinMeshSIDFHEquationSystem Time}
    (P : EinsteinMeshSIDFHAnalyticTheoremPackage E)
    (S : EinsteinMeshSIDFHLocalSolution E)
    (hBounds : S.ContinuationBounds) :
    ∃ T : EinsteinMeshSIDFHLocalSolution E,
      S.ExtendsSolution T :=
  P.continuationCriterion S hBounds

theorem centerSymmetry_preserved_of_analyticPackage
    {Time : Type u}
    {E : EinsteinMeshSIDFHEquationSystem Time}
    (P : EinsteinMeshSIDFHAnalyticTheoremPackage E)
    (S : EinsteinMeshSIDFHLocalSolution E) :
    S.PreservesCenterSymmetry :=
  P.centerSymmetryPreservation S

theorem asymptoticFalloff_preserved_of_analyticPackage
    {Time : Type u}
    {E : EinsteinMeshSIDFHEquationSystem Time}
    (P : EinsteinMeshSIDFHAnalyticTheoremPackage E)
    (S : EinsteinMeshSIDFHLocalSolution E) :
    S.PreservesAsymptoticFalloff :=
  P.asymptoticFalloffPreservation S

namespace EinsteinMeshSIDFHGlobalSolution

/--
A certified global analytic solution produces the exact carrier used by
PR #1166.  The spatial topology is represented in one fixed `R3` chart.
-/
def toGlobalHyperbolicR3Development
    {Time : Type u}
    {α : Type v}
    {E : EinsteinMeshSIDFHEquationSystem Time}
    (S : EinsteinMeshSIDFHGlobalSolution E)
    (recordPrefix : Nat → List α)
    (recordPrefixSucc :
      ∀ d, ∃ a, recordPrefix (d + 1) = recordPrefix d ++ [a]) :
    GlobalHyperbolicR3Development Time α where
  initialData :=
    S.initialData
  initialDataFilled :=
    S.initialDataFilled
  initialTime :=
    S.initialTime
  evolutionFlow :=
    fun _ _ => Homeomorph.refl R3
  evolutionFixesCenter := by
    intro _ _
    rfl
  globallyHyperbolic :=
    S.globallyHyperbolic
  globallyHyperbolic_proved :=
    S.globallyHyperbolic_proved
  recordPrefix :=
    recordPrefix
  recordPrefixSucc :=
    recordPrefixSucc
  boundedCurvatureAtCenter :=
    fun t => E.curvatureBounded t (S.trajectory t)
  boundedCurvatureAtCenter_proved :=
    S.curvatureBounded
  evolutionEquationAtCenter :=
    fun t => E.SatisfiesEvolutionAt t (S.trajectory t)
  evolutionEquationAtCenter_proved :=
    S.equations
  asymptoticFalloff :=
    fun t => E.asymptoticFalloff t (S.trajectory t)
  asymptoticFalloff_proved :=
    S.asymptoticFalloff

end EinsteinMeshSIDFHGlobalSolution

theorem globalDevelopmentExists_of_analyticPackage
    {Time : Type u}
    {α : Type v}
    {E : EinsteinMeshSIDFHEquationSystem Time}
    (P : EinsteinMeshSIDFHAnalyticTheoremPackage E)
    (D : FilledConcreteInitialDataClass)
    (hD : D.isFilled)
    (recordPrefix : Nat → List α)
    (recordPrefixSucc :
      ∀ d, ∃ a, recordPrefix (d + 1) = recordPrefix d ++ [a]) :
    EinsteinMeshSIDFHGlobalDevelopmentExists Time α D := by
  rcases P.globalExistenceFromLocalContinuation D hD with ⟨S, hS⟩
  refine
    ⟨S.toGlobalHyperbolicR3Development
        recordPrefix
        recordPrefixSucc,
      ?_⟩
  exact hS

theorem restrictedNonRealization_of_analyticPackage
    {Time : Type u}
    {α : Type v}
    {E : EinsteinMeshSIDFHEquationSystem Time}
    (P : EinsteinMeshSIDFHAnalyticTheoremPackage E)
    (D : FilledConcreteInitialDataClass)
    (hD : D.isFilled)
    (recordPrefix : Nat → List α)
    (recordPrefixSucc :
      ∀ d, ∃ a, recordPrefix (d + 1) = recordPrefix d ++ [a]) :
    ∃ G : GlobalHyperbolicR3Development Time α,
      G.initialData = D ∧
      ∀ t : Time,
        G.RestrictedNonRealizationConclusion t := by
  apply restrictedNonRealization_reduced_to_globalDevelopmentExistence D
  exact
    globalDevelopmentExists_of_analyticPackage
      P
      D
      hD
      recordPrefix
      recordPrefixSucc

def einsteinMeshSIDFHAnalyticRouteStatus : String :=
  "EQUATIONS_AND_SOLUTION_TYPES_DEFINED_CONDITIONAL_ON_ANALYTIC_THEOREM_PACKAGE"

def einsteinMeshSIDFHAnalyticRouteMissingObject : String :=
  "SOBOLEV_HYPERBOLIC_LOCAL_WELLPOSEDNESS_CONTINUATION_AND_GLOBALIZATION_PROOF"

end Chronos.Frontier
