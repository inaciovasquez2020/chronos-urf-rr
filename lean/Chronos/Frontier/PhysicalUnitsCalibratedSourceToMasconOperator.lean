import Chronos.Frontier.PhysicalUnitsCalibratedSourceToMasconOperatorOrThirdPublicHoldout

namespace Chronos.Frontier

structure PhysicalUnitsCalibratedSourceToMasconOperator where
  sourcePhysicalUnitsOperatorRecorded : Bool
  sourceOutputUnitsRecorded : Bool
  sourceToGridPhysicalUnitsCalibrated : Bool
  sourceToMasconShapeOperatorRecorded : Bool
  masconUnitEquivalenceClosed : Bool
  timeDependentSourceToMasconOperatorClosed : Bool
  normalizedAlignmentComparisonRecorded : Bool
  missingClosureObjectsRecorded : Bool
  physicalSourceUnitsOperatorOnly : Bool
  masconUnitEquivalenceNotClosed : Bool
  timeDependentOperatorNotClosed : Bool
  comparisonOnly : Bool
  independentValidationRequiredBeforePhysicalClaim : Bool
  noEmpiricalGravityResultClaim : Bool
  noGRFailureClaim : Bool
  noNewGravityClaim : Bool
  noDarkMatterReplacementClaim : Bool
  noLambdaCDMFailureClaim : Bool
  noQuantumGravityClaim : Bool
  noClayClaim : Bool
deriving Repr

def physicalUnitsCalibratedSourceToMasconOperator20260530 :
    PhysicalUnitsCalibratedSourceToMasconOperator := {
  sourcePhysicalUnitsOperatorRecorded := true
  sourceOutputUnitsRecorded := true
  sourceToGridPhysicalUnitsCalibrated := true
  sourceToMasconShapeOperatorRecorded := true
  masconUnitEquivalenceClosed := false
  timeDependentSourceToMasconOperatorClosed := false
  normalizedAlignmentComparisonRecorded := true
  missingClosureObjectsRecorded := true
  physicalSourceUnitsOperatorOnly := true
  masconUnitEquivalenceNotClosed := true
  timeDependentOperatorNotClosed := true
  comparisonOnly := true
  independentValidationRequiredBeforePhysicalClaim := true
  noEmpiricalGravityResultClaim := true
  noGRFailureClaim := true
  noNewGravityClaim := true
  noDarkMatterReplacementClaim := true
  noLambdaCDMFailureClaim := true
  noQuantumGravityClaim := true
  noClayClaim := true
}

theorem physicalUnitsCalibratedSourceToMasconOperator_boundary :
    physicalUnitsCalibratedSourceToMasconOperator20260530.sourcePhysicalUnitsOperatorRecorded = true ∧
    physicalUnitsCalibratedSourceToMasconOperator20260530.sourceOutputUnitsRecorded = true ∧
    physicalUnitsCalibratedSourceToMasconOperator20260530.sourceToGridPhysicalUnitsCalibrated = true ∧
    physicalUnitsCalibratedSourceToMasconOperator20260530.sourceToMasconShapeOperatorRecorded = true ∧
    physicalUnitsCalibratedSourceToMasconOperator20260530.masconUnitEquivalenceClosed = false ∧
    physicalUnitsCalibratedSourceToMasconOperator20260530.timeDependentSourceToMasconOperatorClosed = false ∧
    physicalUnitsCalibratedSourceToMasconOperator20260530.normalizedAlignmentComparisonRecorded = true ∧
    physicalUnitsCalibratedSourceToMasconOperator20260530.missingClosureObjectsRecorded = true ∧
    physicalUnitsCalibratedSourceToMasconOperator20260530.physicalSourceUnitsOperatorOnly = true ∧
    physicalUnitsCalibratedSourceToMasconOperator20260530.masconUnitEquivalenceNotClosed = true ∧
    physicalUnitsCalibratedSourceToMasconOperator20260530.timeDependentOperatorNotClosed = true ∧
    physicalUnitsCalibratedSourceToMasconOperator20260530.comparisonOnly = true ∧
    physicalUnitsCalibratedSourceToMasconOperator20260530.independentValidationRequiredBeforePhysicalClaim = true ∧
    physicalUnitsCalibratedSourceToMasconOperator20260530.noEmpiricalGravityResultClaim = true ∧
    physicalUnitsCalibratedSourceToMasconOperator20260530.noGRFailureClaim = true ∧
    physicalUnitsCalibratedSourceToMasconOperator20260530.noNewGravityClaim = true ∧
    physicalUnitsCalibratedSourceToMasconOperator20260530.noDarkMatterReplacementClaim = true ∧
    physicalUnitsCalibratedSourceToMasconOperator20260530.noLambdaCDMFailureClaim = true ∧
    physicalUnitsCalibratedSourceToMasconOperator20260530.noQuantumGravityClaim = true ∧
    physicalUnitsCalibratedSourceToMasconOperator20260530.noClayClaim = true := by
  native_decide

end Chronos.Frontier
