import Chronos.Frontier.FiniteSpectralCompactnessCertificate

namespace Chronos
namespace Frontier
namespace Gravity
namespace EinsteinDynamicsRegularityTransferFrontier

open FiniteSpectralCompactness

structure EinsteinMatterDevelopment where
  spacetimeDimension : Nat
  spacetimeDimension_pos : 0 < spacetimeDimension
  hasLorentzMetric : Prop
  hasMatterStressTensor : Prop
  globallyHyperbolicRegion : Prop

structure EinsteinEquationSatisfied
    (D : EinsteinMatterDevelopment) where
  cosmologicalConstant : Int
  equationSatisfied : Prop
  conservationSatisfied : Prop

structure BoundaryFluxBound
    (D : EinsteinMatterDevelopment) where
  fluxBound : Nat
  fluxBound_pos : 0 < fluxBound
  finiteBoundaryArea : Prop
  finiteEnergyFlux : Prop

structure BackreactionControlled
    (D : EinsteinMatterDevelopment) where
  controlScale : Nat
  controlScale_pos : 0 < controlScale
  noUnboundedModeCreation : Prop
  detectorCutoffStable : Prop

structure EinsteinDynamicsRegularityInput where
  detectorAlgebra : FiniteDetectorAlgebra
  spectralCutoff : SpectralCutoff
  budget : BoundedEnergyAreaBudget
  development : EinsteinMatterDevelopment
  equation : EinsteinEquationSatisfied development
  flux : BoundaryFluxBound development
  backreaction : BackreactionControlled development

def EinsteinDynamicsRegularityTransfer
    (I : EinsteinDynamicsRegularityInput) : Prop :=
  ∃ S : BoundaryObservableStateSpace
      I.detectorAlgebra
      I.spectralCutoff
      I.budget,
    ∀ _epsilonIndex : Nat,
      Nonempty
        (FiniteSpectralCompactnessCertificate
          I.detectorAlgebra
          I.spectralCutoff
          I.budget
          S)

structure EinsteinDynamicsRegularityTransferFrontier where
  input : EinsteinDynamicsRegularityInput
  weakestMissingLemma : Prop
  weakestMissingLemma_eq :
    weakestMissingLemma = EinsteinDynamicsRegularityTransfer input
  status : String
  status_eq : status = "FRONTIER_OPEN"

def regularityTransferFrontier
    (I : EinsteinDynamicsRegularityInput) :
    EinsteinDynamicsRegularityTransferFrontier :=
  {
    input := I
    weakestMissingLemma := EinsteinDynamicsRegularityTransfer I
    weakestMissingLemma_eq := rfl
    status := "FRONTIER_OPEN"
    status_eq := rfl
  }

def EinsteinDynamicsCompactnessTransferTarget
    (I : EinsteinDynamicsRegularityInput) : Prop :=
  EinsteinDynamicsRegularityTransfer I

structure EinsteinDynamicsCompactnessTransferStatus where
  input : EinsteinDynamicsRegularityInput
  regularityFrontier : EinsteinDynamicsRegularityTransferFrontier
  compactnessTarget : Prop
  compactnessTarget_eq :
    compactnessTarget = EinsteinDynamicsCompactnessTransferTarget input
  noTheoremPromotion : Prop

def compactnessTransferStatus
    (I : EinsteinDynamicsRegularityInput) :
    EinsteinDynamicsCompactnessTransferStatus :=
  {
    input := I
    regularityFrontier := regularityTransferFrontier I
    compactnessTarget := EinsteinDynamicsCompactnessTransferTarget I
    compactnessTarget_eq := rfl
    noTheoremPromotion := True
  }

end EinsteinDynamicsRegularityTransferFrontier
end Gravity
end Frontier
end Chronos
