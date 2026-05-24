import Mathlib.Tactic

namespace Chronos
namespace Frontier

/--
R1 substeps for the Long-Chord Exclusion Lemma.

This file does not prove R1 mathematically.
It records the exact substep interface needed before R1 may be promoted.
-/
structure LongChordExclusionSubsteps where
  R1a_trivialFacesAvoidLongChords : Prop
  R1b_linearCombinationsCannotCreateLongChords : Prop
  R1c_maximalSeparationForbidsTrivialLongChord : Prop

/-- R1 is closed exactly when R1a, R1b, and R1c have all been supplied. -/
def LongChordExclusionClosed (S : LongChordExclusionSubsteps) : Prop :=
  S.R1a_trivialFacesAvoidLongChords ∧
  S.R1b_linearCombinationsCannotCreateLongChords ∧
  S.R1c_maximalSeparationForbidsTrivialLongChord

theorem LongChordExclusion_from_R1a_R1b_R1c
    (S : LongChordExclusionSubsteps)
    (h1a : S.R1a_trivialFacesAvoidLongChords)
    (h1b : S.R1b_linearCombinationsCannotCreateLongChords)
    (h1c : S.R1c_maximalSeparationForbidsTrivialLongChord) :
    LongChordExclusionClosed S := by
  exact ⟨h1a, h1b, h1c⟩

/--
R2 substeps for the Diameter-Separation Filling Obstruction.

This file does not prove R2 mathematically.
It records the exact substep interface needed before R2 may be promoted.
-/
structure DiameterSeparationFillingObstructionSubsteps where
  R2a_boundedFillingLocalizesToRootedRegion : Prop
  R2b_distinctFiberSupportsCannotBeJoinedByBoundedTwoChain : Prop
  R2c_boundedFillingForcesForbiddenTwistedClassIdentification : Prop
  R2d_geometricSeparationImpliesAlgebraicInjectivity : Prop

/-- R2 is closed exactly when R2a, R2b, R2c, and R2d have all been supplied. -/
def DiameterSeparationFillingObstructionClosed
    (S : DiameterSeparationFillingObstructionSubsteps) : Prop :=
  S.R2a_boundedFillingLocalizesToRootedRegion ∧
  S.R2b_distinctFiberSupportsCannotBeJoinedByBoundedTwoChain ∧
  S.R2c_boundedFillingForcesForbiddenTwistedClassIdentification ∧
  S.R2d_geometricSeparationImpliesAlgebraicInjectivity

theorem DiameterSeparationFillingObstruction_from_R2a_R2b_R2c_R2d
    (S : DiameterSeparationFillingObstructionSubsteps)
    (h2a : S.R2a_boundedFillingLocalizesToRootedRegion)
    (h2b : S.R2b_distinctFiberSupportsCannotBeJoinedByBoundedTwoChain)
    (h2c : S.R2c_boundedFillingForcesForbiddenTwistedClassIdentification)
    (h2d : S.R2d_geometricSeparationImpliesAlgebraicInjectivity) :
    DiameterSeparationFillingObstructionClosed S := by
  exact ⟨h2a, h2b, h2c, h2d⟩

/--
R3 substeps for the Uniform Local-Type Capacity Lemma.

This file does not prove R3 mathematically.
It records the exact substep interface needed before R3 may be promoted.
-/
structure UniformLocalTypeCapacitySubsteps where
  R3a_boundedLocalTypeFactorizationFiniteStateSpace : Prop
  R3b_finiteStateFactorizationBoundsImageDimension : Prop
  R3c_equalLocalTypeDataGivesEqualQuotientData : Prop
  R3d_uniformDimensionBoundExtracted : Prop

/-- R3 is closed exactly when R3a, R3b, R3c, and R3d have all been supplied. -/
def UniformLocalTypeCapacityClosed
    (S : UniformLocalTypeCapacitySubsteps) : Prop :=
  S.R3a_boundedLocalTypeFactorizationFiniteStateSpace ∧
  S.R3b_finiteStateFactorizationBoundsImageDimension ∧
  S.R3c_equalLocalTypeDataGivesEqualQuotientData ∧
  S.R3d_uniformDimensionBoundExtracted

theorem UniformLocalTypeCapacity_from_R3a_R3b_R3c_R3d
    (S : UniformLocalTypeCapacitySubsteps)
    (h3a : S.R3a_boundedLocalTypeFactorizationFiniteStateSpace)
    (h3b : S.R3b_finiteStateFactorizationBoundsImageDimension)
    (h3c : S.R3c_equalLocalTypeDataGivesEqualQuotientData)
    (h3d : S.R3d_uniformDimensionBoundExtracted) :
    UniformLocalTypeCapacityClosed S := by
  exact ⟨h3a, h3b, h3c, h3d⟩

/--
Conditional assembly package for the non-factorisation target.

The fields require closed R1, R2, and R3 packages.
This is a conditional dependency-chain surface, not an unconditional proof of R1, R2, R3, or non-factorisation.
-/
structure R1R2R3NonFactorisationInputs where
  r1Substeps : LongChordExclusionSubsteps
  r2Substeps : DiameterSeparationFillingObstructionSubsteps
  r3Substeps : UniformLocalTypeCapacitySubsteps
  r1Closed : LongChordExclusionClosed r1Substeps
  r2Closed : DiameterSeparationFillingObstructionClosed r2Substeps
  r3Closed : UniformLocalTypeCapacityClosed r3Substeps

/--
The dependency-chain target is available only from supplied R1/R2/R3 closures.
-/
def NonFactorisationDependencyChainClosed
    (I : R1R2R3NonFactorisationInputs) : Prop :=
  LongChordExclusionClosed I.r1Substeps ∧
  DiameterSeparationFillingObstructionClosed I.r2Substeps ∧
  UniformLocalTypeCapacityClosed I.r3Substeps

theorem R1_R2_R3_TO_NON_FACTORISATION
    (I : R1R2R3NonFactorisationInputs) :
    NonFactorisationDependencyChainClosed I := by
  exact ⟨I.r1Closed, I.r2Closed, I.r3Closed⟩

/--
No-promotion lock.

Chronos-RR and H4.1/FGL promotion are blocked unless theorem-level R1, R2, and R3
closures are supplied.
-/
structure R1R2R3TheoremInputs where
  R1_theorem_proved : Prop
  R2_theorem_proved : Prop
  R3_theorem_proved : Prop

def NonFactorisationPromotionAllowed (P : R1R2R3TheoremInputs) : Prop :=
  P.R1_theorem_proved ∧ P.R2_theorem_proved ∧ P.R3_theorem_proved

def ChronosRRPromotionAllowed (P : R1R2R3TheoremInputs) : Prop :=
  NonFactorisationPromotionAllowed P

def H41FGLPromotionAllowed (P : R1R2R3TheoremInputs) : Prop :=
  NonFactorisationPromotionAllowed P

theorem no_nonfactorisation_promotion_without_R1_R2_R3
    (P : R1R2R3TheoremInputs)
    (hmissing :
      ¬ P.R1_theorem_proved ∨
      ¬ P.R2_theorem_proved ∨
      ¬ P.R3_theorem_proved) :
    ¬ NonFactorisationPromotionAllowed P := by
  intro hallowed
  rcases hmissing with hR1 | hR2 | hR3
  · exact hR1 hallowed.1
  · exact hR2 hallowed.2.1
  · exact hR3 hallowed.2.2

theorem no_chronos_rr_promotion_without_R1
    (P : R1R2R3TheoremInputs)
    (hR1 : ¬ P.R1_theorem_proved) :
    ¬ ChronosRRPromotionAllowed P := by
  intro hallowed
  exact hR1 hallowed.1

theorem no_chronos_rr_promotion_without_R2
    (P : R1R2R3TheoremInputs)
    (hR2 : ¬ P.R2_theorem_proved) :
    ¬ ChronosRRPromotionAllowed P := by
  intro hallowed
  exact hR2 hallowed.2.1

theorem no_chronos_rr_promotion_without_R3
    (P : R1R2R3TheoremInputs)
    (hR3 : ¬ P.R3_theorem_proved) :
    ¬ ChronosRRPromotionAllowed P := by
  intro hallowed
  exact hR3 hallowed.2.2

theorem no_h41_fgl_promotion_without_R1
    (P : R1R2R3TheoremInputs)
    (hR1 : ¬ P.R1_theorem_proved) :
    ¬ H41FGLPromotionAllowed P := by
  intro hallowed
  exact hR1 hallowed.1

theorem no_h41_fgl_promotion_without_R2
    (P : R1R2R3TheoremInputs)
    (hR2 : ¬ P.R2_theorem_proved) :
    ¬ H41FGLPromotionAllowed P := by
  intro hallowed
  exact hR2 hallowed.2.1

theorem no_h41_fgl_promotion_without_R3
    (P : R1R2R3TheoremInputs)
    (hR3 : ¬ P.R3_theorem_proved) :
    ¬ H41FGLPromotionAllowed P := by
  intro hallowed
  exact hR3 hallowed.2.2

end Frontier
end Chronos
