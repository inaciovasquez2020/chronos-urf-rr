import json
from pathlib import Path
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]

TOOL = (
    ROOT
    / "tools/gfe/verify_gfe_full_log_static_euler_map.py"
)

ARTIFACT = (
    ROOT
    / "artifacts/chronos/gfe_full_log_static_euler_map_2026_08_12.json"
)


@pytest.fixture(scope="session")
def verified():
    result = subprocess.run(
        [
            sys.executable,
            str(TOOL),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        timeout=240,
        check=False,
    )

    assert result.returncode == 0, (
        result.stdout
        + "\n"
        + result.stderr
    )

    required = [
        "STATIC_RICCI_SELF_ADJOINT_IDENTITY := PASS",
        "EXACT_SCALAR_CHANNELS := PASS",
        "EXACT_RESOLVENT_DAG := PASS",
        "D_MUNU_EXACT_DAG := PASS",
        "D_MUNU_Q0_NORMALIZATION := PASS",
        "D_MUNU_EF_REGULAR_OPERATOR := PASS",
        (
            "FULL_LOG_STATIC_EULER_MAP := "
            "constructed_as_exact_compositional_DAG"
        ),
        "PHI1_Q0_EINSTEIN := PASS",
        "PHI2_Q0_EINSTEIN := PASS",
        "SCHWARZSCHILD_Q0_EULER := PASS",
        "NEXT_ACTIONS := stop",
    ]

    for marker in required:
        assert marker in result.stdout

    assert ARTIFACT.is_file()

    data = json.loads(
        ARTIFACT.read_text()
    )

    return result.stdout, data


def test_full_log_static_euler_certificate(verified):
    _, data = verified

    assert (
        data["full_log_static_euler_map"]
        == "constructed_as_exact_compositional_DAG"
    )

    assert data["exact_curvature_blocks"] is True
    assert data["exact_resolvent_dag"] is True
    assert data["exact_dressed_scalar"] is True
    assert data["d_mu_nu_exact_dag"] is True
    assert data["q0_einstein_reduction"] is True

    assert data["curvature_truncation"] == "none"


def test_one_form_self_adjoint_relation(verified):
    _, data = verified

    assert (
        data["one_form_self_adjoint_relation"]
        == "C = A + N*F*B"
    )


def test_einstein_targets(verified):
    _, data = verified

    assert (
        data["phi1_q0"]
        == "r*F'(r)+F(r)-1"
    )

    assert (
        data["phi2_q0"]
        == (
            "r*F'(r)+F(r)-1"
            "+2*r*F(r)*N'(r)/N(r)"
        )
    )


def test_open_boundaries_remain_explicit(verified):
    _, data = verified

    boundaries = set(
        data["boundaries"]
    )

    assert "q^2 seed replay remains open" in boundaries

    assert (
        "Bianchi/conservation redundancy remains open"
        in boundaries
    )

    assert (
        "C_N certification remains open"
        in boundaries
    )

    assert (
        "Borel resummation remains open"
        in boundaries
    )

    assert (
        "actual q=1e-2 resummed background remains open"
        in boundaries
    )

    assert (
        "full-log six-state/rank-two rebuild remains open"
        in boundaries
    )
