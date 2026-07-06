import Chronos.Frontier.LocalAnisotropicTurnaroundObservationReceipt

/-
Bounded anisotropic residual classification receipt.

This file records a receipt-level classification boundary for the
Local Group anisotropic turnaround residual marker. It distinguishes
a residual-geometry signal candidate from a noise candidate by a
declared threshold, without deriving gravity, Einstein dynamics, or a
new cosmology solution.
-/

inductive LocalAnisotropicResidualClass : Type where
  | residualGeometrySignalCandidate
  | residualNoiseCandidate
  | residualUndetermined
  deriving DecidableEq, Repr

structure LocalAnisotropicResidualClassificationReceipt : Type where
  observationReceipt : LocalAnisotropicTurnaroundObservationReceipt
  residualKmS : Nat
  radialVelocityErrorKmS : Nat
  distanceErrorVelocityEquivalentKmS : Nat
  noiseFloorKmS : Nat
  geometrySignalThresholdKmS : Nat
  classification : LocalAnisotropicResidualClass
  geometrySignalCandidateRule : residualKmS > geometrySignalThresholdKmS
  noiseCandidateRule : noiseFloorKmS < geometrySignalThresholdKmS
  classificationIsOnlyPredictionInterface : Prop
  boundaryNoGravityDerivation : Prop
  boundaryNoEinsteinLimit : Prop
  boundaryNoNewCosmologySolution : Prop
  boundaryNoClassificationGravityProof : Prop

def localAnisotropicResidualClassificationReceipt :
    LocalAnisotropicResidualClassificationReceipt where
  observationReceipt := localAnisotropicTurnaroundKarachentsev2009Receipt
  residualKmS := localAnisotropicTurnaroundKarachentsev2009Receipt.peculiarVelocityDispersionKmS
  radialVelocityErrorKmS := localAnisotropicTurnaroundKarachentsev2009Receipt.radialVelocityErrorKmS
  distanceErrorVelocityEquivalentKmS :=
    localAnisotropicTurnaroundKarachentsev2009Receipt.distanceErrorVelocityEquivalentKmS
  noiseFloorKmS :=
    localAnisotropicTurnaroundKarachentsev2009Receipt.radialVelocityErrorKmS
    + localAnisotropicTurnaroundKarachentsev2009Receipt.distanceErrorVelocityEquivalentKmS
  geometrySignalThresholdKmS := 20
  classification := LocalAnisotropicResidualClass.residualGeometrySignalCandidate
  geometrySignalCandidateRule := by decide
  noiseCandidateRule := by decide
  classificationIsOnlyPredictionInterface := True
  boundaryNoGravityDerivation := True
  boundaryNoEinsteinLimit := True
  boundaryNoNewCosmologySolution := True
  boundaryNoClassificationGravityProof := True

theorem local_anisotropic_residual_classification_receipt_constants :
    localAnisotropicResidualClassificationReceipt.residualKmS = 25 ∧
    localAnisotropicResidualClassificationReceipt.noiseFloorKmS = 14 ∧
    localAnisotropicResidualClassificationReceipt.geometrySignalThresholdKmS = 20 :=
  ⟨rfl, rfl, rfl⟩

theorem local_anisotropic_residual_classification_receipt_signal_candidate :
    localAnisotropicResidualClassificationReceipt.classification =
      LocalAnisotropicResidualClass.residualGeometrySignalCandidate :=
  rfl

theorem local_anisotropic_residual_classification_receipt_boundary_only :
    localAnisotropicResidualClassificationReceipt.classificationIsOnlyPredictionInterface ∧
    localAnisotropicResidualClassificationReceipt.boundaryNoGravityDerivation ∧
    localAnisotropicResidualClassificationReceipt.boundaryNoEinsteinLimit ∧
    localAnisotropicResidualClassificationReceipt.boundaryNoNewCosmologySolution ∧
    localAnisotropicResidualClassificationReceipt.boundaryNoClassificationGravityProof :=
  ⟨True.intro, True.intro, True.intro, True.intro, True.intro⟩
