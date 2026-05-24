import Mathlib

namespace Chronos
namespace Frontier
namespace ExternalGravitySourceMathematicalTest

def blackHoleShadowSquaredLowerBound : Rat := 27 / 4

def actKSZCentralExponent : Rat := 21 / 10

def actKSZOneSigmaTolerance : Rat := 3 / 10

def inClosedInterval (x lo hi : Rat) : Prop :=
  lo <= x /\ x <= hi

def actKSZInverseSquareMathGate : Prop :=
  inClosedInterval 2
    (actKSZCentralExponent - actKSZOneSigmaTolerance)
    (actKSZCentralExponent + actKSZOneSigmaTolerance)

theorem actKSZInverseSquareMathGate_closed :
    actKSZInverseSquareMathGate := by
  norm_num [
    actKSZInverseSquareMathGate,
    inClosedInterval,
    actKSZCentralExponent,
    actKSZOneSigmaTolerance
  ]

def shadowRatioSquaredGate (shadowRatioSquared : Rat) : Prop :=
  blackHoleShadowSquaredLowerBound <= shadowRatioSquared

theorem blackHoleShadowLowerBoundSaturationGate_closed :
    shadowRatioSquaredGate (27 / 4) := by
  norm_num [shadowRatioSquaredGate, blackHoleShadowSquaredLowerBound]

structure ExternalGravitySourceRecord where
  sourceId : String
  sourceUrl : String
  mathematicalRole : String
  admissibleUse : String
  boundary : String
deriving Repr, BEq

def blackHoleShadowLowerBoundSource : ExternalGravitySourceRecord :=
  {
    sourceId := "APS_PRD_BLACK_HOLE_SHADOW_LOWER_BOUND"
    sourceUrl := "https://journals.aps.org/prd/abstract/10.1103/83t3-r7j2"
    mathematicalRole := "shadow ratio squared lower-bound gate: (r_sh/r_H)^2 >= 27/4"
    admissibleUse := "source-backed gravity-bound map"
    boundary := "not theorem input; not gravity closure"
  }

def actKSZInverseSquareGravitySource : ExternalGravitySourceRecord :=
  {
    sourceId := "ACT_KSZ_INVERSE_SQUARE_GRAVITY_CONSTRAINT"
    sourceUrl := "https://okdiario.com/techy/en/einstein-and-newton-just-survived-a-huge-cosmic-test-and-the-result-makes-dark-matter-harder-to-dismiss-than-ever/3664/"
    mathematicalRole := "one-sigma exponent gate: 2 in [2.1 - 0.3, 2.1 + 0.3]"
    admissibleUse := "external large-scale gravity constraint map"
    boundary := "not dark-matter detection; not DFM-MKC validation or refutation"
  }

def finslerFriedmannGeometrySource : ExternalGravitySourceRecord :=
  {
    sourceId := "FINSLER_FRIEDMANN_GEOMETRIC_ACCELERATION_ANALOGY"
    sourceUrl := "https://www.sciencedaily.com/releases/2026/01/260110211221.htm"
    mathematicalRole := "geometry-driven acceleration analogy only; no numeric gate admitted"
    admissibleUse := "source-backed geometric-cosmology analogy map"
    boundary := "not empirical validation; not dark-energy disproof"
  }

def sourceRecords : List ExternalGravitySourceRecord :=
  [
    blackHoleShadowLowerBoundSource,
    actKSZInverseSquareGravitySource,
    finslerFriedmannGeometrySource
  ]

def status : String :=
  "SOURCE_BACKED_MATHEMATICAL_TEST_ONLY_NOT_THEOREM_INPUT"

end ExternalGravitySourceMathematicalTest
end Frontier
end Chronos
