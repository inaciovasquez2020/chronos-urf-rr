from pathlib import Path
import json

lean = Path("lean/Chronos/Frontier/BulkToBoundaryNuclearitySoundness.lean").read_text()
doc = Path("docs/status/BULK_TO_BOUNDARY_NUCLEARITY_SOUNDNESS_2026_05_16.md").read_text()
artifact = json.loads(Path("artifacts/chronos/bulk_to_boundary_nuclearity_soundness_2026_05_16.json").read_text())

required_lean = [
    "def BoundaryNuclearity",
    "def BulkDeformationPushforwardCompact_wstar",
    "def BulkToBoundaryNuclearitySoundness : Prop",
    "theorem bulk_to_boundary_nuclearity_soundness_implies_unrestricted_boundary_compactness",
    "UnrestrictedUniversalBoundaryCompactness",
]

for phrase in required_lean:
    assert phrase in lean, phrase

assert artifact["status"] == "FRONTIER_OPEN"
assert artifact["conditional_bridge"] == "bulk_to_boundary_nuclearity_soundness_implies_unrestricted_boundary_compactness"

required_doc = [
    "Status: FRONTIER_OPEN",
    "conditional bridge only",
    "It does not establish:",
    "unrestricted `UniversalBoundaryCompactness`",
    "unrestricted `QL_CollapseGate`",
    "Cosmic Censorship",
    "the Hoop Conjecture",
]

for phrase in required_doc:
    assert phrase in doc, phrase

combined = "\n".join([
    lean,
    doc,
    json.dumps(artifact, sort_keys=True),
]).lower()

forbidden = [
    "nuclearity proves unrestricted collapse closure",
    "proves unrestricted universalboundarycompactness",
    "proves unrestricted ql_collapsegate",
    "proves cosmic censorship",
    "proves the hoop conjecture",
    "solves cosmic censorship",
    "solves the hoop conjecture",
    "solves p vs np",
    "solves a clay problem",
    "unrestricted collapse closure is proved",
]

for token in forbidden:
    assert token.lower() not in combined, token

print("Bulk-to-boundary nuclearity soundness frontier verified.")
