import importlib.util
import json
from pathlib import Path
from typing import Any

REGISTRY = Path("artifacts/cor/cor_finite_family_registry.json")
INCIDENCE_VERIFIER = Path("scripts/verify_chronos_cor_incidence_certificate.py")

REQUIRED_BOUNDARY = [
    "This registry verifies a finite family of incidence-basis certificates only.",
    "It verifies shared radius and finite COR_R(G_i) >= alpha |V_i| inequalities.",
    "It does not prove an infinite graph-family theorem.",
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
    "infinite graph-family theorem is proved",
    "P vs NP is solved",
]


def require_int(obj: dict[str, Any], key: str) -> int:
    value = obj.get(key)
    if not isinstance(value, int):
        raise SystemExit(f"{key} must be an integer")
    if value < 0:
        raise SystemExit(f"{key} must be nonnegative")
    return value


def load_incidence_verifier():
    spec = importlib.util.spec_from_file_location("chronos_cor_incidence", INCIDENCE_VERIFIER)
    if spec is None or spec.loader is None:
        raise SystemExit("could not load incidence verifier")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    raw = REGISTRY.read_text()
    registry = json.loads(raw)

    if registry.get("registry_type") != "chronos_cor_finite_family_registry":
        raise SystemExit("wrong registry_type")
    if registry.get("field") != "F2":
        raise SystemExit("field must be F2")

    shared_radius = require_int(registry, "shared_radius")
    alpha_num = require_int(registry, "alpha_num")
    alpha_den = require_int(registry, "alpha_den")
    if alpha_num == 0 or alpha_den == 0:
        raise SystemExit("alpha must be positive")

    cert_paths = registry.get("certificates")
    if not isinstance(cert_paths, list) or not cert_paths:
        raise SystemExit("certificates must be a nonempty list")

    verifier = load_incidence_verifier()

    seen: set[str] = set()
    for entry in cert_paths:
        if not isinstance(entry, str):
            raise SystemExit("certificate paths must be strings")
        if entry in seen:
            raise SystemExit(f"duplicate certificate path: {entry}")
        seen.add(entry)

        path = Path(entry)
        if not path.exists():
            raise SystemExit(f"missing certificate: {entry}")

        verifier.verify_certificate(path)
        cert = json.loads(path.read_text())

        if cert.get("field") != "F2":
            raise SystemExit(f"{entry}: field must be F2")
        if cert.get("radius") != shared_radius:
            raise SystemExit(f"{entry}: radius does not match shared_radius")

        cor = require_int(cert, "certified_obstruction_rank")
        vertex_count = require_int(cert, "vertex_count")
        if cor * alpha_den < alpha_num * vertex_count:
            raise SystemExit(f"{entry}: shared alpha inequality failed")

    boundary = registry.get("boundary")
    if not isinstance(boundary, list):
        raise SystemExit("boundary must be a list")
    boundary_text = "\n".join(str(x) for x in boundary)

    missing = [token for token in REQUIRED_BOUNDARY if token not in boundary_text]
    forbidden = [token for token in FORBIDDEN if token in boundary_text or token in raw]
    if missing:
        raise SystemExit(f"missing boundary tokens: {missing}")
    if forbidden:
        raise SystemExit(f"forbidden overclaim tokens: {forbidden}")

    print(f"Chronos COR finite family registry verification OK: {REGISTRY}")


if __name__ == "__main__":
    main()
