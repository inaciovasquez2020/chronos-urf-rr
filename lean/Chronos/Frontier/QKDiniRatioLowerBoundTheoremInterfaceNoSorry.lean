import Chronos.Frontier.GenuineAnalyticDiniEstimateProofOrStop
import Mathlib

namespace Chronos.Frontier

structure GenuineAnalyticDiniEstimate where
  lower_bound_statement : Prop
  source_bound_shape_acknowledged : True := trivial

structure QKDiniRatioLowerBoundTheoremInterface where
  source_id : String
  source_doi : String
  parameter_valid :
    NondegenerateSourceValidExternalQKDiniCoefficientSlice
  source_theorem_supplies_statement :
    GenuineAnalyticDiniEstimate

def genuineAnalyticDiniEstimate_from_source_theorem
    (T : QKDiniRatioLowerBoundTheoremInterface) :
    GenuineAnalyticDiniEstimate :=
  T.source_theorem_supplies_statement

inductive QKDiniRatioLowerBoundTheoremInterfaceNoSorryStatus where
  | conditionalExternalTheoremInterfaceOnly

def qkDiniRatioLowerBoundTheoremInterfaceNoSorryStatus :
    QKDiniRatioLowerBoundTheoremInterfaceNoSorryStatus :=
  QKDiniRatioLowerBoundTheoremInterfaceNoSorryStatus.conditionalExternalTheoremInterfaceOnly

theorem qkDiniRatioLowerBoundTheoremInterfaceNoSorryStatus_eq :
    qkDiniRatioLowerBoundTheoremInterfaceNoSorryStatus =
      QKDiniRatioLowerBoundTheoremInterfaceNoSorryStatus.conditionalExternalTheoremInterfaceOnly := rfl

def QKDiniRatioLowerBoundTheoremInterfaceNoSorryBoundary : List String :=
  [
    "CONDITIONAL_EXTERNAL_THEOREM_INTERFACE_ONLY",
    "NO_INTERNAL_ANALYTIC_PROOF",
    "NO_CONVERGENCE_PROOF",
    "NO_SUMMABILITY_PROOF",
    "NO_RATIO_BOUND_PROOF",
    "NO_FINAL_ANALYTIC_RESULT",
    "NO_P_VS_NP_CLAIM",
    "NO_CLAY_CLAIM"
  ]

end Chronos.Frontier
