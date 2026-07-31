"""Primary-source extraction anchors.

The registry is a research map. It does not import external results into the
formal development or convert bibliography into a theorem.
"""

from __future__ import annotations


PRIMARY_SOURCES = [
    {
        "id": "regge_wheeler_1957",
        "identifier": "doi:10.1103/PhysRev.108.1063",
        "role": "Schwarzschild odd-parity master equation and potential.",
        "extracts": [
            "odd-parity amplitudes",
            "master radial equation",
            "potential normalization",
            "coordinate convention",
        ],
    },
    {
        "id": "moncrief_1974",
        "identifier": "doi:10.1103/PhysRevD.9.2707",
        "role": "Hamiltonian reduction and gauge-invariant master variable.",
        "extracts": [
            "canonical variables",
            "constraint elimination",
            "master normalization",
            "reduced Hamiltonian",
        ],
    },
    {
        "id": "gerlach_sengupta_1980",
        "identifier": "doi:10.1103/PhysRevD.22.1300",
        "role": "Covariant 2+2 gauge-invariant spherical reduction.",
        "extracts": [
            "orbit-space geometry",
            "odd-parity invariant",
            "reduced field equation",
            "Schwarzschild specialization",
        ],
    },
    {
        "id": "clarkson_barrett_2002",
        "identifier": "arXiv:gr-qc/0209051",
        "role": "Covariant curvature realization of Regge-Wheeler dynamics.",
        "extracts": [
            "curvature variable",
            "harmonic decomposition",
            "Regge-Wheeler tensor",
            "geometric identification",
        ],
    },
    {
        "id": "kodama_ishibashi_2003",
        "identifier": "arXiv:hep-th/0305147",
        "role": "Warped-product vector-sector master reduction.",
        "extracts": [
            "background decomposition",
            "vector invariant",
            "master variable",
            "four-dimensional specialization",
        ],
    },
    {
        "id": "martel_poisson_2005",
        "identifier": "arXiv:gr-qc/0502028",
        "role": "Covariant Schwarzschild odd-parity master formalism.",
        "extracts": [
            "gauge transformation",
            "metric invariant",
            "master normalization",
            "wave equation",
            "source normalization",
        ],
    },
    {
        "id": "tattersall_ferreira_lagos_2017",
        "identifier": "arXiv:1711.01992",
        "role": "Covariant quadratic-action decomposition.",
        "extracts": [
            "action basis",
            "background restrictions",
            "odd-parity quadratic action",
            "auxiliary-field elimination",
            "single-variable master action",
        ],
    },
]


def primary_source_ids() -> list[str]:
    return [str(source["id"]) for source in PRIMARY_SOURCES]
