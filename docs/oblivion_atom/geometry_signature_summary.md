# Geometry Signature — Repository Summary

Module: Oblivion Atom Toolkit

Purpose:
Provide a reproducible diagnostic for detecting graph geometry regimes
(tree / sheet / expander) via local cycle statistics.

Core observable:

(|B_R|, β₁(B_R), ρ(R)),  ρ(R) = β₁(B_R) / |B_R|

Files introduced:

Scripts
- toolkit/oblivion/scripts/geometry_signature_scan.py
- toolkit/oblivion/scripts/graph_geometry_plot.py

Results
- toolkit/oblivion/results/geometry_rr_R12.png
- toolkit/oblivion/results/geometry_twolift_R12.png

Documentation
- docs/oblivion_atom/geometry_signature.md
- docs/oblivion_atom/geometry_signature_results.md
- docs/oblivion_atom/geometry_signature_usage.md

Release
- tag: oblivion-geometry-v1
- GitHub release published with plotted diagnostics

Interpretation:

Tree regime
β₁(B_R) ≈ 0

Sheet regime
|B_R| ≈ R²

Expander regime
|B_R| ≈ Δ^R and ρ(R) stabilizes

Role in Oblivion Atom:

Expander geometry implies rapid cycle-overlap growth,
which is the structural driver behind FO^k type diversity
in bounded-degree graphs.

Status:
Geometry diagnostic layer complete and reproducible.

