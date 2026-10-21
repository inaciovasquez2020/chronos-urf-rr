# GfE bivector-trace normalization audit

Date: 2026-10-21

Audited source revision: `2f56bce744c6e6c8bff90af2e992256d41b82a17`

## Finding

An independent symbolic reconstruction of the Schwarzschild curvature operator and the axial/even-parity principal curvature perturbations gives an eightfold discrepancy between the ordinary six-dimensional matrix trace and the axial coefficient used to calibrate the polar tests.

This audit documents the discrepancy. It does **not** choose a replacement action convention, alter the generator coefficient table, or claim a complete quadratic-action derivation.

## Convention identity

Use the six-dimensional bivector basis indexed by the six ordered representatives
`(0,1), (0,2), (0,3), (1,2), (1,3), (2,3)`, and the curvature endomorphism whose matrix entries are the corresponding components `R_ab{}^{cd}`. In the unrestricted tensor contraction, each of the three antisymmetric index-pair sums counts both pair orientations. Thus, for a curvature tensor antisymmetric in each pair, the unrestricted cubic contraction is eight times the trace computed by summing over one representative per pair:
`R_ab{}^{cd} R_cd{}^{ef} R_ef{}^{ab} = 8 Tr_{Lambda^2}(Rop^3)`,
with the sums on the left unrestricted and the trace on the right taken in the six-dimensional bivector basis.

This identity explains a possible factor of eight; it does not identify which quantity the GfE action is intended to use.

## Independent symbolic checks

The calculation constructs the Schwarzschild metric
`diag(-f, 1/f, r^2, r^2 sin(theta)^2)`, with `f=1-2M/r`, computes the background curvature operator, inserts only the relevant principal second-time or second-radial curvature perturbations, and evaluates the angular integrals with a normalized `Y_20`. It does not use the repository axial table to calibrate the polar calculation.

The computed background operator is
`diag(2M/r^3, -M/r^3, -M/r^3, -M/r^3, -M/r^3, 2M/r^3)`.

### Axial calibration comparison

The ordinary matrix-trace coefficient of the axial `(partial_t^2 h_1)^2` principal term is
`9 M / (2 r^2 (r-2M))`.

The generator table's `k1_tt^2` coefficient at `ell=2` (`L=ell(ell+1)=6`) is
`36 M / (r^2 (r-2M))`.

Their ratio is exactly `8`. The current polar test derives its normalization by taking this ratio, so its polar normalization is not independent of the table convention.

### Even-parity time-principal term

The independently integrated ordinary matrix-trace cubic principal expression is
`3 M r / (2 (r-2M)^2) * (q_H2^2 - q_K^2)`.

If the relative-action multiplier `1/9` is retained, this becomes
`M r / (6 (r-2M)^2) * (q_H2^2 - q_K^2)`,
with Hessian in `(q_H2,q_K)`
`diag(M r/(3(r-2M)^2), -M r/(3(r-2M)^2))`.

For `M>0` and `r>2M`, the Hessian is nonzero and rank two. Therefore an overall factor-of-eight correction does not remove this principal-part obstruction.

### Even-parity lapse radial-principal term

The independently integrated ordinary matrix-trace cubic term involving `(partial_r^2 H0)^2` is
`3 M (r-2M)^2 / (2 r^3) * q_H0_rr^2`.

After the same `1/9` relative-action multiplier, the coefficient of `H0_rr^2` is
`M (r-2M)^2 / (6 r^3)`.
Its Euler–Lagrange equation has fourth-radial-derivative coefficient
`M (r-2M)^2 / (3 r^3)`,
which is nonzero for `M>0` and `r>2M`.

The current repository test reports eight times these cubic and relative-action coefficients. This correction rescales the principal terms; it does not make them vanish.

## Why this remains unresolved

The generator describes its hardcoded coefficient table as the coefficient table for
`integral sqrt(-g) Tr_{Lambda^2}(Rop^3)`, which ordinarily means the matrix trace. However, the inspected source does not independently define the action's contraction convention or provide a separately executable coordinate-expansion derivation of this table. The fixed-mode hashes validate the hardcoded table against its own canonicalized values; they do not independently establish the convention.

Consequently, two different claims must not be conflated:

1. **Algebraic principal-part finding:** the nonzero polar time and lapse radial principal terms survive a uniform factor-of-eight rescaling.
2. **Action-derived physical claim:** the exact coefficient and interpretation of those terms depend on which cubic invariant the action actually specifies. That specification is not resolved by the inspected source.

## Required next step

Before changing the generator or dependent axial receipts, document the intended invariant explicitly—for example, define the bivector endomorphism and state whether the action uses its ordinary matrix trace or the unrestricted six-index contraction. Then independently regenerate the axial coefficient table from that definition and replay all dependent receipts/tests.

`REPOSITORY_CHANGES :=` documentation only; generator and tests unchanged.

`VERIFICATION_BOUNDARY :=` SymPy 1.14 symbolic calculations reproduced the stated principal coefficients and exact ratio. No repository test suite was run as part of this audit, and no full quadratic action was independently derived.
