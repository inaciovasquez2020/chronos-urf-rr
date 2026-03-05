# Oblivion Atom — Roadmap

Current repository status:
Geometry diagnostics, cycle-rank diagnostics, and FO^k collision tools are implemented.

Next stages focus on connecting empirical diagnostics to the formal
cycle-overlap → FO^k diversity lemma.

## Stage 1 — Empirical Validation

Goals

Measure cycle-overlap rank growth on large bounded-degree graphs.

Experiments

random_regular_graphs  
random_lifts  
expander-of-expanders constructions  
grid and torus controls

Outputs

cycle overlap rank scaling  
FO^k collision rates  
geometry signatures

## Stage 2 — Structural Identification

Goal

Identify structural mechanisms producing large cycle-overlap rank.

Hypotheses

expander cycle mixing  
sheet-like overlap layers  
patch dependency chains

## Stage 3 — Logical Translation

Goal

Translate cycle-overlap growth into FO^k neighborhood diversity.

Tools

FO_k_type_collision_detector  
neighborhood enumeration  
local-type growth analysis

## Stage 4 — Formal Lemma

Target statement

For fixed k,Δ there exist R,T such that

COR_R(G) ≥ T ⇒ G is not FO^k_R-homogeneous.

This is the Oblivion Atom rigidity lemma.

## Status

Diagnostics implemented  
Experiments running  
Formal proof stage pending

