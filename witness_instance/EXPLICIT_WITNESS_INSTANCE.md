# Explicit Witness Instance

## Base Graph
Petersen graph (10 vertices, 15 edges, 3-regular)

## Construction
Define two 2-lifts at radius R = 2:
- G^+ : trivial lift (σ ≡ 0)
- G^- : twisted lift with twisted base edge (0,1)

## Computed Quantities
- dim_F2 Z1(G^+) = 12
- dim_F2 Z1^≤5(G^+) = 12
- I_URF(G^+;2) = 0

- dim_F2 Z1(G^-) = 11
- dim_F2 Z1^≤5(G^-) = 10
- I_URF(G^-;2) = 1

## Verified
1. bounded degree ≤ 3
2. explicit 2-lifts constructed
3. I_URF(G^+;2) != I_URF(G^-;2)
4. first real witness object computed

## Not Yet Verified
- local indistinguishability certificate
- tree-ball certificate

## Artifact
artifacts/petersen_2lift_urf_witness_r2.json
