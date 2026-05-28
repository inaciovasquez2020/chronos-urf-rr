import json
from pathlib import Path

ART = Path("artifacts/chronos/gdm_empirical_mass_map_binding_theorem_2026_05_28.json")
DOC = Path("docs/status/GDM_EMPIRICAL_MASS_MAP_BINDING_THEOREM_2026_05_28.md")
LEAN = Path("lean/Chronos/Frontier/GDMEmpiricalMassMapBindingTheorem.lean")

required = [
    "empirical validation",
    "Lambda-CDM failure",
    "dark matter replacement",
    "dark matter phase claim",
    "gravity closure",
    "unrestricted Chronos-RR",
    "unrestricted H4.1/FGL",
    "P vs NP",
    "Clay problem",
]

data = json.loads(ART.read_text())
doc = DOC.read_text()
lean = LEAN.read_text()

assert data["status"] == "EMPIRICAL_BINDING_OBLIGATION_INTERFACE_ONLY"
for token in required:
    assert token in doc
    assert token in data["does_not_prove"]
for token in [
    "empirical_mass_map_binding_from_obligation",
    "zero_residual_under_identical_masses",
]:
    assert token in lean

print("GDM_EMPIRICAL_MASS_MAP_BINDING_THEOREM_OK")
