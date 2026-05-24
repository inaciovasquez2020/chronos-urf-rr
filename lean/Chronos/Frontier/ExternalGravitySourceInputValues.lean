import Mathlib

namespace Chronos
namespace Frontier
namespace ExternalGravityInputValues

def blackHoleShadowBoundRatioSquared : Rat := 27 / 4
def blackHoleShadowTestRatioSquared : Rat := 27 / 4

def blackHoleShadowInputGate : Prop :=
  blackHoleShadowBoundRatioSquared <= blackHoleShadowTestRatioSquared

theorem blackHoleShadowInputGate_closed :
    blackHoleShadowInputGate := by
  norm_num [
    blackHoleShadowInputGate,
    blackHoleShadowBoundRatioSquared,
    blackHoleShadowTestRatioSquared
  ]

def actKSZObservedExponentCentral : Rat := 21 / 10
def actKSZObservedExponentTolerance : Rat := 3 / 10
def actKSZTargetExponent : Rat := 2

def actKSZLowerExponent : Rat :=
  actKSZObservedExponentCentral - actKSZObservedExponentTolerance

def actKSZUpperExponent : Rat :=
  actKSZObservedExponentCentral + actKSZObservedExponentTolerance

def actKSZInputGate : Prop :=
  actKSZLowerExponent <= actKSZTargetExponent /\
  actKSZTargetExponent <= actKSZUpperExponent

theorem actKSZInputGate_closed :
    actKSZInputGate := by
  norm_num [
    actKSZInputGate,
    actKSZLowerExponent,
    actKSZUpperExponent,
    actKSZObservedExponentCentral,
    actKSZObservedExponentTolerance,
    actKSZTargetExponent
  ]

structure ExternalGravityInputValue where
  label : String
  value : String
  role : String
deriving Repr, BEq

def inputValues : List ExternalGravityInputValue :=
  [
    { label := "black_hole_shadow_bound_ratio_squared", value := "27/4", role := "minimum admissible squared shadow-to-horizon ratio" },
    { label := "black_hole_shadow_test_ratio_squared", value := "27/4", role := "saturation test value" },
    { label := "act_ksz_observed_exponent_central", value := "21/10", role := "reported central exponent value" },
    { label := "act_ksz_observed_exponent_tolerance", value := "3/10", role := "reported one-sigma tolerance" },
    { label := "act_ksz_target_exponent", value := "2", role := "Newton-Einstein inverse-square target" },
    { label := "finsler_friedmann_numeric_gate", value := "none", role := "analogy-only source; no numeric gate admitted" }
  ]

def status : String :=
  "INPUT_VALUES_ONLY_NOT_THEOREM_INPUT"

end ExternalGravityInputValues
end Frontier
end Chronos
