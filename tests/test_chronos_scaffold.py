from __future__ import annotations

import re
import subprocess
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=REPO,
        text=True,
        capture_output=True,
        check=False,
    )


def test_chronos_core_files_exist() -> None:
    required = [
        "lean/Chronos/Z1.lean",
        "lean/Chronos/ParityPair.lean",
        "lean/Chronos/Transcript.lean",
        "lean/Chronos/CloseSeeded.lean",
        "lean/Chronos/ParitySep.lean",
        "lean/Chronos/ParitySepProof.lean",
        "lean/Chronos/EP2Status.lean",
        "lean/Chronos/EP2Bundle.lean",
        "lean/Chronos/XorLemmas.lean",
        "lean/Chronos/XorTail.lean",
        "lean/Chronos/XorReduce.lean",
        "lean/Chronos/XorBool.lean",
        "lean/Chronos/XorNorm.lean",
    ]
    missing = [p for p in required if not (REPO / p).exists()]
    assert not missing, f"Missing required files: {missing}"


def test_ep2_bundle_file_compiles() -> None:
    proc = run(["lake", "env", "lean", "lean/Chronos/EP2Bundle.lean"])
    assert proc.returncode == 0, proc.stdout + "\n" + proc.stderr


def test_full_repo_builds() -> None:
    proc = run(["lake", "build"])
    assert proc.returncode == 0, proc.stdout + "\n" + proc.stderr


def test_single_remaining_axiom_in_chronos() -> None:
    proc = run(["grep", "-RIn", r"^[[:space:]]*axiom\b", "lean/Chronos"])
    lines = [line.strip() for line in proc.stdout.splitlines() if line.strip()]
    assert len(lines) == 1, f"Unexpected axiom count: {lines}"
    assert re.fullmatch(
        r"lean/Chronos/XorLemmas\.lean:\d+:axiom parityPair_ne_of_single_diff",
        lines[0],
    ), f"Unexpected axiom set: {lines}"


def test_no_deprecated_structure_syntax_in_chronos() -> None:
    proc = run(["grep", "-RIn", r"^[[:space:]]*structure .*:=", "lean/Chronos"])
    lines = [line.strip() for line in proc.stdout.splitlines() if line.strip()]
    assert lines == [], f"Deprecated structure syntax found: {lines}"


def test_xornorm_file_compiles() -> None:
    proc = run(["lake", "env", "lean", "lean/Chronos/XorNorm.lean"])
    assert proc.returncode == 0, proc.stdout + "\n" + proc.stderr


def test_xorreduce_file_compiles() -> None:
    proc = run(["lake", "env", "lean", "lean/Chronos/XorReduce.lean"])
    assert proc.returncode == 0, proc.stdout + "\n" + proc.stderr
