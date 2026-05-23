namespace Chronos.Frontier

/--
Status tags for candidate analytic estimates.

This is source/estimate-candidate tracking only. No candidate is treated as a
completed proof unless a later object supplies the analytic derivation.
-/
inductive AnalyticEstimateCandidateStatus where
  | candidateOnly
  | sourceMapped
  | insufficientForProof
  | open
deriving Repr, DecidableEq

structure AnalyticEstimateCandidate where
  name : String
  targetSlot : String
  sourceClass : String
  admissibleUse : String
  blockedUse : String
  status : AnalyticEstimateCandidateStatus
  proofSupplied : Bool
deriving Repr

def analyticEstimateCandidateNames : List String :=
  [ "SemiclassicalEinsteinKGFixedPointTemplate"
  , "MaxwellBoltzmannBianchiMatterWellPosednessTemplate"
  , "ActiveLiquidCrystalBootstrapEnergyTemplate"
  , "TSIMFGRPDEFurtherLiteratureTargets"
  , "LeanSearchPremiseRetrievalSupport"
  , "StatisticalHypothesisTestingEmpiricalAuditSupport"
  , "StatisticalFieldTheoryBackgroundSupport"
  , "KOTheoreticGravityBackgroundSupport"
  , "TotalityTheoremClaimBoundaryBackground"
  , "ConcreteSixFieldSlotEstimateGap"
  ]

theorem analytic_estimate_candidate_name_count :
    analyticEstimateCandidateNames.length = 10 := rfl

def candidateOnly
    (name targetSlot sourceClass admissibleUse blockedUse : String) :
    AnalyticEstimateCandidate :=
  { name := name
    targetSlot := targetSlot
    sourceClass := sourceClass
    admissibleUse := admissibleUse
    blockedUse := blockedUse
    status := AnalyticEstimateCandidateStatus.candidateOnly
    proofSupplied := false }

def analyticEstimateCandidates : List AnalyticEstimateCandidate :=
  [ candidateOnly
      "SemiclassicalEinsteinKGFixedPointTemplate"
      "localExistenceSlot / constraintPropagationSlot"
      "semiclassical Einstein--Klein--Gordon fixed-point source"
      "fixed-point and semiclassical Einstein-equation technique template"
      "not a six-field analytic package proof"
  , candidateOnly
      "MaxwellBoltzmannBianchiMatterWellPosednessTemplate"
      "localExistenceSlot / matterCouplingControlSlot"
      "Maxwell--Boltzmann system in Bianchi spacetime source"
      "matter-model and iteration-template candidate"
      "not a non-symmetric Einstein--matter bootstrap kernel proof"
  , candidateOnly
      "ActiveLiquidCrystalBootstrapEnergyTemplate"
      "energyBootstrapSlot / refinedEnergyEstimateSlot"
      "non-GR PDE bootstrap source"
      "generic bootstrap, commutator, and time-weighted energy technique template"
      "not an Einstein--matter proof"
  , candidateOnly
      "TSIMFGRPDEFurtherLiteratureTargets"
      "sourceMapFollowupSlot"
      "conference program and schedule source"
      "identify GR/PDE talks for later literature follow-up"
      "not a proof source"
  , candidateOnly
      "LeanSearchPremiseRetrievalSupport"
      "formalizationToolingSlot"
      "Lean premise-retrieval tooling source"
      "support Mathlib premise discovery during formalization"
      "not an analytic estimate"
  , candidateOnly
      "StatisticalHypothesisTestingEmpiricalAuditSupport"
      "empiricalAuditSlot"
      "statistical methodology source"
      "support empirical validation language outside the gravity proof"
      "not a GR/PDE proof source"
  , candidateOnly
      "StatisticalFieldTheoryBackgroundSupport"
      "backgroundFieldTheorySlot"
      "statistical field theory background source"
      "background terminology and analogy support"
      "not an Einstein--matter analytic package proof"
  , candidateOnly
      "KOTheoreticGravityBackgroundSupport"
      "topologicalBackgroundSlot"
      "KO-theory gravity preprint/background source"
      "topological background/source-map support"
      "not a PDE estimate or collapse proof"
  , candidateOnly
      "TotalityTheoremClaimBoundaryBackground"
      "claimBoundaryAuditSlot"
      "broad foundational preprint/source"
      "claim-boundary audit only"
      "not a mathematical or physical proof input"
  , candidateOnly
      "ConcreteSixFieldSlotEstimateGap"
      "allSixFieldAnalyticSlots"
      "open analytic estimate gap"
      "record that no candidate currently fills all analytic slots"
      "not theorem promotion"
  ]

theorem analytic_estimate_candidate_count :
    analyticEstimateCandidates.length = 10 := rfl

def analyticEstimateCandidatePacketBlockedClaims : List String :=
  [ "proof of SixFieldAnalyticPackageHypothesis"
  , "proof of NonSymmetricEinsteinMatterBootstrapKernelAnalyticPackage"
  , "proof of Einstein-matter well-posedness"
  , "proof of non-symmetric persistence"
  , "proof of matter-coupling control"
  , "proof of concentration transport"
  , "proof of collapse-gate trigger"
  , "proof of cosmic censorship"
  , "proof of hoop conjecture"
  , "proof of gravity closure"
  , "proof of Chronos-RR"
  , "proof of H4.1/FGL"
  , "proof of P vs NP"
  , "proof of any Clay problem"
  ]

structure AnalyticEstimateCandidatePacket where
  candidates : List AnalyticEstimateCandidate
  blockedClaims : List String
  allCandidatesProofSuppliedFalse : Prop
  provesSixFieldAnalyticPackageHypothesis : Prop
  provesGravityClosure : Prop

def analyticEstimateCandidatePacket : AnalyticEstimateCandidatePacket :=
  { candidates := analyticEstimateCandidates
    blockedClaims := analyticEstimateCandidatePacketBlockedClaims
    allCandidatesProofSuppliedFalse := True
    provesSixFieldAnalyticPackageHypothesis := False
    provesGravityClosure := False }

theorem analytic_estimate_candidate_packet_does_not_prove_six_field :
    analyticEstimateCandidatePacket.provesSixFieldAnalyticPackageHypothesis = False := rfl

theorem analytic_estimate_candidate_packet_does_not_prove_gravity_closure :
    analyticEstimateCandidatePacket.provesGravityClosure = False := rfl

end Chronos.Frontier
