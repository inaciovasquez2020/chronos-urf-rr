import Chronos.Frontier.R1cNativeNoTrivialLongChordAcrossMaximalDiameterTarget

namespace Chronos
namespace Frontier

/--
Native contradiction target for the final R1c no-trivial-long-chord input.

This is an interface surface only. It isolates the weakest remaining proof
object: an explicit contradiction from the existence of a trivial long chord
across the maximal diameter.
-/
structure R1cNativeTrivialLongChordContradictionTarget where
  trivialLongChordAcrossMaximalDiameter : Prop
  noTrivialLongChordAcrossMaximalDiameter : Prop
  contradiction :
    trivialLongChordAcrossMaximalDiameter → False
  noTrivial_from_contradiction :
    (trivialLongChordAcrossMaximalDiameter → False) →
      noTrivialLongChordAcrossMaximalDiameter

/--
The no-trivial-long-chord fact follows from the native contradiction target.
-/
theorem R1c_noTrivialLongChordAcrossMaximalDiameter_from_contradiction_target
    (T : R1cNativeTrivialLongChordContradictionTarget) :
    T.noTrivialLongChordAcrossMaximalDiameter :=
  T.noTrivial_from_contradiction T.contradiction

/--
A contradiction target feeds the existing no-trivial-long-chord target while
keeping the actual contradiction proof explicit in the target object.
-/
def r1c_no_trivial_long_chord_target_from_contradiction_target
    (T : R1cNativeTrivialLongChordContradictionTarget) :
    R1cNativeNoTrivialLongChordAcrossMaximalDiameterTarget where
  trivialLongChordAcrossMaximalDiameter :=
    T.trivialLongChordAcrossMaximalDiameter
  noTrivialLongChordAcrossMaximalDiameter :=
    T.noTrivialLongChordAcrossMaximalDiameter
  excludesTrivialLongChordAcrossMaximalDiameter :=
    T.noTrivial_from_contradiction

end Frontier
end Chronos
