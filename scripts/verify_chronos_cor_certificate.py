import json
from pathlib import Path
from typing import Any

DEFAULT_CERT = Path("artifacts/cor/cor_certificate_example.json")

REQUIRED_BOUNDARY = [
    "This finite certificate records arithmetic consistency for COR_R(G).",
    "It does not prove the finite-to-general lift.",
    "It does not prove the locality-to-depth bridge.",
    "It does not prove theorem-level Chronos closure.",
]

FORBIDDEN = [
    "Chronos is solved",
    "theorem-level Chronos closure is proved",
    "unconditional Chronos closure",
    "finite-to-general lift is proved",
    "locality-to-depth bridge is proved",
]


def require_int(obj: dict[str, Any], key: str) -> int:
    value = obj.get(key)
    if not isinstance(value, int):
        raise SystemExit(f"{key} must be an integer")
    if value < 0:
        raise SystemExit(f"{key} must be nonnegative")
    return value


def verify_certificate(path: Path) -> None:
    cert = json.loads(path.read_text())

    if cert.get("certificate_type") != "chronos_certified_obstruction_rank":
        raise SystemExit("wrong certificate_type")
    if cert.get("field") != "F2":
        raise SystemExit("field must be F2")

    radius = require_int(cert, "radius")
    vertex_count = require_int(cert, "vertex_count")
    edge_count = require_int(cert, "edge_count")
    cycle_dim = require_int(cert, "cycle_space_dimension")
    local_rank = require_int(cert, "local_cycle_subspace_rank")
    cor = require_int(cert, "certified_obstruction_rank")

    if radius < 0:
        raise SystemExit("radius must be nonnegative")
    if vertex_count == 0:
        raise SystemExit("vertex_count must be positive")
    if edge_count < vertex_count - 1:
        raise SystemExit("edge_count below connected-example lower sanity bound")
    if cycle_dim > edge_count:
        raise SystemExit("cycle_space_dimension cannot exceed edge_count")
    if local_rank > cycle_dim:
        raise SystemExit("local_cycle_subspace_rank cannot exceed cycle_space_dimension")
    if cor != cycle_dim - local_rank:
        raise SystemExit("certified_obstruction_rank must equal cycle_space_dimension - local_cycle_subspace_rank")

    growth = cert.get("linear_growth_claim", {})
    if growth.get("enabled") is True:
        alpha_num = require_int(growth, "alpha_num")
        alpha_den = require_int(growth, "alpha_den")
        if alpha_den == 0:
            raise SystemExit("alpha_den must be positive")
        if alpha_num == 0:
            raise SystemExit("alpha_num must be positive when growth claim is enabled")
        if cor * alpha_den < alpha_num * vertex_count:
            raise SystemExit("linear growth inequality failed")

    boundary = cert.get("boundary")
    if not isinstance(boundary, list):
        raise SystemExit("boundary must be a list")
    boundary_text = "\n".join(str(x) for x in boundary)

    missing = [token for token in REQUIRED_BOUNDARY if token not in boundary_text]
    forbidden = [token for token in FORBIDDEN if token in boundary_text or token in path.read_text()]
    if missing:
        raise SystemExit(f"missing boundary tokens: {missing}")
    if forbidden:
        raise SystemExit(f"forbidden overclaim tokens: {forbidden}")

    print(f"Chronos COR finite certificate verification OK: {path}")


def main() -> None:
    verify_certificate(DEFAULT_CERT)


if __name__ == "__main__":
    main()
