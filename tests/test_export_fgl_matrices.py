import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_export_fgl_matrices_fails_without_source_file():
    srcs = [
        ROOT / "artifacts/fgl/source_matrices.json",
        ROOT / "data/fgl/source_matrices.json",
        ROOT / "docs/data/fgl/source_matrices.json",
    ]
    backups = []
    for src in srcs:
        if src.exists():
            backup = src.with_suffix(src.suffix + ".bak_test")
            src.rename(backup)
            backups.append((src, backup))
    try:
        p = subprocess.run(
            [sys.executable, str(ROOT / "tools/export_fgl_matrices.py")],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        assert p.returncode == 2
        assert "MISSING: source matrix file" in p.stderr
    finally:
        for src, backup in backups:
            backup.rename(src)
