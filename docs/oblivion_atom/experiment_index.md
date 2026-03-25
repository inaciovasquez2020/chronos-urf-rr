# Oblivion Atom — Experiment Index

This file lists all currently implemented experimental probes used to
analyze cycle-overlap behavior and FO^k diversity in bounded-degree graphs.

## Geometry Diagnostics

geometry_signature_scan.py  
Computes

(|B_R|, β₁(B_R), ρ(R))

graph_geometry_plot.py  
Plots geometry signatures.

Outputs

geometry_rr_R12.png  
geometry_twolift_R12.png

## Cycle-Structure Diagnostics

cycle_parity_rank.py  
Estimates parity-cycle rank contributions.

cycle_sheet_coherence.py  
Detects sheet-like cycle coherence patterns.

local_cycle_rank_distribution.py  
Measures cycle rank distribution across local balls.

cor_patch_dependency_chain.py  
Analyzes dependency chains between cycle patches.

## Logical Diagnostics

FO_k_type_collision_detector.py  
Searches for FO^k neighborhood type collisions.

## Purpose

These probes provide empirical evidence regarding the relationship between

cycle-overlap rank  
local graph geometry  
FO^k distinguishability.

## Current Status

Geometry diagnostic layer implemented.  
Cycle-rank diagnostic layer implemented.  
FO^k collision detector implemented.

