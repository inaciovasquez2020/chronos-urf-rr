from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_cmd(*args: str, cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(args),
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def test_reconcile_ledger_accepts_registered_open_assumption(tmp_path: Path) -> None:
    raw = tmp_path / "raw_status.log"
    out = tmp_path / "frontier-status.json"
    raw.write_text(
        "\n".join(
            [
                "SURFACE boundary_ledger_fixture",
                "MODULE boundary_ledger_fixture Chronos.Frontier.BoundaryLedgerFixture",
                "PLACEHOLDER BoundaryLedgerFixture.open_assumption",
            ]
        )
        + "\n"
    )

    result = run_cmd(
        sys.executable,
        "scripts/reconcile_ledger.py",
        "--input",
        str(raw),
        "--schema",
        "boundaries.toml",
        "--output",
        str(out),
    )

    assert result.returncode == 0, result.stderr
    data = json.loads(out.read_text())
    assert data["verification_boundary"]["open_frontier_objects"] == 1
    assert data["errors"] == []
    assert data["surfaces"][0]["computed_status"] == "FRONTIER_OPEN"


def test_reconcile_ledger_rejects_unregistered_open_assumption(tmp_path: Path) -> None:
    raw = tmp_path / "raw_status.log"
    out = tmp_path / "frontier-status.json"
    raw.write_text(
        "\n".join(
            [
                "SURFACE boundary_ledger_fixture",
                "MODULE boundary_ledger_fixture Chronos.Frontier.BoundaryLedgerFixture",
                "PLACEHOLDER BoundaryLedgerFixture.unregistered_assumption",
            ]
        )
        + "\n"
    )

    result = run_cmd(
        sys.executable,
        "scripts/reconcile_ledger.py",
        "--input",
        str(raw),
        "--schema",
        "boundaries.toml",
        "--output",
        str(out),
    )

    assert result.returncode != 0
    assert "unregistered placeholders" in result.stderr


def test_reconcile_ledger_rejects_undocumented_surface(tmp_path: Path) -> None:
    raw = tmp_path / "raw_status.log"
    out = tmp_path / "frontier-status.json"
    raw.write_text(
        "\n".join(
            [
                "SURFACE undocumented_surface",
                "MODULE undocumented_surface Chronos.Frontier.UndocumentedSurface",
                "PLACEHOLDER UndocumentedSurface.open_assumption",
            ]
        )
        + "\n"
    )

    result = run_cmd(
        sys.executable,
        "scripts/reconcile_ledger.py",
        "--input",
        str(raw),
        "--schema",
        "boundaries.toml",
        "--output",
        str(out),
    )

    assert result.returncode != 0
    assert "undocumented surfaces" in result.stderr


def test_forbidden_overclaim_scanner_rejects_forbidden_claim(tmp_path: Path) -> None:
    bad = tmp_path / "bad.md"
    bad.write_text("This claims unconditional theorem-level closure.\n")

    result = run_cmd(
        sys.executable,
        "scripts/check_forbidden_overclaims.py",
        "--schema",
        "boundaries.toml",
        "--paths",
        str(bad),
    )

    assert result.returncode != 0
    assert "forbidden claim token" in result.stderr


def test_forbidden_overclaim_scanner_accepts_boundary_safe_text(tmp_path: Path) -> None:
    good = tmp_path / "good.md"
    good.write_text("This is a conditional frontier-open status artifact.\n")

    result = run_cmd(
        sys.executable,
        "scripts/check_forbidden_overclaims.py",
        "--schema",
        "boundaries.toml",
        "--paths",
        str(good),
    )

    assert result.returncode == 0, result.stderr


def test_forbidden_overclaim_scanner_accepts_boundary_disclaimer(tmp_path: Path) -> None:
    good = tmp_path / "boundary.md"
    good.write_text(
        "\n".join(
            [
                "## Boundary",
                "",
                "Does not prove:",
                "- P vs NP closure",
                "- unrestricted Chronos-RR",
                "- unconditional theorem-level closure",
            ]
        )
        + "\n"
    )

    result = run_cmd(
        sys.executable,
        "scripts/check_forbidden_overclaims.py",
        "--schema",
        "boundaries.toml",
        "--paths",
        str(good),
    )

    assert result.returncode == 0, result.stderr


def test_forbidden_overclaim_scanner_accepts_json_nonclaim_array(tmp_path: Path) -> None:
    good = tmp_path / "boundary.json"
    good.write_text(
        '{\n'
        '  "does_not_prove": [\n'
        '    "P vs NP closure",\n'
        '    "unrestricted Chronos-RR"\n'
        '  ]\n'
        '}\n'
    )

    result = run_cmd(
        sys.executable,
        "scripts/check_forbidden_overclaims.py",
        "--schema",
        "boundaries.toml",
        "--paths",
        str(good),
    )

    assert result.returncode == 0, result.stderr
