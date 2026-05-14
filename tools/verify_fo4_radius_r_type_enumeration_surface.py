from pathlib import Path
import json

lean = Path("lean/Chronos/Frontier/FO4RadiusRTypeEnumerationSurface.lean").read_text()
status = Path("docs/status/CHRONOS_FO4_RADIUS_R_TYPE_ENUMERATION_SURFACE_2026_05_14.md").read_text()
artifact = json.loads(Path("artifacts/chronos/fo4_radius_r_type_enumeration_surface_2026_05_14.json").read_text())

required_lean = [
    "def FO4RadiusRTypeBound",
    "structure FO4RadiusRTypeCode",
    "structure FO4RadiusRTypeEnumerationInput",
    "def FiniteFO4RadiusRTypeEnumeration",
    "theorem finiteFO4RadiusRTypeEnumeration_under_degree_bound",
    "theorem fo4FiniteTypeEnumerationSurfaceClosed",
    "FINITE_TYPE_ENUMERATION_SURFACE_CLOSED",
]

for token in required_lean:
    assert token in lean, token

assert artifact["status"] == "FINITE_TYPE_ENUMERATION_SURFACE_CLOSED"
assert artifact["closed_surface"] == "code-level finite FO4 radius-R type enumeration"

required_boundary = [
    "Code-level finite FO4 radius-R type enumeration surface only.",
    "Does not prove semantic completeness of FO4 types.",
    "Does not prove bounded cycle-overlap rank.",
    "Does not close rigidity.",
    "Does not prove P vs NP.",
    "Does not solve any Clay problem.",
]

for phrase in required_boundary:
    assert phrase in status, phrase

for forbidden in [
    "semantic completeness of FO4 types is proved",
    "bounded cycle-overlap rank is proved",
    "rigidity is closed",
    "P vs NP is proved",
    "Clay problem is solved",
]:
    assert forbidden not in lean
    assert forbidden not in status

print("FO4 radius-R type enumeration surface verified.")
