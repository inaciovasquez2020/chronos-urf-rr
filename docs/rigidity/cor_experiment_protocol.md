# Cycle-Overlap Rank Experiment Protocol

Goal:
Empirically evaluate COR(G) for bounded-degree graphs.

Procedure:

1. Generate random Δ-regular graphs.
2. Compute cycle basis using networkx.
3. Construct edge-cycle incidence matrix.
4. Compute cycle overlap matrix O = A^T A.
5. Compute rank(O).

Observation target:

    COR(G) growth vs |V(G)|.

If CLR holds, COR should remain bounded under strong local-type homogeneity constraints.
