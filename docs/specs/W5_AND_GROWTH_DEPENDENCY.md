# W5 and Growth Dependency

## Unconditional graph-side dependency split

The unconditional graph-side package reduces to two constructive witness engines.

### Engine 1: growth family
Prove a constructive theorem of the form
\[
\forall R\,\forall C\,\exists G\;(I_R(G)>C),
\]
with the additional local-uniformity property needed to derive FO\(^k_R\)-homogeneity.

Canonical package name:
`localTwoComplexH1Rank_growth`

Required outputs:
1. explicit graph family \(G_n\),
2. proof of radius-\(R\) local uniformity,
3. proof that local cycle-span contribution is controlled,
4. proof that \(I_R(G_n)\to\infty\).

### Engine 2: explicit separation pair
Prove a constructive theorem of the form
\[
\exists (G^+,G^-)\;
\big(
tp_k_R(G^+) = tp_k_R(G^-)
\wedge
I_R(G^+) \neq I_R(G^-)
\big).
\]

Canonical package name:
`W5_rank_separation`

Required outputs:
1. explicit definitions of \(G^+\) and \(G^-\),
2. proof of local-type agreement,
3. proof of quotient-rank separation.

## Reduction map

### Theorem A
Unboundedness follows from Engine 1 plus FO\(^k_R\)-homogeneity transfer.

### Theorem B
Witness separation is exactly Engine 2.

### Theorem C
Nonfactorization follows from Engine 2 plus the propositional reduction schema.

## Critical conclusion

Until both engines are constructive, the unconditional graph-side package is incomplete.

## Immediate implementation order

1. formalize `IR`,
2. complete `localTwoComplexH1Rank_growth`,
3. complete `W5_rank_separation`,
4. package Theorem A,
5. package Theorem B,
6. package Theorem C.
