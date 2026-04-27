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
    generated = [
        ROOT / "artifacts/fgl/finite_patch_matrices.json",
        ROOT / "docs/status/FGL_MATRIX_EXPORT_STATUS_2026_04_27.md",
    ]

    backups = []
    generated_snapshots = {}

    for path in generated:
        if path.exists():
            generated_snapshots[path] = path.read_text(encoding="utf-8")
        else:
            generated_snapshots[path] = None

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

        for path, snapshot in generated_snapshots.items():
            if snapshot is None:
                path.unlink(missing_ok=True)
            else:
                path.write_text(snapshot, encoding="utf-8")
