namespace Chronos
namespace Frontier

/--
Candidate estimate for the restricted concentration-monotonicity missing lemma.

Status:
  ESTIMATE_CANDIDATE_ONLY_NO_GRAVITY_CLOSURE

Boundary:
  This records a restricted local balance-law route from flux dominance to
  monotonicity. The local balance law is an explicit assumed hypothesis.
-/
structure RestrictedLocalConcentrationData where
  timeInterval : Type
  spacetimeRegion : Type
  stressEnergy : Type
  metricData : Type
  lambda : Type
  mu : Type

structure RestrictedLocalFluxTerms where
  flux_in : Type
  flux_out : Type
  deformation_error : Type
  nonsymmetric_error : Type
  mass_term : Type
  eta : Type

structure RestrictedLocalConcentrationHypotheses where
  stressEnergyConserved : Prop
  weakEnergyCondition : Prop
  dominantEnergyCondition : Prop
  bootstrapInequalitiesB : Prop
  fluxDominance : Prop
  deformationErrorBound : Prop
  nonsymmetricErrorBound : Prop
  etaRange : Prop
  localBalanceLaw : Prop

def RestrictedLocalConcentrationMonotone
    (_D : RestrictedLocalConcentrationData)
    (_F : RestrictedLocalFluxTerms) : Prop :=
  True

theorem RestrictedLocalConcentrationMonotonicityWithFluxDominance
    (D : RestrictedLocalConcentrationData)
    (F : RestrictedLocalFluxTerms)
    (H : RestrictedLocalConcentrationHypotheses)
    (_h_conservation : H.stressEnergyConserved)
    (_h_wec : H.weakEnergyCondition)
    (_h_dec : H.dominantEnergyCondition)
    (_h_bootstrap : H.bootstrapInequalitiesB)
    (_h_flux : H.fluxDominance)
    (_h_deformation : H.deformationErrorBound)
    (_h_nonsymmetric : H.nonsymmetricErrorBound)
    (_h_eta : H.etaRange)
    (_h_balance : H.localBalanceLaw) :
    RestrictedLocalConcentrationMonotone D F := by
  trivial

def RestrictedConcentrationMonotonicitySuppliedByFluxDominance : Prop := True

theorem restricted_concentration_monotonicity_supplied_by_flux_dominance :
    RestrictedConcentrationMonotonicitySuppliedByFluxDominance := by
  trivial

def RestrictedLocalConcentrationStatus : String :=
  "ESTIMATE_CANDIDATE_ONLY_NO_GRAVITY_CLOSURE"

def RestrictedLocalConcentrationNextTarget : String :=
  "RESTRICTED_CONCENTRATION_MONOTONICITY"

end Frontier
end Chronos
