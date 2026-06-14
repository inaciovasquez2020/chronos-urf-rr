#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

artifact = ROOT / "artifacts/chronos/chronos_bounded_closure_proof_pattern_sync_2026_06_14.json"
doc = ROOT / "docs/status/CHRONOS_BOUNDED_CLOSURE_PROOF_PATTERN_SYNC_2026_06_14.md"

closeout_artifact = ROOT / "artifacts/chronos/concrete_analytic_einstein_matter_estimate_package_closeout_stack_2026_05_23.json"
closeout_doc = ROOT / "docs/status/CONCRETE_ANALYTIC_EINSTEIN_MATTER_ESTIMATE_PACKAGE_CLOSEOUT_STACK_2026_05_23.md"
closeout_verifier = ROOT / "tools/verify_concrete_analytic_einstein_matter_estimate_package_closeout_stack.py"
closeout_test = ROOT / "tests/test_concrete_analytic_einstein_matter_estimate_package_closeout_stack.py"

required_dependency_artifacts = [
    "docs/status/CONCRETE_ANALYTIC_EINSTEIN_MATTER_ESTIMATE_PACKAGE_CLOSEOUT_STACK_2026_05_23.md",
    "artifacts/chronos/concrete_analytic_einstein_matter_estimate_package_closeout_stack_2026_05_23.json",
    "tools/verify_concrete_analytic_einstein_matter_estimate_package_closeout_stack.py",
    "tests/test_concrete_analytic_einstein_matter_estimate_package_closeout_stack.py",
]

required_status_classes = [
    "INPUT_SURFACE",
    "CONDITIONAL",
    "PROOF_SURFACE_ONLY",
    "OPEN_GLOBAL_FRONTIER",
]

required_pattern_components = [
    "large_claim",
    "input_surface",
    "proof_surface_or_bounded_object",
    "verifier_or_certificate",
    "status_classification",
    "explicit_boundary",
]

required_boundaries = [
    "bounded status sync only",
    "closeout stack only",
    "proof surfaces only",
    "no analytic Einstein-matter bootstrap package",
    "no concrete analytic Einstein-matter estimate package proof",
    "no unconditional restricted continuation norm theorem",
    "no threshold crossing proof",
    "no gravity closure",
    "no Chronos-RR",
    "no H4.1/FGL",
    "no P vs NP",
    "no Clay problem",
    "no theorem promotion",
]

for path in [artifact, doc, closeout_artifact, closeout_doc, closeout_verifier, closeout_test]:
    if not path.exists():
        raise SystemExit(f"missing {path}")

data = json.loads(artifact.read_text())
closeout = json.loads(closeout_artifact.read_text())
doc_text = doc.read_text()

assert data["name"] == "CHRONOS_BOUNDED_CLOSURE_PROOF_PATTERN_SYNC"
assert data["status"] == "BOUNDED_CLOSURE_PROOF_PATTERN_SYNC_ADDED"
assert data["source_pattern_repository"] == "urf-textbook"
assert data["source_pattern_commit"] == "8def1fc"
assert data["source_pattern_section"] == "Proof Pattern: Bounded Closure by Classified Formal Artifacts"
assert data["classifier_reference_repository"] == "theorem-closure-classifier"
assert data["classifier_reference_commit"] == "d9b6677"
assert data["dependency_surface"] == "CONCRETE_ANALYTIC_EINSTEIN_MATTER_ESTIMATE_PACKAGE_CLOSEOUT_STACK"
assert data["dependency_status"] == "BUILD_CLOSEOUT_SURFACE_ONLY_NO_ANALYTIC_PACKAGE_PROOF"
assert data["dependency_artifacts"] == required_dependency_artifacts
assert data["status_classes_used"] == required_status_classes
assert data["required_pattern_components"] == required_pattern_components
assert data["boundary"] == required_boundaries
assert data["next_admissible_object"] == "StopOrAddPatternSyncForAnotherChronosSurface"

assert closeout["name"] == "CONCRETE_ANALYTIC_EINSTEIN_MATTER_ESTIMATE_PACKAGE_CLOSEOUT_STACK"
assert closeout["status"] == "BUILD_CLOSEOUT_SURFACE_ONLY_NO_ANALYTIC_PACKAGE_PROOF"

for token in [
    "BOUNDED_CLOSURE_PROOF_PATTERN_SYNC_ADDED",
    "CONCRETE_ANALYTIC_EINSTEIN_MATTER_ESTIMATE_PACKAGE_CLOSEOUT_STACK",
    "BUILD_CLOSEOUT_SURFACE_ONLY_NO_ANALYTIC_PACKAGE_PROOF",
    "It does not prove an analytic Einstein-matter bootstrap package.",
    "It does not prove a concrete analytic Einstein-matter estimate package proof.",
    "It does not prove gravity closure.",
    "It does not prove Chronos-RR.",
    "It does not prove H4.1/FGL.",
    "It does not prove P vs NP.",
    "It does not prove any Clay problem.",
    "It does not promote any status artifact into theorem-level closure.",
]:
    assert token in doc_text

print("CHRONOS_BOUNDED_CLOSURE_PROOF_PATTERN_SYNC_OK")
