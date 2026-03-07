# Oblivion Atom Toolkit

This directory contains experimental and diagnostic components supporting
the Oblivion Atom program.

Core objective:
Investigate the relationship between **cycle-overlap rank** and **FO^k type diversity**
in bounded-degree graphs.

## Geometry Diagnostics

Geometry signature

(|B_R|, β₁(B_R), ρ(R)),  ρ(R) = β₁(B_R) / |B_R|

Scripts

toolkit/oblivion/scripts/geometry_signature_scan.py  
toolkit/oblivion/scripts/graph_geometry_plot.py

Results

toolkit/oblivion/results/geometry_rr_R12.png  
toolkit/oblivion/results/geometry_twolift_R12.png

## Cycle-Structure Diagnostics

Scripts

toolkit/oblivion/scripts/cycle_parity_rank.py  
toolkit/oblivion/scripts/cycle_sheet_coherence.py  
toolkit/oblivion/scripts/local_cycle_rank_distribution.py  
toolkit/oblivion/scripts/cor_patch_dependency_chain.py  

FO^k analysis

toolkit/oblivion/scripts/FO_k_type_collision_detector.py

## Interpretation

Three geometry regimes appear in bounded-degree graphs:

Tree  
β₁(B_R) ≈ 0

Sheet  
|B_R| ~ R²

Expander  
|B_R| ~ Δ^R with stable cycle density

Expander regimes exhibit rapid growth of cycle-overlap rank,
supporting the Oblivion Atom mechanism for FO^k type diversity.

## Release

Tag: oblivion-geometry-v1  
Includes geometry diagnostics and visualization artifacts.


## Deterministic Cycle Rigidity Layer

- [COR → Cycle Rank Rigidity](cor_to_cycle_rank.md)
- [Cycle Rank → FOᵏ Type Diversity](cycle_rank_to_fok_diversity.md)
- [FOᵏ Diversity → EntropyDepth Growth](fok_diversity_to_entropy_depth.md)
- [Deterministic Cycle Rigidity Theorem](deterministic_cycle_rigidity_theorem.md)
- [Oblivion Atom Reduction Chain](oblivion_atom_chain.md)
- [Cycle–Rank Rigidity Lemma](proofs/cycle_rank_rigidity.md)
- [Cycle–Rank Rigidity Experiment](experiments/cycle_rank_experiment.md)
