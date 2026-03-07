# Reproducing the Cycle-Overlap Visibility Experiment

Repository:
chronos-urf-rr

Graph tested:
rr_n12000_d4_seed9

Radius:
R = 6

---

## Run full experiment

Execute:

./toolkit/oblivion/experiments/run_visibility_experiment.sh

This runs:

1. cycle_overlap_graph.py
2. cycle_component_rank.py
3. wl_k_test.py (sample 250)
4. wl_k_test.py (sample 500)

---

## Expected results

Cycle structure:

cycle_count ≈ 649  
largest overlap component ≈ 82

Cycle rank:

COR_R(G) = 649

WL tests:

WL¹ homogeneous

WL²:

distinct colors ≥ 4

Thus

∃ u,v : χ_WL²(u) ≠ χ_WL²(v)

---

## Interpretation

High cycle-overlap rank becomes visible at

FO³

via

WL² color refinement.

This provides empirical support for the

Cycle-Overlap Visibility Lemma.
