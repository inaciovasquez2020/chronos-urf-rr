import Chronos.Frontier.ThetaResidualNontrivialityLeakageAudit

namespace Chronos.Frontier

/--
A finite holdout row for theta-residual prediction.

`residual` is the withheld residual target.
`prediction` is the model output.
`baseline` is the comparison output.
`residualAccess` records whether the prediction rule directly used the withheld residual.
`halfResidualIdentityAccess` records whether the prediction rule used the deterministic
half-residual identity isolated by the leakage audit.
-/
structure ThetaResidualHoldoutRow where
  residual : Int
  prediction : Int
  baseline : Int
  residualAccess : Bool
  halfResidualIdentityAccess : Bool
deriving DecidableEq, Repr

def ThetaResidualHoldoutRow.noResidualAccess
    (row : ThetaResidualHoldoutRow) : Prop :=
  row.residualAccess = false

def ThetaResidualHoldoutRow.noHalfResidualIdentityAccess
    (row : ThetaResidualHoldoutRow) : Prop :=
  row.halfResidualIdentityAccess = false

def ThetaResidualHoldoutRow.clean
    (row : ThetaResidualHoldoutRow) : Prop :=
  row.noResidualAccess ∧ row.noHalfResidualIdentityAccess

structure ThetaResidualPredictiveHoldoutWithoutResidualAccess where
  rows : List ThetaResidualHoldoutRow
  nonempty_rows : rows ≠ []
  all_clean : ∀ row, row ∈ rows → row.clean

theorem ThetaResidualPredictiveHoldoutWithoutResidualAccess.no_residual_access
    (H : ThetaResidualPredictiveHoldoutWithoutResidualAccess)
    {row : ThetaResidualHoldoutRow}
    (hrow : row ∈ H.rows) :
    row.noResidualAccess :=
  (H.all_clean row hrow).1

theorem ThetaResidualPredictiveHoldoutWithoutResidualAccess.no_half_residual_identity_access
    (H : ThetaResidualPredictiveHoldoutWithoutResidualAccess)
    {row : ThetaResidualHoldoutRow}
    (hrow : row ∈ H.rows) :
    row.noHalfResidualIdentityAccess :=
  (H.all_clean row hrow).2

theorem ThetaResidualPredictiveHoldoutWithoutResidualAccess.clean_rows
    (H : ThetaResidualPredictiveHoldoutWithoutResidualAccess)
    {row : ThetaResidualHoldoutRow}
    (hrow : row ∈ H.rows) :
    row.clean :=
  H.all_clean row hrow

def ThetaResidualPredictiveHoldoutWithoutResidualAccess.certifiedBoundary : String :=
  "HOLDOUT_GATE_ONLY_NO_PREDICTIVE_SIGNAL_CLAIM"

def ThetaResidualPredictiveHoldoutWithoutResidualAccess.nextObject : String :=
  "ThetaResidualPredictiveHoldoutExecutionRun"

end Chronos.Frontier
