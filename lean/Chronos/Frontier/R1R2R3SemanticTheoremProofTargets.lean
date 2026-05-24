import Mathlib.Tactic
import Chronos.Frontier.R1R2R3NonFactorisationPromotionLock

namespace Chronos
namespace Frontier

universe u

/--
Semantic data needed before R1 can be a theorem rather than a Prop-field interface.
-/
structure R1SemanticData where
  Word : Type u
  Edge : Type u
  Face : Type u
  e1 : Edge
  e2 : Edge
  TrivWord : Word → Prop
  TrivFace : Face → Prop
  WordSupport : Word → Edge → Prop
  FaceBoundarySupport : Face → Edge → Prop

/-- The theorem-level Long-Chord Exclusion target. -/
def R1LongChordExclusionTheorem (D : R1SemanticData) : Prop :=
  ∀ word, D.TrivWord word →
    ¬ D.WordSupport word D.e1 ∧
    ¬ D.WordSupport word D.e2

/--
Semantic theorem-proof inputs for R1.

These are still inputs. This structure does not prove the underlying geometry.
-/
structure R1TheoremProofInputs (D : R1SemanticData) where
  R1a_trivialFaceBoundariesAvoidLongChords :
    ∀ face, D.TrivFace face →
      ¬ D.FaceBoundarySupport face D.e1 ∧
      ¬ D.FaceBoundarySupport face D.e2
  R1b_trivialWordSupportComesFromTrivialFaces :
    ∀ word edge, D.TrivWord word → D.WordSupport word edge →
      ∃ face, D.TrivFace face ∧ D.FaceBoundarySupport face edge
  R1c_maximalSeparationForbidsTrivialLongChord : Prop
  R1c_supplied : R1c_maximalSeparationForbidsTrivialLongChord

/-- R1 theorem route from explicit semantic inputs. -/
theorem R1_LongChordExclusion_from_semantic_inputs
    (D : R1SemanticData)
    (H : R1TheoremProofInputs D) :
    R1LongChordExclusionTheorem D := by
  intro word hword
  constructor
  · intro hsupport
    rcases H.R1b_trivialWordSupportComesFromTrivialFaces
      word D.e1 hword hsupport with ⟨face, hface, hboundary⟩
    exact (H.R1a_trivialFaceBoundariesAvoidLongChords face hface).1 hboundary
  · intro hsupport
    rcases H.R1b_trivialWordSupportComesFromTrivialFaces
      word D.e2 hword hsupport with ⟨face, hface, hboundary⟩
    exact (H.R1a_trivialFaceBoundariesAvoidLongChords face hface).2 hboundary

/--
Semantic data needed before R2 can be a theorem rather than a Prop-field interface.
-/
structure R2SemanticData where
  Fiber : Type u
  TwoChain : Type u
  L : Nat
  diameter : TwoChain → Nat
  BoundaryBetween : TwoChain → Fiber → Fiber → Prop

/-- The theorem-level Diameter-Separation Filling Obstruction target. -/
def R2DiameterSeparationFillingObstructionTheorem (D : R2SemanticData) : Prop :=
  ∀ chain u v,
    u ≠ v →
    D.BoundaryBetween chain u v →
    D.L < D.diameter chain

/--
Semantic theorem-proof inputs for R2.

These are still inputs. This structure does not prove the underlying filling obstruction.
-/
structure R2TheoremProofInputs (D : R2SemanticData) where
  R2a_boundedFillingLocalizesToRootedRegion : Prop
  R2a_supplied : R2a_boundedFillingLocalizesToRootedRegion
  R2b_distinctFibersNoBoundedJoining :
    ∀ chain u v,
      u ≠ v →
      D.BoundaryBetween chain u v →
      ¬ D.diameter chain ≤ D.L
  R2c_boundedFillingForcesForbiddenTwistedClassIdentification : Prop
  R2c_supplied : R2c_boundedFillingForcesForbiddenTwistedClassIdentification
  R2d_geometricSeparationImpliesAlgebraicInjectivity : Prop
  R2d_supplied : R2d_geometricSeparationImpliesAlgebraicInjectivity

/-- R2 theorem route from explicit semantic inputs. -/
theorem R2_DiameterSeparationFillingObstruction_from_semantic_inputs
    (D : R2SemanticData)
    (H : R2TheoremProofInputs D) :
    R2DiameterSeparationFillingObstructionTheorem D := by
  intro chain u v huv hboundary
  have hnot : ¬ D.diameter chain ≤ D.L :=
    H.R2b_distinctFibersNoBoundedJoining chain u v huv hboundary
  exact Nat.lt_of_not_ge hnot

/--
Semantic data needed before R3 can be a theorem rather than a Prop-field interface.
-/
structure R3SemanticData where
  QuotientData : Type u
  C : Nat
  dim : QuotientData → Nat
  FactorsThroughBoundedLocalType : QuotientData → Prop

/-- The theorem-level Uniform Local-Type Capacity target. -/
def R3UniformLocalTypeCapacityTheorem (D : R3SemanticData) : Prop :=
  ∀ quotient,
    D.FactorsThroughBoundedLocalType quotient →
    D.dim quotient ≤ D.C

/--
Semantic theorem-proof inputs for R3.

These are still inputs. This structure does not prove the underlying capacity lemma.
-/
structure R3TheoremProofInputs (D : R3SemanticData) where
  R3a_boundedLocalTypeFactorizationFiniteStateSpace : Prop
  R3a_supplied : R3a_boundedLocalTypeFactorizationFiniteStateSpace
  R3b_finiteStateFactorizationBoundsImageDimension : Prop
  R3b_supplied : R3b_finiteStateFactorizationBoundsImageDimension
  R3c_equalLocalTypeDataGivesEqualQuotientData : Prop
  R3c_supplied : R3c_equalLocalTypeDataGivesEqualQuotientData
  R3d_uniformDimensionBoundExtracted :
    ∀ quotient,
      D.FactorsThroughBoundedLocalType quotient →
      D.dim quotient ≤ D.C

/-- R3 theorem route from explicit semantic inputs. -/
theorem R3_UniformLocalTypeCapacity_from_semantic_inputs
    (D : R3SemanticData)
    (H : R3TheoremProofInputs D) :
    R3UniformLocalTypeCapacityTheorem D := by
  intro quotient hfactor
  exact H.R3d_uniformDimensionBoundExtracted quotient hfactor

/--
Combined semantic proof package.

This closes only the theorem-proof route from supplied semantic inputs.
It does not supply those semantic inputs.
-/
structure R1R2R3SemanticTheoremProofData where
  r1Data : R1SemanticData
  r2Data : R2SemanticData
  r3Data : R3SemanticData
  r1Inputs : R1TheoremProofInputs r1Data
  r2Inputs : R2TheoremProofInputs r2Data
  r3Inputs : R3TheoremProofInputs r3Data

def R1R2R3SemanticTheoremProofTargetsClosed
    (D : R1R2R3SemanticTheoremProofData) : Prop :=
  R1LongChordExclusionTheorem D.r1Data ∧
  R2DiameterSeparationFillingObstructionTheorem D.r2Data ∧
  R3UniformLocalTypeCapacityTheorem D.r3Data

/--
Conditional theorem-proof route from supplied semantic inputs.

This remains conditional on supplied semantic inputs.
-/
theorem R1_R2_R3_theorem_proof_targets_from_semantic_inputs
    (D : R1R2R3SemanticTheoremProofData) :
    R1R2R3SemanticTheoremProofTargetsClosed D := by
  constructor
  · exact R1_LongChordExclusion_from_semantic_inputs D.r1Data D.r1Inputs
  · constructor
    · exact R2_DiameterSeparationFillingObstruction_from_semantic_inputs D.r2Data D.r2Inputs
    · exact R3_UniformLocalTypeCapacity_from_semantic_inputs D.r3Data D.r3Inputs

/--
Concrete semantic objects required before theorem-level promotion can be attempted.
-/
structure R1R2R3ConcreteSemanticObjects where
  concreteR1WordEdgeFaceSupportModel : Prop
  concreteR2FiberChainBoundaryDiameterModel : Prop
  concreteR3LocalTypeQuotientDimensionModel : Prop

def R1R2R3ConcreteSemanticsSupplied
    (M : R1R2R3ConcreteSemanticObjects) : Prop :=
  M.concreteR1WordEdgeFaceSupportModel ∧
  M.concreteR2FiberChainBoundaryDiameterModel ∧
  M.concreteR3LocalTypeQuotientDimensionModel

theorem no_R1_R2_R3_theorem_promotion_without_concrete_semantics
    (M : R1R2R3ConcreteSemanticObjects)
    (hmissing :
      ¬ M.concreteR1WordEdgeFaceSupportModel ∨
      ¬ M.concreteR2FiberChainBoundaryDiameterModel ∨
      ¬ M.concreteR3LocalTypeQuotientDimensionModel) :
    ¬ R1R2R3ConcreteSemanticsSupplied M := by
  intro hsupplied
  rcases hmissing with hR1 | hR2 | hR3
  · exact hR1 hsupplied.1
  · exact hR2 hsupplied.2.1
  · exact hR3 hsupplied.2.2

end Frontier
end Chronos
