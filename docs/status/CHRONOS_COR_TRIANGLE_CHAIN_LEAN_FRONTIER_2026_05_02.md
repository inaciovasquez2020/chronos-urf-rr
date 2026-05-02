# Chronos COR Triangle-Chain Lean Frontier — 2026-05-02

Status: LEAN THEOREM-FRONTIER SKELETON / AXIOM-LEVEL TARGET

## Object

This adds a Lean-visible theorem-frontier surface for the next Chronos COR target:

\[
\forall n\ge 1,\quad \operatorname{COR}_0(G_n)=n.
\]

The Lean object is:

```lean
axiom triangleChain_COR0_eq_blocks :
  forall n : Nat, 1 <= n ->
    CertifiedObstructionRankZero (triangleChainGraph n) = n
```

## Conditional theorem surface

The file also records a conditional lower-bound theorem:

```lean
theorem triangleChain_COR0_linear_lower_bound
```

This theorem depends on `triangleChain_COR0_eq_blocks`.

## Boundary

This is a Lean theorem-frontier skeleton only.

It does not prove finite-to-general lift.

It does not prove locality-to-depth bridge.

It does not prove theorem-level Chronos closure.

It does not assert a Chronos closure theorem.

It does not solve P vs NP.
