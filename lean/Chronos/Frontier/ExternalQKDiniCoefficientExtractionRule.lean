import Chronos.Frontier.ExternalQKDiniFormulaExtractionTarget

namespace Chronos
namespace Frontier

structure ExternalQKDiniCoefficientExtractionRuleData where
  sourceId : String
  sourceFormulaName : String
  coefficientSymbol : String
  extractedRule : String
  nativeCodomainDecision : String
  natCodomainStatus : String
  nonzeroWitnessStatus : String
  uniformBoundStatus : String
  boundary : String

def ExternalQKDiniCoefficientExtractionRule :
    ExternalQKDiniCoefficientExtractionRuleData where
  sourceId := "DOI:10.1155/2022/8496249"
  sourceFormulaName := "normalized q-generalized Dini function"
  coefficientSymbol := "zeta_n"
  extractedRule :=
    "zeta_n = ((-c)^n * (a + 2*n)) / (a * 4^n * (q;q)_n * (q^k;q)_n)"
  nativeCodomainDecision :=
    "parameterized analytic scalar coefficient; not intrinsically Nat"
  natCodomainStatus :=
    "NO_NAT_RULE_WITHOUT_DISCRETIZATION_OR_ABSOLUTE_VALUE_ENCODING"
  nonzeroWitnessStatus :=
    "MISSING_PARAMETER_ASSUMPTIONS_FOR_NONZERO_SOURCE_WITNESS"
  uniformBoundStatus :=
    "MISSING_PARAMETER_RESTRICTED_UNIFORM_BOUND_THEOREM"
  boundary :=
    "COEFFICIENT_EXTRACTION_RULE_RECORDED_ONLY_NO_NONZERO_OR_BOUND_PROOF"

theorem externalQKDiniCoefficientExtractionRule_source_id :
    ExternalQKDiniCoefficientExtractionRule.sourceId =
      "DOI:10.1155/2022/8496249" :=
  rfl

theorem externalQKDiniCoefficientExtractionRule_symbol :
    ExternalQKDiniCoefficientExtractionRule.coefficientSymbol =
      "zeta_n" :=
  rfl

theorem externalQKDiniCoefficientExtractionRule_nat_obstruction :
    ExternalQKDiniCoefficientExtractionRule.natCodomainStatus =
      "NO_NAT_RULE_WITHOUT_DISCRETIZATION_OR_ABSOLUTE_VALUE_ENCODING" :=
  rfl

theorem externalQKDiniCoefficientExtractionRule_uniform_bound_missing :
    ExternalQKDiniCoefficientExtractionRule.uniformBoundStatus =
      "MISSING_PARAMETER_RESTRICTED_UNIFORM_BOUND_THEOREM" :=
  rfl

def ExternalQKDiniCoefficientExtractionRuleStatus : String :=
  "COEFFICIENT_EXTRACTION_RULE_RECORDED_ONLY"

end Frontier
end Chronos
