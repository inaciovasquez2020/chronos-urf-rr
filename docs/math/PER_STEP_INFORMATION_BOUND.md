
# Per-Step Information Bound

Status: OPEN

## Weakest sufficient remaining lemma

For the Newstein refinement chain, each admissible step leaks at most the allowed constant-order information into the transcript.

Formal target:
For every admissible refinement step s,
info_leakage(s) <= V_C.

## Role in closure

This is the exact remaining information-side bound needed to complete the quotient-gap assembly after the geometric and quotient-injection steps.

## Dependencies

* admissible transcript model
* stepwise leakage functional
* uniform bound argument
* compatibility with the Newstein quotient chain
  EOF
  cat > tests/test_per_step_info_bound_lock.py <<'EOF'
  from pathlib import Path
  import json

def test_per_step_info_bound_doc_lock():
text = Path("docs/math/PER_STEP_INFORMATION_BOUND.md").read_text()
assert "Status: OPEN" in text
assert "info_leakage(s) <= V_C." in text
assert "remaining information-side bound" in text
assert "Per-Step Information Bound" in text

def test_info_leakage_artifact_lock():
data = json.loads(Path("artifacts/info_leakage_stats.json").read_text())
assert data["project"] == "chronos-urf-rr"
assert data["metric"] == "InformationLeakage"
assert data["status"] == "awaiting_verification"
assert "theoretical_max" in data["bounds"]
