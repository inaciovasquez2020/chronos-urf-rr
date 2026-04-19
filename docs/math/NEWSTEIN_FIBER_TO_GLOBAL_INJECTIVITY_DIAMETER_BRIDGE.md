# Newstein Fiber-to-Global Injectivity Diameter Bridge

Status: OPEN

## Statement

Assume the Fiber Injectivity Diameter Lemma:
\[
u\neq v,\quad
\iota_u(c_u)=\iota_v(c_v)
\Longrightarrow
\forall S\in C_2,\ 
\partial S=c_u-c_v
\Rightarrow
\operatorname{diam}(\operatorname{supp} S)>L.
\]

Assume also that every admissible fiber representative is supported in an \(L\)-bounded rooted ball.

Then for \(u\neq v\),
\[
\iota_u([c_u])=\iota_v([c_v])
\Longrightarrow
[c_u]=0=[c_v].
\]

Equivalently, the induced map
\[
\bigoplus_{u} \bigl(Z_1(B_r(u))/W_u\bigr)\longrightarrow Z_1/W^{\mathrm{glob}}
\]
is injective on pairwise distinct fiber summands.

## Role

This is the direct-sum embedding bridge extracted from the diameter obstruction.

## Dependencies

- docs/math/NEWSTEIN_FIBER_INJECTIVITY_DIAMETER_LEMMA.md
- docs/math/NEWSTEIN_FIBER_TO_GLOBAL_INJECTIVITY_THEOREM.md
- docs/math/NEWSTEIN_SIGMA_PACKAGE_DIMENSION_DROP.md

## Finish condition

Replace this OPEN bridge by a theorem-level derivation that the diameter obstruction forces cross-fiber equality to be trivial.
