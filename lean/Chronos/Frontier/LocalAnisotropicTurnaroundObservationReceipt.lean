import Chronos.Frontier.LocalAnisotropicTurnaroundInputSurface

/-
Bounded observational receipt for the Local Group Hubble-flow /
zero-velocity-radius input surface.

This file records source metadata and receipt-scale constants only.
It does not claim a gravity closure, Einstein-limit derivation, or
new cosmology solution.
-/

structure LocalAnisotropicTurnaroundObservationReceipt : Type where
  sourceTitle : String
  sourceAuthors : String
  sourceYear : Nat
  sourceArxivId : String
  sourceDoi : String
  sampleGalaxyCount : Nat
  distanceLowerMpcX10 : Nat
  distanceUpperMpcX10 : Nat
  localHubbleKmSPerMpc : Nat
  peculiarVelocityDispersionKmS : Nat
  zeroVelocityRadiusMpcX100 : Nat
  radialVelocityErrorKmS : Nat
  distanceErrorVelocityEquivalentKmS : Nat
  boundaryNoGravityClosure : Prop
  boundaryNoEinsteinLimit : Prop
  boundaryNoNewCosmologySolution : Prop

def localAnisotropicTurnaroundKarachentsev2009Receipt :
    LocalAnisotropicTurnaroundObservationReceipt where
  sourceTitle := "The Hubble flow around the Local Group"
  sourceAuthors := "I. D. Karachentsev, O. G. Kashibadze, D. I. Makarov, R. B. Tully"
  sourceYear := 2009
  sourceArxivId := "0811.4610"
  sourceDoi := "10.1111/j.1365-2966.2008.14300.x"
  sampleGalaxyCount := 30
  distanceLowerMpcX10 := 7
  distanceUpperMpcX10 := 30
  localHubbleKmSPerMpc := localAnisotropicTurnaroundReceiptLocalHubbleKmSPerMpc
  peculiarVelocityDispersionKmS := localAnisotropicTurnaroundReceiptPeculiarVelocityResidualKmS
  zeroVelocityRadiusMpcX100 := localAnisotropicTurnaroundReceiptR0MpcX100
  radialVelocityErrorKmS := 4
  distanceErrorVelocityEquivalentKmS := 10
  boundaryNoGravityClosure := True
  boundaryNoEinsteinLimit := True
  boundaryNoNewCosmologySolution := True

theorem local_anisotropic_turnaround_observation_receipt_matches_input_constants :
    localAnisotropicTurnaroundKarachentsev2009Receipt.localHubbleKmSPerMpc = 78 ∧
    localAnisotropicTurnaroundKarachentsev2009Receipt.peculiarVelocityDispersionKmS = 25 ∧
    localAnisotropicTurnaroundKarachentsev2009Receipt.zeroVelocityRadiusMpcX100 = 96 :=
  ⟨rfl, rfl, rfl⟩

theorem local_anisotropic_turnaround_observation_receipt_is_boundary_only :
    localAnisotropicTurnaroundKarachentsev2009Receipt.boundaryNoGravityClosure ∧
    localAnisotropicTurnaroundKarachentsev2009Receipt.boundaryNoEinsteinLimit ∧
    localAnisotropicTurnaroundKarachentsev2009Receipt.boundaryNoNewCosmologySolution :=
  ⟨True.intro, True.intro, True.intro⟩
