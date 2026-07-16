import Chronos.Frontier.CausalRecordEinsteinRosenAnalyticDevelopmentInterface

namespace Chronos.Frontier

universe u v

/--
A scalar field on the fixed spatial chart `R3`.
-/
abbrev ReducedScalarField :=
  R3 → ℝ

/--
The ten independent components of a symmetric four-dimensional metric
perturbation, represented on the fixed spatial chart.
-/
abbrev ReducedMetricField :=
  Fin 10 → ReducedScalarField

/--
Three spatial derivatives of a scalar field.
-/
abbrev ReducedScalarSpatialGradient :=
  Fin 3 → ReducedScalarField

/--
Three spatial derivatives of each reduced metric component.
-/
abbrev ReducedMetricSpatialGradient :=
  Fin 3 → ReducedMetricField

/--
First-order reduced harmonic-gauge state vector.

The entries represent:

* ten metric components `h`;
* their time and spatial derivatives;
* the mesh scalar and its first derivatives;
* the SIDFH scalar and its first derivatives.
-/
structure ReducedHarmonicStateVector where
  metric :
    ReducedMetricField
  metricTime :
    ReducedMetricField
  metricSpace :
    ReducedMetricSpatialGradient
  mesh :
    ReducedScalarField
  meshTime :
    ReducedScalarField
  meshSpace :
    ReducedScalarSpatialGradient
  sidfh :
    ReducedScalarField
  sidfhTime :
    ReducedScalarField
  sidfhSpace :
    ReducedScalarSpatialGradient

/--
Chosen regularity for the three-dimensional quasilinear wave system.

`4 ≤ s` is the backtracked integer condition used by this formal interface.
It is strong enough to record the usual requirement that the solution possess
more than the derivatives needed for first-order coefficient control.

No Sobolev embedding theorem is claimed here.
-/
structure ReducedSobolevRegularityChoice where
  s :
    Nat
  four_le_s :
    4 ≤ s
  weightOrder :
    Nat
  weightOrder_pos :
    0 < weightOrder

/--
Residual bundle for the reduced Einstein--mesh--SIDFH system.
-/
structure ReducedHarmonicResidualBundle where
  metric :
    ReducedMetricField
  mesh :
    ReducedScalarField
  sidfh :
    ReducedScalarField
  hamiltonian :
    ReducedScalarField
  momentum :
    ReducedScalarSpatialGradient

namespace ReducedHarmonicResidualBundle

def zero :
    ReducedHarmonicResidualBundle where
  metric :=
    fun _ _ => 0
  mesh :=
    fun _ => 0
  sidfh :=
    fun _ => 0
  hamiltonian :=
    fun _ => 0
  momentum :=
    fun _ _ => 0

end ReducedHarmonicResidualBundle

/--
Typed differential-operator toolkit for the reduced harmonic system.

The principal terms are three wave operators.  The lower-order terms are split
into the quadratic reduced-Einstein source, matter stress-energy source, scalar
potential terms, and mesh/SIDFH coupling terms.

The toolkit deliberately leaves differentiation and analytic estimates as
data because those operators are not yet implemented in the repository.
-/
structure ReducedHarmonicOperatorToolkit
    (Time : Type u) where
  regularity :
    ReducedSobolevRegularityChoice
  metricWave :
    Time →
      ReducedHarmonicStateVector →
      ReducedMetricField
  meshWave :
    Time →
      ReducedHarmonicStateVector →
      ReducedScalarField
  sidfhWave :
    Time →
      ReducedHarmonicStateVector →
      ReducedScalarField
  einsteinQuadraticSource :
    Time →
      ReducedHarmonicStateVector →
      ReducedMetricField
  stressEnergySource :
    Time →
      ReducedHarmonicStateVector →
      ReducedMetricField
  meshPotentialSource :
    Time →
      ReducedHarmonicStateVector →
      ReducedScalarField
  meshSIDFHCouplingSource :
    Time →
      ReducedHarmonicStateVector →
      ReducedScalarField
  sidfhPotentialSource :
    Time →
      ReducedHarmonicStateVector →
      ReducedScalarField
  sidfhMeshCouplingSource :
    Time →
      ReducedHarmonicStateVector →
      ReducedScalarField
  hamiltonianConstraint :
    ReducedHarmonicStateVector →
      ReducedScalarField
  momentumConstraint :
    ReducedHarmonicStateVector →
      ReducedScalarSpatialGradient
  matchesInitialData :
    FilledConcreteInitialDataClass →
      ReducedHarmonicStateVector →
      Prop
  curvatureSize :
    Time →
      ReducedHarmonicStateVector →
      ℝ
  matterSize :
    Time →
      ReducedHarmonicStateVector →
      ℝ
  curvatureThreshold :
    ℝ
  matterThreshold :
    ℝ
  centerSymmetric :
    Time →
      ReducedHarmonicStateVector →
      Prop
  weightedAsymptoticFalloff :
    Time →
      ReducedHarmonicStateVector →
      Prop

namespace ReducedHarmonicOperatorToolkit

/--
Principal diagonal wave operator on the reduced state.
-/
def principalOperator
    {Time : Type u}
    (O : ReducedHarmonicOperatorToolkit Time)
    (t : Time)
    (U : ReducedHarmonicStateVector) :
    ReducedHarmonicResidualBundle where
  metric :=
    O.metricWave t U
  mesh :=
    O.meshWave t U
  sidfh :=
    O.sidfhWave t U
  hamiltonian :=
    fun _ => 0
  momentum :=
    fun _ _ => 0

/--
Combined lower-order Einstein and scalar-field sources.
-/
def lowerOrderSource
    {Time : Type u}
    (O : ReducedHarmonicOperatorToolkit Time)
    (t : Time)
    (U : ReducedHarmonicStateVector) :
    ReducedHarmonicResidualBundle where
  metric :=
    fun i x =>
      O.einsteinQuadraticSource t U i x +
      O.stressEnergySource t U i x
  mesh :=
    fun x =>
      O.meshPotentialSource t U x +
      O.meshSIDFHCouplingSource t U x
  sidfh :=
    fun x =>
      O.sidfhPotentialSource t U x +
      O.sidfhMeshCouplingSource t U x
  hamiltonian :=
    fun _ => 0
  momentum :=
    fun _ _ => 0

/--
Reduced evolution residual: principal wave operator minus lower-order source.
-/
def evolutionResidual
    {Time : Type u}
    (O : ReducedHarmonicOperatorToolkit Time)
    (t : Time)
    (U : ReducedHarmonicStateVector) :
    ReducedHarmonicResidualBundle where
  metric :=
    fun i x =>
      O.metricWave t U i x -
      O.einsteinQuadraticSource t U i x -
      O.stressEnergySource t U i x
  mesh :=
    fun x =>
      O.meshWave t U x -
      O.meshPotentialSource t U x -
      O.meshSIDFHCouplingSource t U x
  sidfh :=
    fun x =>
      O.sidfhWave t U x -
      O.sidfhPotentialSource t U x -
      O.sidfhMeshCouplingSource t U x
  hamiltonian :=
    fun _ => 0
  momentum :=
    fun _ _ => 0

def metricEquationResidual
    {Time : Type u}
    (O : ReducedHarmonicOperatorToolkit Time)
    (t : Time)
    (U : ReducedHarmonicStateVector) :
    ReducedHarmonicResidualBundle where
  metric :=
    (O.evolutionResidual t U).metric
  mesh :=
    fun _ => 0
  sidfh :=
    fun _ => 0
  hamiltonian :=
    fun _ => 0
  momentum :=
    fun _ _ => 0

def meshEquationResidual
    {Time : Type u}
    (O : ReducedHarmonicOperatorToolkit Time)
    (t : Time)
    (U : ReducedHarmonicStateVector) :
    ReducedHarmonicResidualBundle where
  metric :=
    fun _ _ => 0
  mesh :=
    (O.evolutionResidual t U).mesh
  sidfh :=
    fun _ => 0
  hamiltonian :=
    fun _ => 0
  momentum :=
    fun _ _ => 0

def sidfhEquationResidual
    {Time : Type u}
    (O : ReducedHarmonicOperatorToolkit Time)
    (t : Time)
    (U : ReducedHarmonicStateVector) :
    ReducedHarmonicResidualBundle where
  metric :=
    fun _ _ => 0
  mesh :=
    fun _ => 0
  sidfh :=
    (O.evolutionResidual t U).sidfh
  hamiltonian :=
    fun _ => 0
  momentum :=
    fun _ _ => 0

def hamiltonianResidual
    {Time : Type u}
    (O : ReducedHarmonicOperatorToolkit Time)
    (U : ReducedHarmonicStateVector) :
    ReducedHarmonicResidualBundle where
  metric :=
    fun _ _ => 0
  mesh :=
    fun _ => 0
  sidfh :=
    fun _ => 0
  hamiltonian :=
    O.hamiltonianConstraint U
  momentum :=
    fun _ _ => 0

def momentumResidual
    {Time : Type u}
    (O : ReducedHarmonicOperatorToolkit Time)
    (U : ReducedHarmonicStateVector) :
    ReducedHarmonicResidualBundle where
  metric :=
    fun _ _ => 0
  mesh :=
    fun _ => 0
  sidfh :=
    fun _ => 0
  hamiltonian :=
    fun _ => 0
  momentum :=
    O.momentumConstraint U

/--
The operator toolkit instantiates the equation signature merged in PR #1167.
-/
def toEquationSystem
    {Time : Type u}
    (O : ReducedHarmonicOperatorToolkit Time) :
    EinsteinMeshSIDFHEquationSystem Time where
  State :=
    ReducedHarmonicStateVector
  Residual :=
    ReducedHarmonicResidualBundle
  zeroResidual :=
    ReducedHarmonicResidualBundle.zero
  harmonicGaugeEinsteinResidual :=
    O.metricEquationResidual
  meshScalarResidual :=
    O.meshEquationResidual
  sidfhScalarResidual :=
    O.sidfhEquationResidual
  hamiltonianConstraintResidual :=
    O.hamiltonianResidual
  momentumConstraintResidual :=
    O.momentumResidual
  matchesInitialData :=
    O.matchesInitialData
  curvatureBounded :=
    fun t U =>
      O.curvatureSize t U ≤ O.curvatureThreshold
  matterFieldsBounded :=
    fun t U =>
      O.matterSize t U ≤ O.matterThreshold
  centerSymmetric :=
    O.centerSymmetric
  asymptoticFalloff :=
    O.weightedAsymptoticFalloff

end ReducedHarmonicOperatorToolkit

/--
Algebraic backtracking lemma for the local energy estimate.

An integrated energy inequality and a controlled accumulated source imply the
standard multiplicative local bound.
-/
theorem localEnergyEstimate_of_integratedSourceControl
    (initialEnergy accumulatedSource finalEnergy growth : ℝ)
    (hIntegrated :
      finalEnergy ≤ initialEnergy + accumulatedSource)
    (hSource :
      accumulatedSource ≤ growth * initialEnergy) :
    finalEnergy ≤ (1 + growth) * initialEnergy := by
  calc
    finalEnergy ≤ initialEnergy + accumulatedSource :=
      hIntegrated
    _ ≤ initialEnergy + growth * initialEnergy :=
      add_le_add_right hSource initialEnergy
    _ = (1 + growth) * initialEnergy := by
      ring

/--
Backtracked `H^s` energy toolkit.

This interface retains only the estimates needed to derive uniqueness,
continuation, center symmetry, and weighted falloff.  The actual Sobolev norm
and PDE energy identity remain the two concrete analytic missing objects.
-/
structure BacktrackedSobolevEnergyToolkit
    {Time : Type u}
    (E : EinsteinMeshSIDFHEquationSystem Time) where
  regularity :
    ReducedSobolevRegularityChoice
  hsEnergy :
    E.State →
      ℝ
  hsEnergy_nonneg :
    ∀ U, 0 ≤ hsEnergy U
  differenceEnergy :
    E.State →
      E.State →
      ℝ
  differenceEnergy_nonneg :
    ∀ U V, 0 ≤ differenceEnergy U V
  differenceEnergy_eq_zero_iff :
    ∀ U V, differenceEnergy U V = 0 ↔ U = V
  growthFactor :
    Time →
      ℝ
  growthFactor_nonneg :
    ∀ t, 0 ≤ growthFactor t
  localEnergyEstimate :
    ∀ S T : EinsteinMeshSIDFHLocalSolution E,
      ∀ t,
        S.IsInSlab t →
        T.IsInSlab t →
        differenceEnergy (S.trajectory t) (T.trajectory t) ≤
          growthFactor t *
            differenceEnergy
              (S.trajectory S.initialTime)
              (T.trajectory T.initialTime)
  sameInitialData_zero :
    ∀ S T : EinsteinMeshSIDFHLocalSolution E,
      S.SameInitialData T →
      differenceEnergy
        (S.trajectory S.initialTime)
        (T.trajectory T.initialTime) = 0
  continuationNorm :
    EinsteinMeshSIDFHLocalSolution E →
      Time →
      ℝ
  continuationNorm_nonneg :
    ∀ S t, 0 ≤ continuationNorm S t
  continuationBounds_control :
    ∀ S : EinsteinMeshSIDFHLocalSolution E,
      S.ContinuationBounds →
      ∃ C : ℝ,
        ∀ t,
          S.IsInSlab t →
          continuationNorm S t ≤ C
  extension_of_uniform_continuation_bound :
    ∀ S : EinsteinMeshSIDFHLocalSolution E,
      (∃ C : ℝ,
        ∀ t,
          S.IsInSlab t →
          continuationNorm S t ≤ C) →
      ∃ T : EinsteinMeshSIDFHLocalSolution E,
        S.ExtendsSolution T
  centerDefectEnergy :
    EinsteinMeshSIDFHLocalSolution E →
      Time →
      ℝ
  centerDefectEnergy_nonneg :
    ∀ S t, 0 ≤ centerDefectEnergy S t
  centerDefectEnergy_eq_zero_iff :
    ∀ S t,
      centerDefectEnergy S t = 0 ↔
        E.centerSymmetric t (S.trajectory t)
  centerDefectEstimate :
    ∀ S : EinsteinMeshSIDFHLocalSolution E,
      ∀ t,
        S.IsInSlab t →
        centerDefectEnergy S t ≤
          growthFactor t *
            centerDefectEnergy S S.initialTime
  falloffDefectEnergy :
    EinsteinMeshSIDFHLocalSolution E →
      Time →
      ℝ
  falloffDefectEnergy_nonneg :
    ∀ S t, 0 ≤ falloffDefectEnergy S t
  falloffDefectEnergy_eq_zero_iff :
    ∀ S t,
      falloffDefectEnergy S t = 0 ↔
        E.asymptoticFalloff t (S.trajectory t)
  falloffDefectEstimate :
    ∀ S : EinsteinMeshSIDFHLocalSolution E,
      ∀ t,
        S.IsInSlab t →
        falloffDefectEnergy S t ≤
          growthFactor t *
            falloffDefectEnergy S S.initialTime

namespace BacktrackedSobolevEnergyToolkit

def UniformContinuationBound
    {Time : Type u}
    {E : EinsteinMeshSIDFHEquationSystem Time}
    (P : BacktrackedSobolevEnergyToolkit E)
    (S : EinsteinMeshSIDFHLocalSolution E) : Prop :=
  ∃ C : ℝ,
    ∀ t,
      S.IsInSlab t →
      P.continuationNorm S t ≤ C

/--
The local energy estimate implies uniqueness on overlapping slabs.
-/
theorem localUniqueness_from_energy
    {Time : Type u}
    {E : EinsteinMeshSIDFHEquationSystem Time}
    (P : BacktrackedSobolevEnergyToolkit E)
    (S T : EinsteinMeshSIDFHLocalSolution E)
    (hInitial : S.SameInitialData T) :
    S.AgreeOnOverlap T := by
  intro t hS hT
  have hEstimate :=
    P.localEnergyEstimate S T t hS hT
  have hInitialZero :=
    P.sameInitialData_zero S T hInitial
  rw [hInitialZero, mul_zero] at hEstimate
  have hNonnegative :=
    P.differenceEnergy_nonneg
      (S.trajectory t)
      (T.trajectory t)
  have hZero :
      P.differenceEnergy
        (S.trajectory t)
        (T.trajectory t) = 0 :=
    le_antisymm hEstimate hNonnegative
  exact
    (P.differenceEnergy_eq_zero_iff
      (S.trajectory t)
      (T.trajectory t)).mp hZero

/--
Curvature and matter bounds control the continuation norm, and a uniformly
bounded continuation norm yields an extension.
-/
theorem continuation_from_energy_bounds
    {Time : Type u}
    {E : EinsteinMeshSIDFHEquationSystem Time}
    (P : BacktrackedSobolevEnergyToolkit E)
    (S : EinsteinMeshSIDFHLocalSolution E)
    (hBounds : S.ContinuationBounds) :
    ∃ T : EinsteinMeshSIDFHLocalSolution E,
      S.ExtendsSolution T :=
  P.extension_of_uniform_continuation_bound
    S
    (P.continuationBounds_control S hBounds)

/--
Weak blow-up alternative: failure of extension excludes every uniform
continuation-norm bound.
-/
theorem noExtension_implies_noUniformContinuationBound
    {Time : Type u}
    {E : EinsteinMeshSIDFHEquationSystem Time}
    (P : BacktrackedSobolevEnergyToolkit E)
    (S : EinsteinMeshSIDFHLocalSolution E)
    (hNoExtension :
      ¬ ∃ T : EinsteinMeshSIDFHLocalSolution E,
          S.ExtendsSolution T) :
    ¬ P.UniformContinuationBound S := by
  intro hBound
  exact
    hNoExtension
      (P.extension_of_uniform_continuation_bound S hBound)

/--
Strong real-valued blow-up alternative: if no extension exists, then the
continuation norm exceeds every proposed real bound somewhere on the slab.
-/
theorem continuationNorm_unbounded_of_noExtension
    {Time : Type u}
    {E : EinsteinMeshSIDFHEquationSystem Time}
    (P : BacktrackedSobolevEnergyToolkit E)
    (S : EinsteinMeshSIDFHLocalSolution E)
    (hNoExtension :
      ¬ ∃ T : EinsteinMeshSIDFHLocalSolution E,
          S.ExtendsSolution T) :
    ∀ C : ℝ,
      ∃ t,
        S.IsInSlab t ∧
        C < P.continuationNorm S t := by
  intro C
  by_contra hNoLargeValue
  have hBound :
      P.UniformContinuationBound S := by
    refine ⟨C, ?_⟩
    intro t ht
    apply le_of_not_gt
    intro hLarge
    exact hNoLargeValue ⟨t, ht, hLarge⟩
  exact
    (P.noExtension_implies_noUniformContinuationBound
      S
      hNoExtension) hBound

/--
Zero center-defect energy is transported by the energy estimate.
-/
theorem centerSymmetry_preserved_from_energy
    {Time : Type u}
    {E : EinsteinMeshSIDFHEquationSystem Time}
    (P : BacktrackedSobolevEnergyToolkit E)
    (S : EinsteinMeshSIDFHLocalSolution E) :
    S.PreservesCenterSymmetry := by
  intro hInitial t ht
  have hInitialZero :
      P.centerDefectEnergy S S.initialTime = 0 :=
    (P.centerDefectEnergy_eq_zero_iff
      S
      S.initialTime).mpr hInitial
  have hEstimate :=
    P.centerDefectEstimate S t ht
  rw [hInitialZero, mul_zero] at hEstimate
  have hNonnegative :=
    P.centerDefectEnergy_nonneg S t
  have hZero :
      P.centerDefectEnergy S t = 0 :=
    le_antisymm hEstimate hNonnegative
  exact
    (P.centerDefectEnergy_eq_zero_iff S t).mp hZero

/--
Zero weighted-falloff defect is transported by the energy estimate.
-/
theorem weightedAsymptoticFalloff_preserved_from_energy
    {Time : Type u}
    {E : EinsteinMeshSIDFHEquationSystem Time}
    (P : BacktrackedSobolevEnergyToolkit E)
    (S : EinsteinMeshSIDFHLocalSolution E) :
    S.PreservesAsymptoticFalloff := by
  intro hInitial t ht
  have hInitialZero :
      P.falloffDefectEnergy S S.initialTime = 0 :=
    (P.falloffDefectEnergy_eq_zero_iff
      S
      S.initialTime).mpr hInitial
  have hEstimate :=
    P.falloffDefectEstimate S t ht
  rw [hInitialZero, mul_zero] at hEstimate
  have hNonnegative :=
    P.falloffDefectEnergy_nonneg S t
  have hZero :
      P.falloffDefectEnergy S t = 0 :=
    le_antisymm hEstimate hNonnegative
  exact
    (P.falloffDefectEnergy_eq_zero_iff S t).mp hZero

/--
The backtracked energy toolkit supplies four of the six fields of the analytic
package.  Local existence and global existence remain explicit inputs.
-/
def toAnalyticTheoremPackage
    {Time : Type u}
    {E : EinsteinMeshSIDFHEquationSystem Time}
    (P : BacktrackedSobolevEnergyToolkit E)
    (localExistence :
      ∀ D : FilledConcreteInitialDataClass,
        D.isFilled →
        ∃ S : EinsteinMeshSIDFHLocalSolution E,
          S.initialData = D)
    (globalExistence :
      ∀ D : FilledConcreteInitialDataClass,
        D.isFilled →
        ∃ S : EinsteinMeshSIDFHGlobalSolution E,
          S.initialData = D) :
    EinsteinMeshSIDFHAnalyticTheoremPackage E where
  localExistence :=
    localExistence
  localUniqueness :=
    P.localUniqueness_from_energy
  continuationCriterion :=
    P.continuation_from_energy_bounds
  centerSymmetryPreservation :=
    P.centerSymmetry_preserved_from_energy
  asymptoticFalloffPreservation :=
    P.weightedAsymptoticFalloff_preserved_from_energy
  globalExistenceFromLocalContinuation :=
    globalExistence

end BacktrackedSobolevEnergyToolkit

open scoped BigOperators
open MeasureTheory

/--
A bounded spatial multi-index in three dimensions.

Each component is at most `order`, and the subtype condition imposes the
standard total-order bound `|α| ≤ order`. This gives a finite index type for
the differentiated energy sum.
-/
abbrev ReducedSpatialMultiIndex (order : Nat) :=
  { α : Fin 3 → Fin (order + 1) //
      ∑ i : Fin 3, (α i).val ≤ order }

namespace ReducedSpatialMultiIndex

/--
Canonical axis list for a spatial multi-index: all `0` derivatives first,
then all `1` derivatives, then all `2` derivatives.

No commutation theorem for mixed derivatives is asserted here.
-/
def axisList
    {order : Nat}
    (α : ReducedSpatialMultiIndex order) :
    List (Fin 3) :=
  (List.finRange 3).flatMap fun i =>
    List.replicate (α.1 i).val i

end ReducedSpatialMultiIndex

/--
The concrete coordinate derivative in the `i`-th Euclidean spatial direction.

`fderiv` is total in Lean; later analytic work must supply the differentiability
and integrability hypotheses needed to identify these values with Sobolev weak
derivatives for the solution class.
-/
noncomputable def reducedSpatialPartialDerivative
    (i : Fin 3)
    (f : ReducedScalarField) :
    ReducedScalarField :=
  fun x =>
    (fderiv ℝ f x) ((EuclideanSpace.basisFun (Fin 3) ℝ) i)

/--
Iterated coordinate differentiation along a fixed finite axis list.
-/
noncomputable def reducedSpatialDerivativeAlong :
    List (Fin 3) → ReducedScalarField → ReducedScalarField
  | [], f =>
      f
  | i :: is, f =>
      reducedSpatialDerivativeAlong is
        (reducedSpatialPartialDerivative i f)

/--
Concrete spatial derivative `D^α f`, using the canonical axis order attached
to `α`.
-/
noncomputable def reducedSpatialMultiDerivative
    {order : Nat}
    (α : ReducedSpatialMultiIndex order)
    (f : ReducedScalarField) :
    ReducedScalarField :=
  reducedSpatialDerivativeAlong
    (ReducedSpatialMultiIndex.axisList α)
    f

/--
Pointwise differentiated first-order energy density for one scalar wave field.

For every `|α| ≤ order`, it contains the squares of `D^α field`,
`D^α fieldTime`, and all three components of `D^α fieldSpace`.
-/
noncomputable def reducedScalarFirstOrderHsDensity
    (order : Nat)
    (field fieldTime : ReducedScalarField)
    (fieldSpace : ReducedScalarSpatialGradient)
    (x : R3) :
    ℝ :=
  ∑ α : ReducedSpatialMultiIndex order, (
    (reducedSpatialMultiDerivative α field x) ^ 2 +
    (reducedSpatialMultiDerivative α fieldTime x) ^ 2 +
    (∑ j : Fin 3,
      (reducedSpatialMultiDerivative α (fieldSpace j) x) ^ 2))

/--
Concrete pointwise `H^s` energy density for the complete reduced harmonic
state.

The first-order variables are differentiated through order `s - 1`. Thus the
spatial-gradient entries control the primary metric, mesh, and SIDFH fields
through spatial order `s`, while the time-derivative entries are controlled
through order `s - 1`.
-/
noncomputable def concreteReducedHsEnergyDensity
    (R : ReducedSobolevRegularityChoice)
    (U : ReducedHarmonicStateVector)
    (x : R3) :
    ℝ :=
  (∑ a : Fin 10,
    reducedScalarFirstOrderHsDensity
      (R.s - 1)
      (U.metric a)
      (U.metricTime a)
      (fun j => U.metricSpace j a)
      x) +
  reducedScalarFirstOrderHsDensity
    (R.s - 1)
    U.mesh
    U.meshTime
    U.meshSpace
    x +
  reducedScalarFirstOrderHsDensity
    (R.s - 1)
    U.sidfh
    U.sidfhTime
    U.sidfhSpace
    x

/--
Finiteness condition for the concrete differentiated energy density.
-/
def HasFiniteConcreteReducedHsEnergy
    (R : ReducedSobolevRegularityChoice)
    (U : ReducedHarmonicStateVector) :
    Prop :=
  Integrable (concreteReducedHsEnergyDensity R U)

/--
Concrete spatial multi-index differentiated `H^s` energy of the reduced state,
integrated over the fixed Euclidean `R3` slice with volume measure.
-/
noncomputable def concreteReducedHsEnergy
    (R : ReducedSobolevRegularityChoice)
    (U : ReducedHarmonicStateVector) :
    ℝ :=
  (1 / 2 : ℝ) *
    ∫ x : R3, concreteReducedHsEnergyDensity R U x

/--
The coordinate spatial Laplacian on the fixed Euclidean `R3` chart.
-/
noncomputable def reducedSpatialLaplacian
    (field : ReducedScalarField) :
    ReducedScalarField :=
  fun x =>
    ∑ j : Fin 3,
      reducedSpatialPartialDerivative j
        (reducedSpatialPartialDerivative j field) x

/--
The differentiated acceleration-work density
`D^α fieldTime * D^α fieldAcceleration`.
-/
noncomputable def scalarDifferentiatedAccelerationWorkDensity
    {order : Nat}
    (α : ReducedSpatialMultiIndex order)
    (fieldTime fieldAcceleration : ReducedScalarField) :
    ReducedScalarField :=
  fun x =>
    reducedSpatialMultiDerivative α fieldTime x *
      reducedSpatialMultiDerivative α fieldAcceleration x

/--
The differentiated Laplacian-work density
`D^α fieldTime * Δ(D^α field)`.
-/
noncomputable def scalarDifferentiatedLaplacianWorkDensity
    {order : Nat}
    (α : ReducedSpatialMultiIndex order)
    (field fieldTime : ReducedScalarField) :
    ReducedScalarField :=
  fun x =>
    reducedSpatialMultiDerivative α fieldTime x *
      reducedSpatialLaplacian
        (reducedSpatialMultiDerivative α field) x

/--
The spatial-gradient contribution to the differentiated energy rate:
`Σ_j ∂_j(D^α fieldTime) * ∂_j(D^α field)`.
-/
noncomputable def scalarDifferentiatedGradientRateDensity
    {order : Nat}
    (α : ReducedSpatialMultiIndex order)
    (field fieldTime : ReducedScalarField) :
    ReducedScalarField :=
  fun x =>
    ∑ j : Fin 3,
      reducedSpatialPartialDerivative j
          (reducedSpatialMultiDerivative α fieldTime) x *
        reducedSpatialPartialDerivative j
          (reducedSpatialMultiDerivative α field) x

/--
The Green-flux density whose vanishing integral supplies the spatial
integration-by-parts boundary condition.
-/
noncomputable def scalarDifferentiatedGreenFluxDensity
    {order : Nat}
    (α : ReducedSpatialMultiIndex order)
    (field fieldTime : ReducedScalarField) :
    ReducedScalarField :=
  fun x =>
    scalarDifferentiatedLaplacianWorkDensity
        α field fieldTime x +
      scalarDifferentiatedGradientRateDensity
        α field fieldTime x

/--
Exact analytic hypotheses needed for one differentiated scalar spatial
integration-by-parts step.

The boundary-flux cancellation is explicit. It is not derived here from
compact support, weighted falloff, or a divergence theorem.
-/
structure ScalarDifferentiatedPrincipalWaveIBPData
    {order : Nat}
    (α : ReducedSpatialMultiIndex order)
    (field fieldTime : ReducedScalarField) :
    Prop where
  laplacianWork_integrable :
    Integrable
      (scalarDifferentiatedLaplacianWorkDensity
        α field fieldTime)
  gradientRate_integrable :
    Integrable
      (scalarDifferentiatedGradientRateDensity
        α field fieldTime)
  boundaryFluxIntegral_zero :
    (∫ x : R3,
      scalarDifferentiatedGreenFluxDensity
        α field fieldTime x) = 0

/--
Scalar spatial integration by parts for one differentiated reduced field:
`∫ D^α fieldTime · Δ(D^α field)
 = -∫ ∇D^α fieldTime · ∇D^α field`.
-/
theorem scalarDifferentiatedSpatialIntegrationByParts
    {order : Nat}
    (α : ReducedSpatialMultiIndex order)
    (field fieldTime : ReducedScalarField)
    (H :
      ScalarDifferentiatedPrincipalWaveIBPData
        α field fieldTime) :
    (∫ x : R3,
      scalarDifferentiatedLaplacianWorkDensity
        α field fieldTime x) =
      -(∫ x : R3,
        scalarDifferentiatedGradientRateDensity
          α field fieldTime x) := by
  have hsum :
      (∫ x : R3,
        scalarDifferentiatedLaplacianWorkDensity
          α field fieldTime x) +
        (∫ x : R3,
          scalarDifferentiatedGradientRateDensity
            α field fieldTime x) = 0 := by
    rw [← integral_add
      H.laplacianWork_integrable
      H.gradientRate_integrable]
    simpa [scalarDifferentiatedGreenFluxDensity] using
      H.boundaryFluxIntegral_zero
  linarith

/--
Integrated work of the differentiated scalar principal wave operator
`D^α fieldAcceleration - Δ(D^α field)`.
-/
noncomputable def scalarDifferentiatedPrincipalWaveWork
    {order : Nat}
    (α : ReducedSpatialMultiIndex order)
    (field fieldTime fieldAcceleration : ReducedScalarField) :
    ℝ :=
  (∫ x : R3,
    scalarDifferentiatedAccelerationWorkDensity
      α fieldTime fieldAcceleration x) -
    (∫ x : R3,
      scalarDifferentiatedLaplacianWorkDensity
        α field fieldTime x)

/--
The corresponding differentiated scalar energy-rate pairing.
-/
noncomputable def scalarDifferentiatedEnergyRatePairing
    {order : Nat}
    (α : ReducedSpatialMultiIndex order)
    (field fieldTime fieldAcceleration : ReducedScalarField) :
    ℝ :=
  (∫ x : R3,
    scalarDifferentiatedAccelerationWorkDensity
      α fieldTime fieldAcceleration x) +
    (∫ x : R3,
      scalarDifferentiatedGradientRateDensity
        α field fieldTime x)

/--
Principal-wave integration-by-parts identity for one spatially differentiated
reduced scalar field.
-/
theorem scalarPrincipalWaveIntegrationByPartsIdentity
    {order : Nat}
    (α : ReducedSpatialMultiIndex order)
    (field fieldTime fieldAcceleration : ReducedScalarField)
    (H :
      ScalarDifferentiatedPrincipalWaveIBPData
        α field fieldTime) :
    scalarDifferentiatedPrincipalWaveWork
        α field fieldTime fieldAcceleration =
      scalarDifferentiatedEnergyRatePairing
        α field fieldTime fieldAcceleration := by
  unfold scalarDifferentiatedPrincipalWaveWork
  unfold scalarDifferentiatedEnergyRatePairing
  rw [scalarDifferentiatedSpatialIntegrationByParts
    α field fieldTime H]
  ring

/--
A spatial vector field on the fixed Euclidean `R3` chart.
-/
abbrev ReducedSpatialVectorField := R3 → R3

/--
Coordinate divergence of a spatial vector field.
-/
noncomputable def reducedSpatialDivergence
    (flux : ReducedSpatialVectorField) :
    ReducedScalarField :=
  fun x =>
    ∑ j : Fin 3,
      reducedSpatialPartialDerivative j
        (fun y => flux y j) x

/--
The Green flux vector
`D^α fieldTime * ∇(D^α field)`.
-/
noncomputable def scalarDifferentiatedGreenFluxVector
    {order : Nat}
    (α : ReducedSpatialMultiIndex order)
    (field fieldTime : ReducedScalarField) :
    ReducedSpatialVectorField :=
  fun x =>
    WithLp.toLp 2 fun j =>
      reducedSpatialMultiDerivative α fieldTime x *
        reducedSpatialPartialDerivative j
          (reducedSpatialMultiDerivative α field) x

/--
The generic compact-support divergence theorem needed on the fixed `R3`
chart.

This is deliberately isolated as one global analytic missing lemma rather
than assumed separately for every reduced field.
-/
def CompactSupportDivergenceIntegralProperty : Prop :=
  ∀ flux : ReducedSpatialVectorField,
    HasCompactSupport flux →
    Integrable (reducedSpatialDivergence flux) →
    (∫ x : R3, reducedSpatialDivergence flux x) = 0

/--
Coordinate product rule for the concrete spatial derivative.
-/
theorem reducedSpatialPartialDerivative_mul
    (j : Fin 3)
    (f g : ReducedScalarField)
    (x : R3)
    (hf : DifferentiableAt ℝ f x)
    (hg : DifferentiableAt ℝ g x) :
    reducedSpatialPartialDerivative j
        (fun y => f y * g y) x =
      f x * reducedSpatialPartialDerivative j g x +
        g x * reducedSpatialPartialDerivative j f x := by
  unfold reducedSpatialPartialDerivative
  have h :=
    congrArg
      (fun L : R3 →L[ℝ] ℝ =>
        L ((EuclideanSpace.basisFun (Fin 3) ℝ) j))
      (fderiv_fun_mul hf hg)
  simpa using h

/--
The divergence of the differentiated Green vector equals the existing
Laplacian-work plus gradient-rate density.
-/
theorem scalarDifferentiatedGreenFlux_factorization
    {order : Nat}
    (α : ReducedSpatialMultiIndex order)
    (field fieldTime : ReducedScalarField)
    (hTime :
      ∀ x,
        DifferentiableAt ℝ
          (reducedSpatialMultiDerivative α fieldTime) x)
    (hSpace :
      ∀ j x,
        DifferentiableAt ℝ
          (reducedSpatialPartialDerivative j
            (reducedSpatialMultiDerivative α field)) x) :
    scalarDifferentiatedGreenFluxDensity
        α field fieldTime =
      reducedSpatialDivergence
        (scalarDifferentiatedGreenFluxVector
          α field fieldTime) := by
  funext x
  symm
  change
    (∑ j : Fin 3,
      reducedSpatialPartialDerivative j
        (fun y =>
          reducedSpatialMultiDerivative α fieldTime y *
            reducedSpatialPartialDerivative j
              (reducedSpatialMultiDerivative α field) y)
        x) =
      reducedSpatialMultiDerivative α fieldTime x *
          (∑ j : Fin 3,
            reducedSpatialPartialDerivative j
              (reducedSpatialPartialDerivative j
                (reducedSpatialMultiDerivative α field))
              x) +
        ∑ j : Fin 3,
          reducedSpatialPartialDerivative j
              (reducedSpatialMultiDerivative α fieldTime)
              x *
            reducedSpatialPartialDerivative j
              (reducedSpatialMultiDerivative α field)
              x
  calc
    (∑ j : Fin 3,
      reducedSpatialPartialDerivative j
        (fun y =>
          reducedSpatialMultiDerivative α fieldTime y *
            reducedSpatialPartialDerivative j
              (reducedSpatialMultiDerivative α field) y)
        x) =
        ∑ j : Fin 3,
          (reducedSpatialMultiDerivative α fieldTime x *
              reducedSpatialPartialDerivative j
                (reducedSpatialPartialDerivative j
                  (reducedSpatialMultiDerivative α field))
                x +
            reducedSpatialPartialDerivative j
                (reducedSpatialMultiDerivative α field)
                x *
              reducedSpatialPartialDerivative j
                (reducedSpatialMultiDerivative α fieldTime)
                x) := by
      apply Finset.sum_congr rfl
      intro j _
      exact reducedSpatialPartialDerivative_mul
        j
        (reducedSpatialMultiDerivative α fieldTime)
        (reducedSpatialPartialDerivative j
          (reducedSpatialMultiDerivative α field))
        x
        (hTime x)
        (hSpace j x)
    _ =
      reducedSpatialMultiDerivative α fieldTime x *
          (∑ j : Fin 3,
            reducedSpatialPartialDerivative j
              (reducedSpatialPartialDerivative j
                (reducedSpatialMultiDerivative α field))
              x) +
        ∑ j : Fin 3,
          reducedSpatialPartialDerivative j
              (reducedSpatialMultiDerivative α fieldTime)
              x *
            reducedSpatialPartialDerivative j
              (reducedSpatialMultiDerivative α field)
              x := by
      rw [Finset.sum_add_distrib, Finset.mul_sum]
      congr 1
      apply Finset.sum_congr rfl
      intro j _
      ring

/--
Concrete compact-support data reducing the differentiated Green-flux
cancellation to the generic compact-support divergence theorem.

The factorization field records the still-required coordinate product-rule
calculation identifying the existing Green density with the divergence of
`D^α fieldTime * ∇(D^α field)`.
-/
structure ScalarDifferentiatedCompactSupportFluxData
    {order : Nat}
    (α : ReducedSpatialMultiIndex order)
    (field fieldTime : ReducedScalarField) :
    Prop where
  laplacianWork_integrable :
    Integrable
      (scalarDifferentiatedLaplacianWorkDensity
        α field fieldTime)
  gradientRate_integrable :
    Integrable
      (scalarDifferentiatedGradientRateDensity
        α field fieldTime)
  divergence_integrable :
    Integrable
      (reducedSpatialDivergence
        (scalarDifferentiatedGreenFluxVector
          α field fieldTime))
  flux_compactSupport :
    HasCompactSupport
      (scalarDifferentiatedGreenFluxVector
        α field fieldTime)
  fieldTime_differentiable :
    ∀ x,
      DifferentiableAt ℝ
        (reducedSpatialMultiDerivative α fieldTime) x
  fieldSpace_differentiable :
    ∀ j x,
      DifferentiableAt ℝ
        (reducedSpatialPartialDerivative j
          (reducedSpatialMultiDerivative α field)) x

/--
Compact support forces the integrated differentiated Green flux to vanish,
provided the generic compact-support divergence theorem holds.
-/
theorem scalarDifferentiatedBoundaryFluxIntegral_zero_of_compactSupport
    {order : Nat}
    (α : ReducedSpatialMultiIndex order)
    (field fieldTime : ReducedScalarField)
    (hDivergence :
      CompactSupportDivergenceIntegralProperty)
    (H :
      ScalarDifferentiatedCompactSupportFluxData
        α field fieldTime) :
    (∫ x : R3,
      scalarDifferentiatedGreenFluxDensity
        α field fieldTime x) = 0 := by
  rw [scalarDifferentiatedGreenFlux_factorization
    α field fieldTime
    H.fieldTime_differentiable
    H.fieldSpace_differentiable]
  exact hDivergence
    (scalarDifferentiatedGreenFluxVector
      α field fieldTime)
    H.flux_compactSupport
    H.divergence_integrable

/--
The compact-support reduction supplies the previously required scalar
principal-wave integration-by-parts data.
-/
theorem scalarDifferentiatedPrincipalWaveIBPData_of_compactSupport
    {order : Nat}
    (α : ReducedSpatialMultiIndex order)
    (field fieldTime : ReducedScalarField)
    (hDivergence :
      CompactSupportDivergenceIntegralProperty)
    (H :
      ScalarDifferentiatedCompactSupportFluxData
        α field fieldTime) :
    ScalarDifferentiatedPrincipalWaveIBPData
      α field fieldTime where
  laplacianWork_integrable :=
    H.laplacianWork_integrable
  gradientRate_integrable :=
    H.gradientRate_integrable
  boundaryFluxIntegral_zero :=
    scalarDifferentiatedBoundaryFluxIntegral_zero_of_compactSupport
      α field fieldTime hDivergence H

def causalRecordEinsteinRosenCompactGreenFluxStatus : String :=
  "GREEN_FLUX_PRODUCT_RULE_PROVED_AND_REDUCED_TO_COMPACT_DIVERGENCE"

def causalRecordEinsteinRosenCompactGreenFluxMissingObject : String :=
  "COMPACT_SUPPORT_DIVERGENCE_INTEGRAL_THEOREM"

def causalRecordEinsteinRosenScalarPrincipalWaveIBPStatus : String :=
  "SCALAR_PRINCIPAL_WAVE_IBP_FROM_VANISHING_GREEN_FLUX"

/--
Machine-readable boundary left after the scalar identity.
-/
def causalRecordEinsteinRosenScalarPrincipalWaveIBPMissingObject : String :=
  "COMPACT_SUPPORT_DIVERGENCE_INTEGRAL_THEOREM"

/--
Machine-readable status for the concrete energy layer.
-/
def causalRecordEinsteinRosenConcreteHsEnergyStatus : String :=
  "CONCRETE_SPATIAL_MULTI_INDEX_HS_ENERGY_DEFINED"

/--
The next analytic boundary after defining the energy itself.
-/
def causalRecordEinsteinRosenConcreteHsEnergyMissingObject : String :=
  "PDE_ENERGY_IDENTITY_AND_SOURCE_TERM_BOUNDS"

def causalRecordEinsteinRosenSobolevBacktrackStatus : String :=
  "BACKTRACKED_TO_HS_ENERGY_TOOLKIT_WITH_S_GE_4"

def causalRecordEinsteinRosenSobolevBacktrackProved : String :=
  "ENERGY_SCHEMA_UNIQUENESS_BLOWUP_ALTERNATIVE_CENTER_AND_FALLOFF_TRANSPORT"

def causalRecordEinsteinRosenSobolevBacktrackMissingObjects : String :=
  "PDE_ENERGY_IDENTITY_SOURCE_BOUNDS_LOCAL_AND_GLOBAL_EXISTENCE"

end Chronos.Frontier
