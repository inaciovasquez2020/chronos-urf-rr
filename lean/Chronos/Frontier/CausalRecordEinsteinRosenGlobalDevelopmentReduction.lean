import Chronos.Frontier.CausalRecordEinsteinRosenRestrictedNonRealization
import Chronos.Frontier.FilledConcreteInitialDataClass

namespace Chronos.Frontier

universe u w

/--
A single certified global development carrier for the restricted
causal-record Einstein--Rosen route.

This is the reduced interface replacing the four separate arguments of
`causalRecordRestrictedEinsteinRosenNonRealization`.

The remaining analytic boundary is existence of this carrier from the chosen
Einstein--mesh--SIDFH initial-value problem.
-/
structure GlobalHyperbolicR3Development
    (Time : Type u)
    (α : Type w) where
  initialData :
    FilledConcreteInitialDataClass
  initialDataFilled :
    initialData.isFilled
  initialTime :
    Time
  evolutionFlow :
    ∀ (_s _t : Time), R3 ≃ₜ R3
  evolutionFixesCenter :
    ∀ (s t : Time), evolutionFlow s t (0 : R3) = 0
  globallyHyperbolic :
    Prop
  globallyHyperbolic_proved :
    globallyHyperbolic
  recordPrefix :
    Nat → List α
  recordPrefixSucc :
    ∀ d, ∃ a, recordPrefix (d + 1) = recordPrefix d ++ [a]
  boundedCurvatureAtCenter :
    Time → Prop
  boundedCurvatureAtCenter_proved :
    ∀ t, boundedCurvatureAtCenter t
  evolutionEquationAtCenter :
    Time → Prop
  evolutionEquationAtCenter_proved :
    ∀ t, evolutionEquationAtCenter t
  asymptoticFalloff :
    Time → Prop
  asymptoticFalloff_proved :
    ∀ t, asymptoticFalloff t

namespace GlobalHyperbolicR3Development

/-- The fixed `ℝ³` foliation produces the slice-evolution carrier. -/
def sliceEvolution
    {Time : Type u}
    {α : Type w}
    (G : GlobalHyperbolicR3Development Time α) :
    SliceEvolution Time where
  Slice :=
    fun _ =>
      {
        carrier := R3
        topology := inferInstance
      }
  initialTime :=
    G.initialTime
  evolutionHomeomorph :=
    G.evolutionFlow
  initialR3Homeomorph :=
    Homeomorph.refl R3

/--
The canonical decoded core used by this reduction is the standard closed
three-ball on every prefix.

This derives the topological three-ball and nesting obligations, but it does
not yet derive a nontrivial shrinking physical core from the field equations.
-/
def canonicalDecodedCoreSystem
    {Time : Type u}
    {α : Type w}
    (G : GlobalHyperbolicR3Development Time α) :
    DecodedCoreSystem Time α G.sliceEvolution where
  recordPrefix :=
    G.recordPrefix
  prefixSucc :=
    G.recordPrefixSucc
  decode :=
    fun _ _ => (Metric.closedBall (0 : R3) 1 : Set R3)
  decodeAntitone := by
    intro _ _ _ _ x hx
    exact hx
  coreChart := by
    intro _ _
    refine ⟨?_⟩
    exact Homeomorph.refl ClosedBall3

/--
Regularity is the conjunction of:
* being the invariant center;
* bounded curvature at that center;
* satisfaction of the selected evolution equation there.
-/
def canonicalCenterSystem
    {Time : Type u}
    {α : Type w}
    (G : GlobalHyperbolicR3Development Time α) :
    CenterSystem Time G.sliceEvolution where
  center :=
    fun _ => (0 : R3)
  IsCenter :=
    fun _ x => x = (0 : R3)
  RegularAt :=
    fun t x =>
      x = (0 : R3) ∧
      G.boundedCurvatureAtCenter t ∧
      G.evolutionEquationAtCenter t
  centerCharacterization := by
    intro _ _
    rfl
  centerTransport :=
    G.evolutionFixesCenter
  regularTransport := by
    intro s t x
    constructor
    · rintro ⟨hx, _, _⟩
      refine
        ⟨?_,
          G.boundedCurvatureAtCenter_proved t,
          G.evolutionEquationAtCenter_proved t⟩
      rw [hx]
      exact G.evolutionFixesCenter s t
    · rintro ⟨hx, _, _⟩
      refine
        ⟨?_,
          G.boundedCurvatureAtCenter_proved s,
          G.evolutionEquationAtCenter_proved s⟩
      apply (G.evolutionFlow s t).injective
      change G.evolutionFlow s t x =
        G.evolutionFlow s t (0 : R3)
      change G.evolutionFlow s t x = (0 : R3) at hx
      rw [G.evolutionFixesCenter s t]
      exact hx
  initialRegular :=
    ⟨rfl,
      G.boundedCurvatureAtCenter_proved G.initialTime,
      G.evolutionEquationAtCenter_proved G.initialTime⟩

/--
The chosen asymptotic falloff class has one marked asymptotic end.

`PUnit` records uniqueness of the end marker.  A future analytic theorem must
justify that the physical geometric end space is represented by this marker.
-/
def canonicalAsymptoticEndSystem
    {Time : Type u}
    {α : Type w}
    (G : GlobalHyperbolicR3Development Time α) :
    AsymptoticEndSystem.{u, 0} Time G.initialTime where
  End :=
    fun _ => PUnit
  endTransport :=
    fun _ _ => Equiv.refl PUnit
  initialEnd :=
    PUnit.unit
  initialEndUnique := by
    intro e
    cases e
    rfl

/-- The conclusion generated from the single certified development carrier. -/
def RestrictedNonRealizationConclusion
    {Time : Type u}
    {α : Type w}
    (G : GlobalHyperbolicR3Development Time α)
    (t : Time) : Prop :=
  let E := G.sliceEvolution
  let C := G.canonicalDecodedCoreSystem
  let Z := G.canonicalCenterSystem
  let A := G.canonicalAsymptoticEndSystem
  Nonempty ((E.Slice t).carrier ≃ₜ R3) ∧
  (∀ d,
    C.decode t (C.recordPrefix (d + 1)) ⊆
      C.decode t (C.recordPrefix d)) ∧
  (∀ d,
    Nonempty
      ({x // x ∈ C.decode t (C.recordPrefix d)} ≃ₜ ClosedBall3)) ∧
  Z.RegularAt t (Z.center t) ∧
  (∀ {x y : (E.Slice t).carrier},
    Z.IsCenter t x →
    Z.IsCenter t y →
    x = y) ∧
  ¬ A.HasEinsteinRosenTwoEndTopology t

/--
The four global packages used in PR #1165 are generated from one certified
global development carrier.
-/
theorem restrictedNonRealization_from_globalDevelopment
    {Time : Type u}
    {α : Type w}
    (G : GlobalHyperbolicR3Development Time α)
    (t : Time) :
    G.RestrictedNonRealizationConclusion t := by
  unfold RestrictedNonRealizationConclusion
  exact
    causalRecordRestrictedEinsteinRosenNonRealization
      G.sliceEvolution
      G.canonicalDecodedCoreSystem
      G.canonicalCenterSystem
      G.canonicalAsymptoticEndSystem
      t

end GlobalHyperbolicR3Development

/--
The exact remaining global existence problem for a fixed initial-data object.
-/
def EinsteinMeshSIDFHGlobalDevelopmentExists
    (Time : Type u)
    (α : Type w)
    (D : FilledConcreteInitialDataClass) : Prop :=
  ∃ G : GlobalHyperbolicR3Development Time α,
    G.initialData = D

/--
Reduction from admissible initial data to the restricted non-realization
conclusion.

The only non-constructor input is existence of the certified global
development.
-/
theorem restrictedNonRealization_reduced_to_globalDevelopmentExistence
    {Time : Type u}
    {α : Type w}
    (D : FilledConcreteInitialDataClass)
    (hD :
      EinsteinMeshSIDFHGlobalDevelopmentExists Time α D) :
    ∃ G : GlobalHyperbolicR3Development Time α,
      G.initialData = D ∧
      ∀ t : Time,
        G.RestrictedNonRealizationConclusion t := by
  rcases hD with ⟨G, hG⟩
  refine ⟨G, hG, ?_⟩
  intro t
  exact G.restrictedNonRealization_from_globalDevelopment t

/-- Machine-readable status for the reduced route. -/
def causalRecordEinsteinRosenGlobalDevelopmentReductionStatus : String :=
  "REDUCED_TO_CERTIFIED_GLOBAL_DEVELOPMENT_EXISTENCE"

/-- Exact remaining analytic boundary. -/
def causalRecordEinsteinRosenGlobalDevelopmentMissingLemma : String :=
  "EINSTEIN_MESH_SIDFH_GLOBAL_DEVELOPMENT_EXISTS_FROM_ADMISSIBLE_INITIAL_DATA"

end Chronos.Frontier
