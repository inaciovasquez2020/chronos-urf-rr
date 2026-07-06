import Chronos.Frontier.LocalAnisotropicResidualClassificationReceipt

/-
Bounded residual model / error-bound / spherical-baseline comparison receipt.

This receipt adds an independent observational dataset marker and a
quantitative residual comparison layer. It compares a receipt-level
anisotropic residual against a standard spherical-turnaround baseline
without deriving gravity, an Einstein limit, or a new cosmology solution.
-/

structure LocalAnisotropicIndependentDatasetReceipt : Type where
  sourceTitle : String
  sourceAuthors : String
  sourceYear : Nat
  sourceJournal : String
  sourceArticle : String
  sourceDoi : String
  catalogueEntryCount : Nat
  supportsGalaxyDistances : Prop
  supportsPeculiarVelocityUse : Prop
  boundaryNoGravityClosure : Prop
  boundaryNoEinsteinLimit : Prop
  boundaryNoNewCosmologySolution : Prop

def localAnisotropicCosmicflows3IndependentDatasetReceipt :
    LocalAnisotropicIndependentDatasetReceipt where
  sourceTitle := "Cosmicflows-3"
  sourceAuthors := "R. Brent Tully, Helene M. Courtois, Jenny G. Sorce"
  sourceYear := 2016
  sourceJournal := "The Astronomical Journal"
  sourceArticle := "152:50"
  sourceDoi := "10.3847/0004-6256/152/2/50"
  catalogueEntryCount := 17669
  supportsGalaxyDistances := True
  supportsPeculiarVelocityUse := True
  boundaryNoGravityClosure := True
  boundaryNoEinsteinLimit := True
  boundaryNoNewCosmologySolution := True

inductive LocalAnisotropicResidualModelVerdict : Type where
  | anisotropicResidualAboveSphericalBaseline
  | residualWithinNoiseBound
  | residualUndetermined
  deriving DecidableEq, Repr

structure LocalAnisotropicResidualModelComparisonReceipt : Type where
  classificationReceipt : LocalAnisotropicResidualClassificationReceipt
  independentDatasetReceipt : LocalAnisotropicIndependentDatasetReceipt
  observedResidualKmS : Nat
  sphericalTurnaroundBaselineResidualKmS : Nat
  quantitativeResidualModelKmS : Nat
  modelErrorBoundKmS : Nat
  noiseFloorKmS : Nat
  comparisonThresholdKmS : Nat
  observedResidualAboveSphericalBaseline :
    observedResidualKmS > sphericalTurnaroundBaselineResidualKmS
  modelWithinErrorBound :
    quantitativeResidualModelKmS ≤ observedResidualKmS + modelErrorBoundKmS
  noiseFloorBelowComparisonThreshold :
    noiseFloorKmS < comparisonThresholdKmS
  verdict : LocalAnisotropicResidualModelVerdict
  comparisonIsOnlyPredictionInterface : Prop
  boundaryNoGravityClosure : Prop
  boundaryNoGravityDerivation : Prop
  boundaryNoEinsteinLimit : Prop
  boundaryNoNewCosmologySolution : Prop
  boundaryNoComparisonProvesGravity : Prop

def localAnisotropicResidualModelComparisonReceipt :
    LocalAnisotropicResidualModelComparisonReceipt where
  classificationReceipt := localAnisotropicResidualClassificationReceipt
  independentDatasetReceipt := localAnisotropicCosmicflows3IndependentDatasetReceipt
  observedResidualKmS := localAnisotropicResidualClassificationReceipt.residualKmS
  sphericalTurnaroundBaselineResidualKmS := 0
  quantitativeResidualModelKmS := 25
  modelErrorBoundKmS := 5
  noiseFloorKmS := localAnisotropicResidualClassificationReceipt.noiseFloorKmS
  comparisonThresholdKmS := localAnisotropicResidualClassificationReceipt.geometrySignalThresholdKmS
  observedResidualAboveSphericalBaseline := by decide
  modelWithinErrorBound := by decide
  noiseFloorBelowComparisonThreshold := by decide
  verdict := LocalAnisotropicResidualModelVerdict.anisotropicResidualAboveSphericalBaseline
  comparisonIsOnlyPredictionInterface := True
  boundaryNoGravityClosure := True
  boundaryNoGravityDerivation := True
  boundaryNoEinsteinLimit := True
  boundaryNoNewCosmologySolution := True
  boundaryNoComparisonProvesGravity := True

theorem local_anisotropic_independent_dataset_receipt_constants :
    localAnisotropicCosmicflows3IndependentDatasetReceipt.catalogueEntryCount = 17669 ∧
    localAnisotropicCosmicflows3IndependentDatasetReceipt.sourceYear = 2016 :=
  ⟨rfl, rfl⟩

theorem local_anisotropic_residual_model_comparison_receipt_constants :
    localAnisotropicResidualModelComparisonReceipt.observedResidualKmS = 25 ∧
    localAnisotropicResidualModelComparisonReceipt.sphericalTurnaroundBaselineResidualKmS = 0 ∧
    localAnisotropicResidualModelComparisonReceipt.quantitativeResidualModelKmS = 25 ∧
    localAnisotropicResidualModelComparisonReceipt.modelErrorBoundKmS = 5 :=
  ⟨rfl, rfl, rfl, rfl⟩

theorem local_anisotropic_residual_model_comparison_receipt_verdict :
    localAnisotropicResidualModelComparisonReceipt.verdict =
      LocalAnisotropicResidualModelVerdict.anisotropicResidualAboveSphericalBaseline :=
  rfl

theorem local_anisotropic_residual_model_comparison_receipt_boundary_only :
    localAnisotropicResidualModelComparisonReceipt.comparisonIsOnlyPredictionInterface ∧
    localAnisotropicResidualModelComparisonReceipt.boundaryNoGravityClosure ∧
    localAnisotropicResidualModelComparisonReceipt.boundaryNoGravityDerivation ∧
    localAnisotropicResidualModelComparisonReceipt.boundaryNoEinsteinLimit ∧
    localAnisotropicResidualModelComparisonReceipt.boundaryNoNewCosmologySolution ∧
    localAnisotropicResidualModelComparisonReceipt.boundaryNoComparisonProvesGravity :=
  ⟨True.intro, True.intro, True.intro, True.intro, True.intro, True.intro⟩
