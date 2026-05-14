from pathlib import Path
import json

lean = Path("lean/Chronos/Frontier/FO4SemanticCompletenessSurface.lean").read_text()
status = Path("docs/status/CHRONOS_FO4_SEMANTIC_COMPLETENESS_SURFACE_2026_05_14.md").read_text()
artifact = json.loads(Path("artifacts/chronos/fo4_semantic_completeness_surface_2026_05_14.json").read_text())

required_lean = [
    "structure FO4RadiusRNeighborhood",
    "def BoundedDegreeRadiusRNeighborhood",
    "structure FO4SemanticTypeRealization",
    "def SemanticCompleteFO4RadiusRTypeCodes",
    "def FO4SemanticCompletenessHypothesis",
    "theorem semanticCompletenessSurface_from_hypothesis",
    "SEMANTIC_COMPLETENESS_INTERFACE_CLOSED_ONLY",
]

for token in required_lean:
    assert token in lean, token

assert artifact["status"] == "SEMANTIC_COMPLETENESS_INTERFACE_CLOSED_ONLY"
assert artifact["closed_surface"] == "semantic completeness interface for FO4 radius-R type codes"

required_boundary = [
    "Defines semantic completeness interface only.",
    "Does not prove semantic completeness from graph semantics.",
    "Does not prove ColapR rank control.",
    "Does not close rigidity.",
    "Does not prove P vs NP.",
    "Does not solve any Clay problem.",
]

for phrase in required_boundary:
    assert phrase in status, phrase

for forbidden in [
    "semantic completeness from graph semantics is proved",
    "ColapR rank control is proved",
    "bounded cycle-overlap rank is proved",
    "rigidity is closed",
    "P vs NP is proved",
    "Clay problem is solved",
]:
    assert forbidden not in lean
    assert forbidden not in status

print("FO4 semantic completeness surface verified.")
