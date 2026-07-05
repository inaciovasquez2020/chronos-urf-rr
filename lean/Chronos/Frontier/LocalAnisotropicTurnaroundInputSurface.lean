import Chronos.Frontier.R1R2R3AxiomBoundaryClosure

/-
Local anisotropic turnaround input surface.

This file is only an input/prediction-interface surface. It records the
known observational transition between Local-Group-scale bound motion and
large-scale Hubble flow without deriving physical gravity, Einstein dynamics,
or a new cosmology.
-/

structure LocalAnisotropicTurnaroundInputSurface : Type 1 where
  Structure : Type
  Center : Structure
  DistanceMpcX100 : Structure → Nat
  RadialVelocityKmS : Structure → Int
  HubbleParameterKmSPerMpc : Nat
  PeculiarVelocityResidualKmS : Structure → Int
  ZeroVelocityRadiusMpcX100 : Nat
  SphericalTurnaroundPredictionMpcX100 : Nat
  AnisotropicResidual : Structure → Prop
  noGravityClosureClaim : Prop
  noEinsteinLimitClaim : Prop
  noNewCosmologySolutionClaim : Prop

/-- Receipt-scaled Local Group zero-velocity radius: R₀ ≈ 0.96 Mpc. -/
def localAnisotropicTurnaroundReceiptR0MpcX100 : Nat := 96

/-- Receipt local Hubble-flow slope near the Local Group: H ≈ 78 km/s/Mpc. -/
def localAnisotropicTurnaroundReceiptLocalHubbleKmSPerMpc : Nat := 78

/-- Receipt-scale peculiar-velocity residual/dispersion marker: ≈ 25 km/s. -/
def localAnisotropicTurnaroundReceiptPeculiarVelocityResidualKmS : Nat := 25

/--
A residual is only classified as a candidate prediction-interface datum.
It is not promoted to a physical gravity derivation.
-/
structure LocalAnisotropicTurnaroundPredictionInterfaceCandidate : Type 1 where
  surface : LocalAnisotropicTurnaroundInputSurface
  witness : surface.Structure
  residual : surface.AnisotropicResidual witness

theorem anisotropic_residual_is_prediction_interface_candidate
    (surface : LocalAnisotropicTurnaroundInputSurface)
    (witness : surface.Structure)
    (residual : surface.AnisotropicResidual witness) :
    Nonempty LocalAnisotropicTurnaroundPredictionInterfaceCandidate :=
  ⟨⟨surface, witness, residual⟩⟩
