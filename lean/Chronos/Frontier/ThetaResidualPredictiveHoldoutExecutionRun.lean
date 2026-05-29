import Chronos.Frontier.ThetaResidualPredictiveHoldoutWithoutResidualAccess

namespace Chronos.Frontier

/--
Execution metadata for a theta-residual predictive holdout run.

This records an executed run only after the no-residual-access holdout gate has
already been supplied.  It does not certify physical validation or nontrivial
predictive signal.
-/
structure ThetaResidualPredictiveHoldoutExecutionRun where
  gate : ThetaResidualPredictiveHoldoutWithoutResidualAccess
  rowCount : Nat
  rowCount_matches : rowCount = gate.rows.length
  reductionNumerator : Nat
  reductionDenominator : Nat
  denominator_pos : reductionDenominator ≠ 0
  thresholdPassed : Bool

theorem ThetaResidualPredictiveHoldoutExecutionRun.nonempty_rows
    (R : ThetaResidualPredictiveHoldoutExecutionRun) :
    R.gate.rows ≠ [] :=
  R.gate.nonempty_rows

theorem ThetaResidualPredictiveHoldoutExecutionRun.rowCount_eq_length
    (R : ThetaResidualPredictiveHoldoutExecutionRun) :
    R.rowCount = R.gate.rows.length :=
  R.rowCount_matches

theorem ThetaResidualPredictiveHoldoutExecutionRun.no_residual_access
    (R : ThetaResidualPredictiveHoldoutExecutionRun)
    {row : ThetaResidualHoldoutRow}
    (hrow : row ∈ R.gate.rows) :
    row.noResidualAccess :=
  R.gate.no_residual_access hrow

theorem ThetaResidualPredictiveHoldoutExecutionRun.no_half_residual_identity_access
    (R : ThetaResidualPredictiveHoldoutExecutionRun)
    {row : ThetaResidualHoldoutRow}
    (hrow : row ∈ R.gate.rows) :
    row.noHalfResidualIdentityAccess :=
  R.gate.no_half_residual_identity_access hrow

theorem ThetaResidualPredictiveHoldoutExecutionRun.clean_rows
    (R : ThetaResidualPredictiveHoldoutExecutionRun)
    {row : ThetaResidualHoldoutRow}
    (hrow : row ∈ R.gate.rows) :
    row.clean :=
  R.gate.clean_rows hrow

def ThetaResidualPredictiveHoldoutExecutionRun.certifiedBoundary : String :=
  "EXECUTION_RUN_ONLY_NO_VALIDATION_CLAIM"

def ThetaResidualPredictiveHoldoutExecutionRun.nextObject : String :=
  "ThetaResidualPredictiveHoldoutIndependentValidationGate"

end Chronos.Frontier
