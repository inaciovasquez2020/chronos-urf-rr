import Chronos.Frontier.R1R2R3PromotionObstructionFrontierLock

namespace Chronos
namespace Frontier

/--
Native endpoint object for the R1 long-chord layer.
This is deliberately finite and repository-native: endpoints are represented by
stable natural-number identifiers inside the finite-data/native-binding surface.
-/
structure LongChordEndpoint where
  id : Nat
deriving Repr, DecidableEq

/--
The exact metric datum used by the R1 long-chord obstruction layer.
`ambientDistance` is the native path distance between endpoints.
`chordLength` is the proposed shortcut/chord length.
`localityRadius` is the allowed local radius.
-/
structure LongChordMetricDatum where
  ambientDistance : Nat
  chordLength : Nat
  localityRadius : Nat
deriving Repr, DecidableEq

/--
The exact native object appearing in the repository-native LongChordExclusion layer.
-/
structure LongChordNativeObject where
  leftEndpoint : LongChordEndpoint
  rightEndpoint : LongChordEndpoint
  metric : LongChordMetricDatum
deriving Repr, DecidableEq

/--
A long-chord witness says the chord lies outside the allowed locality radius
while still shortcutting the ambient native distance.
-/
def LongChordWitness (x : LongChordNativeObject) : Prop :=
  x.metric.localityRadius < x.metric.chordLength ∧
    x.metric.chordLength < x.metric.ambientDistance

/--
Native long-chord coherence says the ambient native distance is already bounded
by the locality radius. Under this invariant, a long-chord witness is impossible.
-/
def NativeLongChordCoherence (x : LongChordNativeObject) : Prop :=
  x.metric.ambientDistance <= x.metric.localityRadius

theorem long_chord_witness_contradiction
    (x : LongChordNativeObject)
    (hWitness : LongChordWitness x)
    (hCoherent : NativeLongChordCoherence x) :
    False :=
  by
    rcases hWitness with ⟨hRadiusLtChord, hChordLtAmbient⟩
    have hChordLtRadius :
        x.metric.chordLength < x.metric.localityRadius :=
      Nat.lt_of_lt_of_le hChordLtAmbient hCoherent
    exact Nat.not_lt_of_ge (Nat.le_of_lt hChordLtRadius) hRadiusLtChord

/--
Native diameter/filling datum for R2.
`sourceDiameter` is the pre-filling diameter scale.
`targetDiameter` is the post-filling visible diameter scale.
`fillingCost` is the amount of diameter paid by an admissible filling.
`separationFloor` is the separation lower bound that must survive filling.
-/
structure DiameterFillingNativeObject where
  sourceDiameter : Nat
  targetDiameter : Nat
  fillingCost : Nat
  separationFloor : Nat
deriving Repr, DecidableEq

/--
Diameter/filling compatibility invariant.
The separation floor is below the source diameter, and the source diameter is
bounded by target diameter plus filling cost.
-/
def DiameterFillingCompatibility (x : DiameterFillingNativeObject) : Prop :=
  x.separationFloor <= x.sourceDiameter ∧
    x.sourceDiameter <= x.targetDiameter + x.fillingCost

theorem monotone_separation_lower_bound
    (x : DiameterFillingNativeObject)
    (hCompat : DiameterFillingCompatibility x) :
    x.separationFloor <= x.targetDiameter + x.fillingCost :=
  by
    exact Nat.le_trans hCompat.left hCompat.right

/--
Native local-type capacity datum for R3.
`localTypeCount` is the number of local types admitted by the native object.
-/
structure LocalTypeCapacityNativeObject where
  localTypeCount : Nat
deriving Repr, DecidableEq

/-- Explicit uniform local-type capacity bound C. -/
def ExplicitLocalTypeCapacityC : Nat :=
  4096

def WithinExplicitLocalTypeCapacity
    (x : LocalTypeCapacityNativeObject) : Prop :=
  x.localTypeCount <= ExplicitLocalTypeCapacityC

theorem explicit_local_type_capacity_bound_positive :
    0 < ExplicitLocalTypeCapacityC :=
  by
    decide

theorem local_type_capacity_bound_certificate
    (x : LocalTypeCapacityNativeObject)
    (hBound : x.localTypeCount <= ExplicitLocalTypeCapacityC) :
    WithinExplicitLocalTypeCapacity x :=
  by
    exact hBound

/--
Combined ingredient packet requested before attempting obstruction elimination.
This does not prove the R1/R2/R3 promotion targets; it provides the native
objects and first contradiction/lower-bound/capacity ingredients.
-/
def NativeLongChordDiameterCapacityIngredientPacket : Prop :=
  True

theorem native_long_chord_diameter_capacity_ingredient_packet :
    NativeLongChordDiameterCapacityIngredientPacket :=
  by
    trivial

end Frontier
end Chronos
