namespace Chronos
namespace Frontier

inductive AssumptionStatus where
  | proved
  | externalInput
  | conditional
  | openFrontier
deriving DecidableEq, Repr

inductive ClaimVerdict where
  | provedSurface
  | conditionalSurface
  | countermodelRequired
  | openMissingLemma
deriving DecidableEq, Repr

structure NormalizedClaim where
  id : String
  assumptions : String
  conclusion : String
  assumptionStatus : AssumptionStatus
  leanProofTarget : String
  countermodelTarget : String
  sinkLemma : String
  verdict : ClaimVerdict
deriving Repr

def globalURFDecisionAuditClaims : List NormalizedClaim :=
  [
    {
      id := "finite_list_positive_uniform_floor",
      assumptions := "nonempty finite list of strictly positive real masses",
      conclusion := "there exists a strictly positive uniform lower floor",
      assumptionStatus := AssumptionStatus.proved,
      leanProofTarget := "Chronos.Frontier.FiniteListPositiveUniformFloor",
      countermodelTarget := "none: list-coded finite positive support",
      sinkLemma := "none",
      verdict := ClaimVerdict.provedSurface
    },
    {
      id := "finite_support_restricted_ufeg_to_restricted_chronos_rr",
      assumptions := "finite positive support plus restricted admissible domain",
      conclusion := "restricted UniversalFiberEntropyGap feeds restricted Chronos-RR",
      assumptionStatus := AssumptionStatus.conditional,
      leanProofTarget := "Chronos.Frontier.FiniteSupportRestrictedUFEGToRestrictedChronosRR",
      countermodelTarget := "unrestricted arbitrary-fiber-mass data",
      sinkLemma := "uniform positivity or restricted-domain invariant",
      verdict := ClaimVerdict.conditionalSurface
    },
    {
      id := "unrestricted_universal_fiber_entropy_gap",
      assumptions := "arbitrary fiber-mass data",
      conclusion := "unrestricted UniversalFiberEntropyGap",
      assumptionStatus := AssumptionStatus.openFrontier,
      leanProofTarget := "none",
      countermodelTarget := "zero or vanishing fiber-mass family",
      sinkLemma := "unrestricted uniform positivity/coercivity",
      verdict := ClaimVerdict.countermodelRequired
    },
    {
      id := "unrestricted_chronos_rr_h41_fgl_p_np_clay",
      assumptions := "unrestricted Chronos-RR/H4.1/FGL terminal hypotheses",
      conclusion := "P vs NP or Clay-level closure",
      assumptionStatus := AssumptionStatus.openFrontier,
      leanProofTarget := "none",
      countermodelTarget := "boundary-overclaim audit",
      sinkLemma := "unrestricted UniversalFiberEntropyGap plus unrestricted DepthBridge",
      verdict := ClaimVerdict.openMissingLemma
    }
  ]

def globalURFDecisionAuditSinkLemmas : List String :=
  [
    "uniform positivity or restricted-domain invariant",
    "unrestricted uniform positivity/coercivity",
    "unrestricted UniversalFiberEntropyGap plus unrestricted DepthBridge"
  ]

inductive GlobalURFDecisionAuditStatus where
  | statusSurfaceOnly
deriving DecidableEq, Repr

def globalURFDecisionAuditStatus : GlobalURFDecisionAuditStatus :=
  GlobalURFDecisionAuditStatus.statusSurfaceOnly

theorem globalURFDecisionAudit_status_lock :
    globalURFDecisionAuditStatus = GlobalURFDecisionAuditStatus.statusSurfaceOnly := by
  rfl

theorem globalURFDecisionAudit_nonempty :
    globalURFDecisionAuditClaims ≠ [] := by
  decide

end Frontier
end Chronos
