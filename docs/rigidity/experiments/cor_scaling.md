# Cycle–Overlap Rank Scaling Experiment

## Purpose
Empirically study growth of the cycle–overlap rank in bounded-degree graphs to test rigidity predictions related to the EntropyDepth program.

## Setup
Graphs are generated with fixed bounded degree and increasing vertex count.

For each instance we compute:

- cycle incidence matrix
- cycle-overlap matrix
- rank of the overlap matrix

The experiment records:

- number of vertices n
- radius parameter R
- cycle rank
- number of repeated cycle pairs
- minimal witness subgraph

## Outputs

results/cor_scaling_regular.json  
results/cor_scaling.png

## Interpretation

Observed behavior shows that the overlap rank grows linearly with the graph size in the tested families.

This supports the rigidity heuristic:

cycle-overlap rank ∝ number of vertices.

Consequently, FO^k-local refinement systems cannot compress the configuration space beyond O(1) entropy loss per refinement step.

This empirical scaling aligns with the Chronos / EntropyDepth lower-bound mechanism.
