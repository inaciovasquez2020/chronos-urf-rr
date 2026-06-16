import Chronos.Frontier.R1R2R3SemanticTheoremProofTargets
import Chronos.Frontier.R1RestrictedLongChordSafeAdmissibility

namespace Chronos
namespace Frontier

/--
A concrete safe native endpoint for the restricted R1 semantic instance.
-/
def R1ConcreteNativeSafeEndpoint : LongChordEndpoint :=
  { id := 0 }

/--
A concrete safe metric datum.  It carries no long-chord witness because all
three distances are zero.
-/
def R1ConcreteNativeSafeMetricDatum : LongChordMetricDatum :=
  { ambientDistance := 0
    chordLength := 0
    localityRadius := 0 }

/--
A concrete native object used as the distinguished semantic edge endpoints.
-/
def R1ConcreteNativeSafeObject : LongChordNativeObject :=
  { leftEndpoint := R1ConcreteNativeSafeEndpoint
    rightEndpoint := R1ConcreteNativeSafeEndpoint
    metric := R1ConcreteNativeSafeMetricDatum }

/--
The concrete safe native object is admissible for the restricted R1 repair.
-/
theorem R1ConcreteNativeSafeObject_admissible :
    R1LongChordSafeNativeAdmissible R1ConcreteNativeSafeObject := by
  intro hWitness
  exact Nat.not_lt_zero _ hWitness.left

/--
Concrete R1 semantic data restricted to safe native objects.

This avoids the refuted unrestricted predicate
`RepositoryNativeR1LongChordCoherence`; trivial words/faces and support are
indexed by `R1LongChordSafeNativeAdmissible`.
-/
def R1ConcreteNativeSafeSemanticData : R1SemanticData where
  Word := LongChordNativeObject
  Edge := LongChordNativeObject
  Face := LongChordNativeObject
  e1 := R1ConcreteNativeSafeObject
  e2 := R1ConcreteNativeSafeObject
  TrivWord := R1LongChordSafeNativeAdmissible
  TrivFace := R1LongChordSafeNativeAdmissible
  WordSupport := fun w e =>
    R1LongChordSafeNativeAdmissible w ∧
      w = e ∧
        e ≠ R1ConcreteNativeSafeObject ∧
          e ≠ R1ConcreteNativeSafeObject
  FaceBoundarySupport := fun f e =>
    R1LongChordSafeNativeAdmissible f ∧
      f = e ∧
        e ≠ R1ConcreteNativeSafeObject ∧
          e ≠ R1ConcreteNativeSafeObject

/--
For the concrete safe semantic instance, trivial word support comes from a
trivial face boundary by choosing the word itself as the face.
-/
theorem R1ConcreteNativeSafeSemanticData_R1b :
    ∀ word edge,
      R1ConcreteNativeSafeSemanticData.TrivWord word →
      R1ConcreteNativeSafeSemanticData.WordSupport word edge →
        ∃ face,
          R1ConcreteNativeSafeSemanticData.TrivFace face ∧
            R1ConcreteNativeSafeSemanticData.FaceBoundarySupport face edge := by
  intro word edge hword hsupport
  exact ⟨word, hword, hsupport⟩

/--
For the concrete safe semantic instance, the distinguished endpoints are
excluded from face-boundary support.
-/
theorem R1ConcreteNativeSafeSemanticData_R1a :
    ∀ face, R1ConcreteNativeSafeSemanticData.TrivFace face →
      ¬ R1ConcreteNativeSafeSemanticData.FaceBoundarySupport
          face R1ConcreteNativeSafeSemanticData.e1 ∧
      ¬ R1ConcreteNativeSafeSemanticData.FaceBoundarySupport
          face R1ConcreteNativeSafeSemanticData.e2 := by
  intro face _hface
  constructor
  · intro hsupport
    exact hsupport.2.2.1 rfl
  · intro hsupport
    exact hsupport.2.2.2 rfl

end Frontier
end Chronos
