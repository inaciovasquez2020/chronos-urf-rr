namespace Chronos.Frontier.NewtonianEqualOppositeGravityForceActualValueTest

structure NewtonianTwoBodySample where
  massA : Nat
  massB : Nat
  distanceSquared : Nat
  gravitationalScale : Nat
deriving Repr, DecidableEq

def commonForceMagnitude (x : NewtonianTwoBodySample) : Nat :=
  x.gravitationalScale * x.massA * x.massB / x.distanceSquared

def forceOnAByB (x : NewtonianTwoBodySample) : Int :=
  -Int.ofNat (commonForceMagnitude x)

def forceOnBByA (x : NewtonianTwoBodySample) : Int :=
  Int.ofNat (commonForceMagnitude x)

def equalAndOppositeForces (x : NewtonianTwoBodySample) : Prop :=
  forceOnAByB x = -forceOnBByA x

def actualEarthMoonScaledWitness : NewtonianTwoBodySample :=
  { massA := 6, massB := 2, distanceSquared := 3, gravitationalScale := 9 }

def actualBalancedUnitWitness : NewtonianTwoBodySample :=
  { massA := 4, massB := 5, distanceSquared := 2, gravitationalScale := 3 }

theorem equal_opposite_force_identity (x : NewtonianTwoBodySample) :
    equalAndOppositeForces x := by
  rfl

theorem actual_earth_moon_scaled_force_values :
    commonForceMagnitude actualEarthMoonScaledWitness = 36 ∧
    forceOnAByB actualEarthMoonScaledWitness = -36 ∧
    forceOnBByA actualEarthMoonScaledWitness = 36 ∧
    equalAndOppositeForces actualEarthMoonScaledWitness := by
  simp [actualEarthMoonScaledWitness, commonForceMagnitude, forceOnAByB,
    forceOnBByA, equalAndOppositeForces]

theorem actual_balanced_unit_force_values :
    commonForceMagnitude actualBalancedUnitWitness = 30 ∧
    forceOnAByB actualBalancedUnitWitness = -30 ∧
    forceOnBByA actualBalancedUnitWitness = 30 ∧
    equalAndOppositeForces actualBalancedUnitWitness := by
  simp [actualBalancedUnitWitness, commonForceMagnitude, forceOnAByB,
    forceOnBByA, equalAndOppositeForces]

end Chronos.Frontier.NewtonianEqualOppositeGravityForceActualValueTest
