# Graph-Side Formal Targets

## Fixed invariant

For a finite graph \(G\) and radius \(R\), define
\[
I_R(G)
:=
\operatorname{rank}_{\mathbf F_2}\!\Big(
Z_1(G)\Big/\big\langle Z_1(B_R(v)) : v\in V(G)\big\rangle
\Big).
\]

Here:
- \(Z_1(G)\) is the \(\mathbf F_2\)-cycle space of \(G\),
- \(B_R(v)\) is the induced radius-\(R\) ball around \(v\),
- the denominator is the span in \(Z_1(G)\) of all cycles supported inside radius-\(R\) balls.

## Unconditional graph-side theorem package

### Theorem A
\[
\forall k,\Delta,R\,\forall C\,\exists G\;
\big(
\deg(G)\le \Delta \wedge
\mathrm{FO}^k\text{-homogeneous}_R(G)\wedge
I_R(G)>C
\big).
\]

### Theorem B
\[
\exists (G^+,G^-)\;
\big(
\mathrm{EF}^{R}_{k}(G^+,G^-)\wedge
I_R(G^+)\neq I_R(G^-)
\big).
\]

### Theorem C
\[
\neg\exists f\in \mathrm{FO}^k_R\text{-Def}\;
\forall G\;
\big(
I_R(G)=f(\operatorname{tp}^k_R(G))
\big).
\]

## Conditional complexity-side package

The following remain conditional until exact formal definitions are fixed:

\[
\mathrm{ED}(P_n)\ge \Omega(n\log n),
\]

\[
\forall A\in \mathrm{P}_{\det}\;\exists R_A\;\forall n\;
T_A(n)\ge \mathrm{ED}(P_n)/\operatorname{polylog}(n).
\]

Required missing objects:
1. formal definition of \(ED(P_n)\),
2. formal normalization theorem,
3. formal universality embedding.

## Critical implementation obligations

1. formal definition of \(I_R(G)\),
2. constructive `localTwoComplexH1Rank_growth`,
3. constructive `W5_rank_separation`,
4. FO\(^k_R\)-non-definability derivation from EF/local-type agreement,
5. removal of all critical `axiom` / `sorry` / `admit`.
