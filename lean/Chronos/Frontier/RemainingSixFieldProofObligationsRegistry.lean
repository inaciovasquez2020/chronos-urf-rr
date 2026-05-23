namespace Chronos.Frontier

/--
Status tags for remaining six-field gravity proof obligations.

This registry records proof obligations only. It does not supply analytic
estimates, close the six-field package, or promote any gravity theorem.
-/
inductive ProofObligationStatus where
  | open
  | suppliedTarget
  | conditional
  | closed
deriving Repr, DecidableEq

structure ProofObligation where
  name : String
  summary : String
  status : ProofObligationStatus
  theoremPromotionAllowed : Bool
deriving Repr

def remainingSixFieldProofObligationNames : List String :=
  [ "AnalyticEstimateCandidatePacket"
  , "FilledConcreteInitialDataClass"
  , "FilledConcreteMatterModel"
  , "LocalExistenceProof"
  , "LocalUniquenessProof"
  , "ConstraintPropagationProof"
  , "GaugeControlProof"
  , "EnergyBootstrapProof"
  , "RefinedEnergyEstimateProof"
  , "BootstrapClosureProof"
  , "MatterCouplingControlProof"
  , "EnergyConditionPreservationProof"
  , "NonSymmetricPersistenceProof"
  , "ConcentrationTransportProof"
  , "ContinuationAlternativeProof"
  , "CollapseThresholdCriterionProof"
  , "CollapseGateTriggerProof"
  , "SlabIterationProof"
  , "BootstrapSlabToSixFieldInstantiationProof"
  , "NonSymmetricEinsteinMatterBootstrapKernelAnalyticPackageProof"
  , "SixFieldAnalyticPackageHypothesisProof"
  , "RestrictedGravityClosureBridgeProof"
  ]

theorem remaining_six_field_proof_obligation_count :
    remainingSixFieldProofObligationNames.length = 22 := rfl

def openObligation (name summary : String) : ProofObligation :=
  { name := name
    summary := summary
    status := ProofObligationStatus.open
    theoremPromotionAllowed := false }

def remainingSixFieldProofObligations : List ProofObligation :=
  [ openObligation "AnalyticEstimateCandidatePacket"
      "candidate packet collecting analytic estimates or cited proof sources"
  , openObligation "FilledConcreteInitialDataClass"
      "filled initial-data class with regularity, constraints, seeds, and admissibility"
  , openObligation "FilledConcreteMatterModel"
      "filled matter model with stress-energy, coupling, conservation, and source control"
  , openObligation "LocalExistenceProof"
      "existence of slab solution from admissible initial data"
  , openObligation "LocalUniquenessProof"
      "uniqueness of slab solution in the selected solution class"
  , openObligation "ConstraintPropagationProof"
      "initial constraints remain true under evolution"
  , openObligation "GaugeControlProof"
      "selected gauge remains controlled on each slab"
  , openObligation "EnergyBootstrapProof"
      "bootstrap energy bound is propagated on a slab"
  , openObligation "RefinedEnergyEstimateProof"
      "assumed bootstrap bound improves to a refined estimate"
  , openObligation "BootstrapClosureProof"
      "refined estimate closes the bootstrap loop"
  , openObligation "MatterCouplingControlProof"
      "matter source terms remain controlled by the energy hierarchy"
  , openObligation "EnergyConditionPreservationProof"
      "selected energy condition persists under evolution"
  , openObligation "NonSymmetricPersistenceProof"
      "non-symmetric sector does not vanish or exit the admissible class"
  , openObligation "ConcentrationTransportProof"
      "initial concentration seed persists or strengthens along evolution"
  , openObligation "ContinuationAlternativeProof"
      "regular continuation holds or threshold is reached"
  , openObligation "CollapseThresholdCriterionProof"
      "threshold condition is precisely defined and reachable"
  , openObligation "CollapseGateTriggerProof"
      "threshold implies QL_CollapseGate"
  , openObligation "SlabIterationProof"
      "closed slab advances to the next slab"
  , openObligation "BootstrapSlabToSixFieldInstantiationProof"
      "analytic estimates fill all six-field slots"
  , openObligation "NonSymmetricEinsteinMatterBootstrapKernelAnalyticPackageProof"
      "kernel package is fully instantiated from lower obligations"
  , openObligation "SixFieldAnalyticPackageHypothesisProof"
      "six-field analytic package follows from the instantiated kernel"
  , openObligation "RestrictedGravityClosureBridgeProof"
      "six-field analytic package implies the restricted gravity target"
  ]

theorem remaining_six_field_proof_obligations_count :
    remainingSixFieldProofObligations.length = 22 := rfl

def remainingSixFieldBlockedClaims : List String :=
  [ "unrestricted Einstein-matter well-posedness"
  , "unrestricted non-symmetric collapse theorem"
  , "cosmic censorship"
  , "hoop conjecture"
  , "unrestricted gravity closure"
  , "Chronos-RR"
  , "H4.1/FGL"
  , "P vs NP"
  , "any Clay problem"
  ]

structure RemainingSixFieldProofObligationsRegistry where
  obligations : List ProofObligation
  blockedClaims : List String
  allObligationsRemainOpen : Prop
  provesSixFieldAnalyticPackageHypothesis : Prop
  provesGravityClosure : Prop

def remainingSixFieldProofObligationsRegistry :
    RemainingSixFieldProofObligationsRegistry :=
  { obligations := remainingSixFieldProofObligations
    blockedClaims := remainingSixFieldBlockedClaims
    allObligationsRemainOpen := True
    provesSixFieldAnalyticPackageHypothesis := False
    provesGravityClosure := False }

theorem remaining_registry_does_not_prove_six_field :
    remainingSixFieldProofObligationsRegistry.provesSixFieldAnalyticPackageHypothesis = False := rfl

theorem remaining_registry_does_not_prove_gravity_closure :
    remainingSixFieldProofObligationsRegistry.provesGravityClosure = False := rfl

end Chronos.Frontier
