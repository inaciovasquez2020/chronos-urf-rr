import Mathlib.Tactic

namespace Chronos
namespace Frontier

/--
Shared native carrier introduced to remove full independence between R1/R2/R3 models.

This is the first non-trivial coupling layer: all three semantics now act on a
single underlying carrier type.
-/
structure SharedCarrier where
  α : Type
  inst : DecidableEq α

/--
R1 structure now references the shared carrier.
-/
structure SharedR1 where
  carrier : SharedCarrier

/--
R2 structure now references the shared carrier.
-/
structure SharedR2 where
  carrier : SharedCarrier

/--
R3 structure now references the shared carrier.
-/
structure SharedR3 where
  carrier : SharedCarrier

/--
Coupled binding: R1/R2/R3 must share the same carrier instance.
-/
structure SharedR1R2R3Binding where
  C : SharedCarrier
  r1 : SharedR1
  r2 : SharedR2
  r3 : SharedR3
  r1_ok : r1.carrier = C
  r2_ok : r2.carrier = C
  r3_ok : r3.carrier = C

theorem shared_carrier_well_formed (B : SharedR1R2R3Binding) :
    B.r1.carrier = B.r2.carrier ∧ B.r2.carrier = B.r3.carrier := by
  constructor
  · exact Eq.trans B.r1_ok (Eq.symm B.r2_ok)
  · exact Eq.trans B.r2_ok (Eq.symm B.r3_ok)

end Frontier
end Chronos
