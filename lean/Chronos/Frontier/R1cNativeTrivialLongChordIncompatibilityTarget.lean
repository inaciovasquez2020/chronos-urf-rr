import Chronos.Frontier.R1cNativeTrivialLongChordContradictionTarget

namespace Chronos
namespace Frontier

/--
Native incompatibility target for the final R1c trivial-long-chord contradiction.

This surface isolates a still weaker proof object than the contradiction target:
a compatibility invariant together with an incompatibility theorem saying that
the invariant rules out a trivial long chord across the maximal diameter.
-/
structure R1cNativeTrivialLongChordIncompatibilityTarget where
  trivialLongChordAcrossMaximalDiameter : Prop
  maximalDiameterCompatibility : Prop
  compatibility : maximalDiameterCompatibility
  incompatibility :
    maximalDiameterCompatibility →
      trivialLongChordAcrossMaximalDiameter → False

/--
The explicit incompatibility certificate gives the contradiction proof required
by the previous R1c target.
-/
theorem R1c_trivialLongChordContradiction_from_incompatibility_target
    (T : R1cNativeTrivialLongChordIncompatibilityTarget) :
    T.trivialLongChordAcrossMaximalDiameter → False :=
  T.incompatibility T.compatibility

/--
The incompatibility target feeds the existing contradiction target.

The exported no-trivial proposition is chosen to be the negation of the
trivial-long-chord proposition itself, so no additional semantic closure is
hidden in this bridge.
-/
def r1c_trivial_long_chord_contradiction_target_from_incompatibility_target
    (T : R1cNativeTrivialLongChordIncompatibilityTarget) :
    R1cNativeTrivialLongChordContradictionTarget where
  trivialLongChordAcrossMaximalDiameter :=
    T.trivialLongChordAcrossMaximalDiameter
  noTrivialLongChordAcrossMaximalDiameter :=
    T.trivialLongChordAcrossMaximalDiameter → False
  contradiction :=
    R1c_trivialLongChordContradiction_from_incompatibility_target T
  noTrivial_from_contradiction :=
    fun h => h

end Frontier
end Chronos
