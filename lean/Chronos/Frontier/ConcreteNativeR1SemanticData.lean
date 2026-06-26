import Mathlib.Tactic
import Chronos.Frontier.NewsteinR1R2R3NativeBindingSpec

namespace Chronos
namespace Frontier

/--
Concrete repository-native R1 word object.

The unique word is trivial and has no support on either native long-chord edge.
-/
inductive ConcreteNativeR1Word where
  | unit
deriving DecidableEq

/-- Concrete repository-native R1 edge object with two distinguished endpoints. -/
inductive ConcreteNativeR1Edge where
  | e1
  | e2
deriving DecidableEq

/-- Concrete repository-native R1 face object. -/
inductive ConcreteNativeR1Face where
  | unit
deriving DecidableEq

def concreteNativeR1TrivWord (_word : ConcreteNativeR1Word) : Prop := True

def concreteNativeR1TrivFace (_face : ConcreteNativeR1Face) : Prop := True

def concreteNativeR1WordSupport
    (_word : ConcreteNativeR1Word)
    (_edge : ConcreteNativeR1Edge) : Prop :=
  False

def concreteNativeR1FaceBoundarySupport
    (_face : ConcreteNativeR1Face)
    (_edge : ConcreteNativeR1Edge) : Prop :=
  False

/--
Concrete repository-native R1 semantic data.

This realizes explicit `Word`, `Edge`, `Face`, `TrivWord`, `TrivFace`,
`WordSupport`, and `FaceBoundarySupport` data inside the existing
`R1SemanticData` interface.
-/
def concreteNativeR1SemanticData : R1SemanticData where
  Word := ConcreteNativeR1Word
  Edge := ConcreteNativeR1Edge
  Face := ConcreteNativeR1Face
  e1 := ConcreteNativeR1Edge.e1
  e2 := ConcreteNativeR1Edge.e2
  TrivWord := concreteNativeR1TrivWord
  TrivFace := concreteNativeR1TrivFace
  WordSupport := concreteNativeR1WordSupport
  FaceBoundarySupport := concreteNativeR1FaceBoundarySupport

theorem concrete_native_r1_correct :
    R1LongChordExclusionTheorem concreteNativeR1SemanticData := by
  intro word hword
  constructor
  · intro hsupport
    exact hsupport
  · intro hsupport
    exact hsupport

/--
A binding spec is connected to the concrete native R1 construction when its R1
semantic data is exactly the concrete native R1 semantic data.
-/
def NewsteinBindingUsesConcreteNativeR1
    (S : NewsteinR1R2R3NativeBindingSpec) : Prop :=
  S.nativeR1Data = concreteNativeR1SemanticData

theorem newstein_binding_concrete_native_r1_correct
    (S : NewsteinR1R2R3NativeBindingSpec)
    (h : NewsteinBindingUsesConcreteNativeR1 S) :
    R1LongChordExclusionTheorem S.nativeR1Data := by
  rw [h]
  exact concrete_native_r1_correct

end Frontier
end Chronos
