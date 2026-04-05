import Mathlib
import Chronos.Transcript
import Chronos.Z1

namespace Chronos

universe u v

def close_seeded {V : Type u} {E : Type v}
  (_T : EFTranscript V) : Cycle E :=
  { edges := [] }

end Chronos
