# Oblivion Atom — Reproducibility

All diagnostics in this module are reproducible from the repository.

## 1. Geometry Signature

Compute the signature:

python3 toolkit/oblivion/scripts/geometry_signature_scan.py \
--graph_json GRAPH.json \
--root 0 \
--Rmax 12 \
> signature.json

## 2. Plot Geometry

python3 toolkit/oblivion/scripts/graph_geometry_plot.py \
--graph_json GRAPH.json \
--max_R 12 \
--out geometry.png

## 3. Cycle Diagnostics

Run cycle analysis scripts:

cycle_parity_rank.py  
cycle_sheet_coherence.py  
local_cycle_rank_distribution.py  
cor_patch_dependency_chain.py

## 4. Logical Diagnostics

Detect FO^k neighborhood collisions:

FO_k_type_collision_detector.py

## 5. Repository State

Release tag:

oblivion-geometry-v1

Artifacts:

geometry_rr_R12.png  
geometry_twolift_R12.png  

All scripts and documentation are version-controlled
under the chronos-urf-rr repository.

