import argparse
import json
from pathlib import Path
from typing import Any


def triangle_chain_certificate(blocks: int, radius: int = 0) -> dict[str, Any]:
    if blocks <= 0:
        raise ValueError("blocks must be positive")
    if radius != 0:
        raise ValueError("this constructor surface is locked to radius 0")

    vertex_count = 3 * blocks
    edges: list[list[int]] = []
    cycle_basis: list[list[int]] = []

    for i in range(blocks):
        a = 3 * i
        tri_edges = [[a, a + 1], [a + 1, a + 2], [a + 2, a]]
        start = len(edges)
        edges.extend(tri_edges)

        vec = [0] * (4 * blocks - 1)
        vec[start] = 1
        vec[start + 1] = 1
        vec[start + 2] = 1
        cycle_basis.append(vec)

        if i + 1 < blocks:
            edges.append([a + 2, a + 3])

    edge_count = len(edges)
    assert edge_count == 4 * blocks - 1

    return {
        "certificate_type": "chronos_cor_incidence_basis_certificate",
        "version": 1,
        "graph_id": f"triangle-chain-blocks-{blocks}",
        "field": "F2",
        "radius": radius,
        "vertex_count": vertex_count,
        "edges": edges,
        "cycle_basis": [v[:edge_count] for v in cycle_basis],
        "local_cycle_basis": [],
        "cycle_space_dimension": blocks,
        "local_cycle_subspace_rank": 0,
        "certified_obstruction_rank": blocks,
        "linear_growth_claim": {
            "enabled": True,
            "alpha_num": 1,
            "alpha_den": 3
        },
        "boundary": [
            "This finite incidence-basis certificate verifies raw GF(2) boundary annihilation.",
            "It verifies the finite cycle-space dimension from the incidence matrix.",
            "It verifies the finite local-cycle rank from radius-R graph balls.",
            "It does not prove the finite-to-general lift.",
            "It does not prove the locality-to-depth bridge.",
            "It does not prove theorem-level Chronos closure."
        ]
    }


def family_registry(blocks_values: list[int], output_dir: Path) -> dict[str, Any]:
    cert_paths = [
        str(output_dir / f"cor_triangle_chain_blocks_{blocks}.json")
        for blocks in blocks_values
    ]
    return {
        "registry_type": "chronos_cor_finite_family_registry",
        "version": 1,
        "field": "F2",
        "shared_radius": 0,
        "alpha_num": 1,
        "alpha_den": 3,
        "certificates": cert_paths,
        "boundary": [
            "This registry verifies a finite family of incidence-basis certificates only.",
            "It verifies shared radius and finite COR_R(G_i) >= alpha |V_i| inequalities.",
            "It does not prove an infinite graph-family theorem.",
            "It does not prove the finite-to-general lift.",
            "It does not prove the locality-to-depth bridge.",
            "It does not prove theorem-level Chronos closure."
        ]
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--blocks", type=int, nargs="+", default=[1, 2, 3])
    parser.add_argument("--output-dir", type=Path, default=Path("artifacts/cor/triangle_chain_family"))
    args = parser.parse_args()

    if any(n <= 0 for n in args.blocks):
        raise SystemExit("all block counts must be positive")

    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    for blocks in args.blocks:
        cert = triangle_chain_certificate(blocks)
        path = output_dir / f"cor_triangle_chain_blocks_{blocks}.json"
        path.write_text(json.dumps(cert, indent=2) + "\n")

    registry = family_registry(args.blocks, output_dir)
    (output_dir / "cor_triangle_chain_family_registry.json").write_text(
        json.dumps(registry, indent=2) + "\n"
    )

    print(f"generated Chronos COR triangle-chain family certificates in {output_dir}")


if __name__ == "__main__":
    main()
