import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/high_girth_lift.json"


def test_high_girth_lift_generation_preserves_tracked_artifact():
    before = ARTIFACT.read_text(encoding="utf-8") if ARTIFACT.exists() else None

    try:
        subprocess.run(
            [sys.executable, "scripts/generate_high_girth_lift.py"],
            cwd=ROOT,
            check=True,
        )
        assert ARTIFACT.exists()
    finally:
        if before is None:
            ARTIFACT.unlink(missing_ok=True)
        else:
            ARTIFACT.write_text(before, encoding="utf-8")
