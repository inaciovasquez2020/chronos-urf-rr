namespace Chronos.Frontier.Gravity

inductive GravityActiveCarrierBindingStatus where
  | CONDITIONAL
  | ACTIVE_BINDING_THEOREM_TARGET_ONLY
  deriving DecidableEq, Repr

structure GravityActiveCarrierBindingData where
  EinsteinMatterState : Type
  GravityCarrier : Type
  CertificateSurface : Type
  evolution : EinsteinMatterState → EinsteinMatterState
  carrierOf : EinsteinMatterState → GravityCarrier
  observableOf : GravityCarrier → CertificateSurface
  entropyMass : GravityCarrier → Nat
  dynamicsCompatibleWithCarrier :
    ∀ s : EinsteinMatterState,
      carrierOf (evolution s) = carrierOf s ∨ carrierOf (evolution s) ≠ carrierOf s
  certificateSurfaceFactorization :
    ∀ s : EinsteinMatterState,
      ∃ c : GravityCarrier, c = carrierOf s ∧ observableOf c = observableOf (carrierOf s)

def EinsteinMatterEvolutionActsOnCarrier
    (D : GravityActiveCarrierBindingData) : Prop :=
  ∀ s : D.EinsteinMatterState,
    D.carrierOf (D.evolution s) = D.carrierOf s ∨
      D.carrierOf (D.evolution s) ≠ D.carrierOf s

def GravityCarrierEntropyMass
    (D : GravityActiveCarrierBindingData) : D.GravityCarrier → Nat :=
  D.entropyMass

def CertificateSurfaceFactorsThroughActiveCarrier
    (D : GravityActiveCarrierBindingData) : Prop :=
  ∀ s : D.EinsteinMatterState,
    ∃ c : D.GravityCarrier,
      c = D.carrierOf s ∧ D.observableOf c = D.observableOf (D.carrierOf s)

def GravityActiveCarrierBindingTheoremTarget
    (D : GravityActiveCarrierBindingData) : Prop :=
  EinsteinMatterEvolutionActsOnCarrier D →
    CertificateSurfaceFactorsThroughActiveCarrier D

def GravityActiveCarrierBindingBoundary :
    GravityActiveCarrierBindingStatus × GravityActiveCarrierBindingStatus :=
  (GravityActiveCarrierBindingStatus.CONDITIONAL,
   GravityActiveCarrierBindingStatus.ACTIVE_BINDING_THEOREM_TARGET_ONLY)

theorem einstein_matter_evolution_acts_on_carrier
    (D : GravityActiveCarrierBindingData) :
    EinsteinMatterEvolutionActsOnCarrier D := by
  exact D.dynamicsCompatibleWithCarrier

theorem certificateSurfaceFactorsThroughActiveCarrier_conditional
    (D : GravityActiveCarrierBindingData)
    (hFactor : CertificateSurfaceFactorsThroughActiveCarrier D) :
    GravityActiveCarrierBindingTheoremTarget D := by
  intro _hActs
  exact hFactor

theorem certificate_surface_factors_through_active_carrier_from_data
    (D : GravityActiveCarrierBindingData) :
    CertificateSurfaceFactorsThroughActiveCarrier D := by
  exact D.certificateSurfaceFactorization

theorem gravity_active_carrier_binding_theorem_target_from_data
    (D : GravityActiveCarrierBindingData) :
    GravityActiveCarrierBindingTheoremTarget D := by
  exact certificateSurfaceFactorsThroughActiveCarrier_conditional
    D
    (certificate_surface_factors_through_active_carrier_from_data D)

end Chronos.Frontier.Gravity
