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

def causalRecordEinsteinRosenSobolevBacktrackStatus : String :=
  "BACKTRACKED_TO_HS_ENERGY_TOOLKIT_WITH_S_GE_4"

def causalRecordEinsteinRosenSobolevBacktrackProved : String :=
  "ENERGY_SCHEMA_UNIQUENESS_BLOWUP_ALTERNATIVE_CENTER_AND_FALLOFF_TRANSPORT"

def causalRecordEinsteinRosenSobolevBacktrackMissingObjects : String :=
  "CONCRETE_SOBOLEV_NORM_AND_PDE_ENERGY_IDENTITY_PLUS_LOCAL_AND_GLOBAL_EXISTENCE"

end Chronos.Frontier
