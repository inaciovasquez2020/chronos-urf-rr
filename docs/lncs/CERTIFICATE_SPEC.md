# Certificate Specification

## Objects

Graph := (V, E)

CycleBasis := list of edge-sets spanning Z1(G)

LocalCycles := cycles with length ≤ 2R+1

QuotientRank := dim_F2(Z1(G) / Z1^{≤ 2R+1}(G))

## JSON Schema (abstract)

{
  "vertices": [...],
  "edges": [...],
  "cycle_basis": [...],
  "local_cycles": [...],
  "quotient_rank": <int>
}

## Invariant Binding

Verifier(JSON) == Lean(RankSeparation)

## Guarantee

If verifier accepts JSON, then:
I(G⁺) ≠ I(G⁻)

## Constraint

All fields must reconstruct cycle space and local subspace exactly.
