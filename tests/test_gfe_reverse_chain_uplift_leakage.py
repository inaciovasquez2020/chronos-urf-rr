from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools/gfe/certify_gfe_reverse_chain_uplift_leakage.py"


def test_reverse_chain_uplift_leading_leakage(tmp_path):
    output = tmp_path / "reverse_chain_uplift.json"

    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--output", str(output)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    stdout = result.stdout
    assert "AUGMENTED_GRAPH_IDENTITY := exact" in stdout
    assert "NORMALIZED_LEAKAGE_MAGNITUDE_GT := 2/15" in stdout
    assert (
        "RESULT := nonzero Fredholm obstruction becomes a "
        "uniformly nonzero resonant fast-mode source"
    ) in stdout

    data = json.loads(output.read_text(encoding="utf-8"))

    assert data["program"] == "GfE Reverse-Chain Uplift"
    assert data["uplift"]["ansatz"] == "Q = p P + alpha r"
    assert data["inner_crossing_mode"]["pairing_abs_sq"]["nonzero"] is True
    assert data["leading_leakage"]["normalized_source_magnitude_gt"] == "2/15"
    assert data["leading_leakage"]["uniformly_nonzero"] is True
    assert "global invariant manifold not yet proved" in data["boundary"]
    assert "projected 220 QNM/tail transfer remains prohibited" in data["boundary"]
