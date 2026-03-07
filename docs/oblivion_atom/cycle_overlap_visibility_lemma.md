# Cycle–Overlap Visibility Lemma (Empirical)

## Statement

Fix Δ and R.

There exists a threshold T such that for any graph G with
max degree ≤ Δ,

    COR_R(G) ≥ T

implies

    ∃ u,v : tp_3(u) ≠ tp_3(v)

Equivalently,

    WL² distinguishes vertices of G.

## Evidence

Experiment: rr_n12000_d4_seed9

R = 6

Measured:

COR_R(G) = 649  
overlap components = 253  
largest component = 82

WL¹:

homogeneous

WL² (sample 250):

distinct colors = 4

WL² (sample 500):

distinct colors = 7

Thus

    ∃ u,v : χ_WL²(u) ≠ χ_WL²(v)

## Interpretation

Cycle–overlap rank becomes visible at

    FO³

while remaining invisible to

    FO¹, FO².

This matches the expected locality barrier in bounded-degree graphs.

## Role in Oblivion Atom

Provides the missing bridge

    cycle overlap → FO^k type diversity

empirically at

    k = 3.


Open proof task tracked in GitHub issue.
