#!/usr/bin/env python3
from pathlib import Path
import sys

path = Path("lean/Chronos/Frontier/SecularVanishingPolynomialInputSurface.lean")
text = path.read_text()

required = [
    "inductive ChronosSemanticDerivationRules",
    "| constant (n : Nat)",
    "| variable (n : Nat)",
    "| add {p q : ChronosSemanticPolynomialSyntax}",
    "| mul {p q : ChronosSemanticPolynomialSyntax}",
    "structure ChronosSemanticDerivationObject",
    "chronosSemanticDerivedVariableZero",
    "chronosSemanticDerivationRules_preserve_nonSemanticSVPBoundary",
    "missing_everywhere_vanishing",
    "chronosEvaluationSpecificSoundnessBoundary_preserves_nonSemanticSVPBoundary",
    "chronosEvaluationSpecificSoundnessBoundary",
    "ChronosEvaluationSpecificSoundnessBoundary",
    "admissible : Nat → Prop",
    "vanishes_on_admissible",
    "chronosPositiveEvaluationSpecificSoundnessInputSurface_preserves_nonSemanticSVPBoundary",
    "chronosPositiveEvaluationSpecificSoundnessInputSurface",
    "ChronosPositiveEvaluationSpecificSoundnessInputSurface",
    "witness_nonzero",
    "chronosNondegenerateEvaluationWitnessSurface_preserves_nonSemanticSVPBoundary",
    "chronosNondegenerateEvaluationWitnessSurface",
    "ChronosNondegenerateEvaluationWitnessSurface",
    "chronosSamePolynomialSyntacticNonzeroSurface_preserves_nonSemanticSVPBoundary",
    "same_polynomial_nonzero",
    "chronosSamePolynomialSyntacticNonzeroSurface",
    "ChronosSamePolynomialSyntacticNonzeroSurface",
    "chronosSemanticPolynomialSyntaxZero",
    "chronosNondegenerateEvaluation",
]

missing = [item for item in required if item not in text]
if missing:
    print("MISSING_OBJECT := " + missing[0])
    sys.exit(1)

start = text.index("inductive ChronosSemanticDerivationRules")
section = text[start:text.index("structure ChronosSemanticPolynomialInterface", start)]

forbidden = [
    "sorry",
    "admit",
    "axiom",
    "opaque",
    "derives_vanishing",
    "SemanticChronosSVPSolved",
    "semanticChronosSVPSolved",
    "SEMANTIC_CHRONOS_SVP_SOLVED",
]

bad = [item for item in forbidden if item in section]
if bad:
    print("MISSING_OBJECT := boundary_preserving_derivation_rules_without_" + bad[0])
    sys.exit(1)

print("CHRONOS_SEMANTIC_DERIVATION_RULES_BOUNDARY_OK")
