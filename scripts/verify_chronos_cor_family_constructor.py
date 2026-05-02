import importlib.util
import json
import subprocess
import sys
from pathlib import Path

GENERATOR = Path("scripts/generate_chronos_cor_triangle_chain_family.py")
INCIDENCE_VERIFIER = Path("scripts/verify_chronos_cor_incidence_certificate.py")
REGISTRY_VERIFIER = Path("scripts/verify_chronos_cor_finite_family_registry.py")
GENERATED_DIR = Path("artifacts/cor/triangle_chain_family")
GENERATED_REGISTRY = GENERATED_DIR / "cor_triangle_chain_family_registry.json"

REQUIRED_BOUNDARY = [
    "It does not prove the finite-to-general lift.",
    "It does not prove the locality-to-depth bridge.",
    "It does not prove theorem-level Chronos closure.",
]

FORBIDDEN = [
    "Chronos is solved",
    "finite-to-general lift is proved",
    "locality-to-depth bridge is proved",
    "theorem-level Chronos closure is proved",
    "infinite graph-family theorem is proved",
    "P vs NP is solved",
]


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def verify_generated_certificates() -> None:
    incidence = load_module(INCIDENCE_VERIFIER, "chronos_cor_incidence")
    registry = load_module(REGISTRY_VERIFIER, "chronos_cor_registry")

    cert_paths = sorted(GENERATED_DIR.glob("cor_triangle_chain_blocks_*.json"))
    if not cert_paths:
        raise SystemExit("no generated triangle-chain certificates found")

    for path in cert_paths:
        cert = json.loads(path.read_text())
        blocks = int(path.stem.split("_")[-1])

        if cert["graph_id"] != f"triangle-chain-blocks-{blocks}":
            raise SystemExit(f"{path}: graph_id mismatch")
        if cert["radius"] != 0:
            raise SystemExit(f"{path}: radius must be 0")
        if cert["vertex_count"] != 3 * blocks:
            raise SystemExit(f"{path}: vertex_count mismatch")
        if len(cert["edges"]) != 4 * blocks - 1:
            raise SystemExit(f"{path}: edge count mismatch")
        if cert["cycle_space_dimension"] != blocks:
            raise SystemExit(f"{path}: cycle dimension mismatch")
        if cert["local_cycle_subspace_rank"] != 0:
            raise SystemExit(f"{path}: radius-0 local rank must be 0")
        if cert["certified_obstruction_rank"] != blocks:
            raise SystemExit(f"{path}: COR mismatch")
        if cert["certified_obstruction_rank"] * 3 < cert["vertex_count"]:
            raise SystemExit(f"{path}: alpha=1/3 inequality failed")

        text = path.read_text()
        missing = [token for token in REQUIRED_BOUNDARY if token not in text]
        forbidden = [token for token in FORBIDDEN if token in text]
        if missing:
            raise SystemExit(f"{path}: missing boundary tokens: {missing}")
        if forbidden:
            raise SystemExit(f"{path}: forbidden overclaim tokens: {forbidden}")

        incidence.verify_certificate(path)

    registry.verify_registry(GENERATED_REGISTRY)


def main() -> None:
    subprocess.run(
        [
            sys.executable,
            str(GENERATOR),
            "--blocks",
            "1",
            "2",
            "3",
            "--output-dir",
            str(GENERATED_DIR),
        ],
        check=True,
    )
    verify_generated_certificates()
    print("Chronos COR symbolic family constructor verification OK.")


if __name__ == "__main__":
    main()
