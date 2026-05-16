from pathlib import Path
import json

lean = Path("lean/Chronos/Frontier/BoundaryNuclearityFromFiniteDetectorAlgebra.lean").read_text()
doc = Path("docs/status/BOUNDARY_NUCLEARITY_FROM_FINITE_DETECTOR_ALGEBRA_2026_05_16.md").read_text()
artifact = json.loads(Path("artifacts/chronos/boundary_nuclearity_from_finite_detector_algebra_2026_05_16.json").read_text())
status_text = "\n".join(p.read_text() for p in Path("docs/status").glob("*.md") if "BulkToBoundaryNuclearitySoundness" in p.read_text())

required_lean = [
    "def FiniteDetectorAlgebra",
    "def BoundaryNuclearityFromFiniteDetectorAlgebra : Prop",
    "BulkToBoundaryNuclearitySoundness",
    "theorem boundary_nuclearity_from_finite_detector_algebra_implies_bulk_to_boundary_nuclearity_soundness",
]

for phrase in required_lean:
    assert phrase in lean, phrase

assert "axiom " not in lean
assert artifact["status"] == "FRONTIER_OPEN"
assert artifact["conditional_bridge"] == "boundary_nuclearity_from_finite_detector_algebra_implies_bulk_to_boundary_nuclearity_soundness"

required_doc = [
    "Status: FRONTIER_OPEN",
    "conditional bridge only",
    "BulkToBoundaryNuclearitySoundness",
    "It does not establish:",
    "unrestricted `UniversalBoundaryCompactness`",
    "unrestricted `QL_CollapseGate`",
    "Cosmic Censorship",
    "the Hoop Conjecture",
]

for phrase in required_doc:
    assert phrase in doc, phrase

assert "BulkToBoundaryNuclearitySoundness" in status_text
assert "BoundaryNuclearityFromFiniteDetectorAlgebra" in status_text

combined = "\n".join([
    lean,
    doc,
    status_text,
    json.dumps(artifact, sort_keys=True),
]).lower()

forbidden = [
    "finite detector algebra proves unrestricted collapse closure",
    "proves bulk-to-boundary nuclearity soundness",
    "proves unrestricted universalboundarycompactness",
    "proves unrestricted ql_collapsegate",
    "proves cosmic censorship",
    "proves the hoop conjecture",
    "solves cosmic censorship",
    "solves the hoop conjecture",
    "solves p vs np",
    "solves a clay problem",
]

for token in forbidden:
    assert token.lower() not in combined, token

print("Boundary nuclearity from finite detector algebra frontier verified.")
