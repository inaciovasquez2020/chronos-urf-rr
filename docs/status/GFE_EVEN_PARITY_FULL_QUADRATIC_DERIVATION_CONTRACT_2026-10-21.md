# Independent even-parity quadratic-action derivation: execution contract

Date: 2026-10-21

Status: `SPECIFIED_NOT_EXECUTED`. This file defines the derivation boundary; it is not evidence that the full quadratic action has been computed.

## Target

Independently derive the complete coefficient of `epsilon**2` in

```
S_cubic[epsilon] = integral dt dr dtheta dphi
                   sqrt(-det(g(epsilon))) Tr_{Lambda^2}(Rop(epsilon)**3)
```

for the even-parity Regge–Wheeler-gauge perturbation of Schwarzschild, at fixed `ell=2, m=0`, with all four radial/time-dependent amplitudes `H0(t,r), H1(t,r), H2(t,r), K(t,r)`. No axial table, cached coefficient table, axial normalization ratio, or existing polar helper may be used to construct the answer.

## Metric and conventions

Let `f=1-2M/r`, `Y=sqrt(5/(16*pi))*(3*cos(theta)**2-1)`, and coordinates `(t,r,theta,phi)`. Define the one-parameter metric directly by

```
g_tt   = -f * (1 + epsilon * H0 * Y)
g_tr   =       epsilon * H1 * Y
g_rr   = 1/f * (1 + epsilon * H2 * Y)
g_thth = r**2 * (1 + epsilon * K * Y)
g_phph = r**2*sin(theta)**2 * (1 + epsilon * K * Y)
```

All other components vanish. This explicitly fixes the sign and normalization convention for this derivation. If a different convention is intended by the physical action, it must be translated explicitly rather than silently mixed into this calculation.

The matrix trace is taken on the six representative bivectors
`(t,r),(t,theta),(t,phi),(r,theta),(r,phi),(theta,phi)`, with
`(Rop)_(ab)^(cd) = g^(ce) g^(df) R_(abef)`.
The action uses the ordinary six-dimensional matrix trace. It does **not** use the unrestricted six-index contraction unless an explicit factor of eight is independently justified by the action definition.

## Required calculation

1. Build `g(epsilon)` and its inverse from the metric, not from the repository coefficient table.
2. Compute Christoffel symbols from the metric definition.
3. Compute the Riemann tensor from the Christoffel symbols, with the sign convention stated in the implementation.
4. Assemble the six-dimensional curvature endomorphism.
5. Form `sqrt(-det(g(epsilon))) * trace(Rop(epsilon)**3)`.
6. Extract the exact `epsilon**2` coefficient by `diff(expression, epsilon, 2).subs(epsilon,0)/2`.
7. Integrate the coefficient over the sphere using the explicit normalized `Y_20`; preserve the radial/time derivative terms and integrate by parts only in a separately reported, reproducible step.
8. Independently differentiate the resulting Lagrangian with respect to all derivative jets of `H0,H1,H2,K` to report the full quadratic Euler–Lagrange equations and their principal symbol.
9. Compare only after derivation against the repository table. Report term-by-term differences; never calibrate the result to an axial coefficient.

## Acceptance tests

A completed implementation must establish all of the following before the status can change:

- `BACKGROUND_CURVATURE_REPRODUCED`: at epsilon zero, the six-dimensional operator is `diag(2M/r**3,-M/r**3,-M/r**3,-M/r**3,-M/r**3,2M/r**3)` under the selected Riemann convention.
- `ANGULAR_NORMALIZATION_REPRODUCED`: `integral(Y_20**2 dOmega)=1`.
- `QUADRATIC_COEFFICIENT_EXTRACTED`: the full epsilon-squared coefficient is generated from the metric, not imported.
- `FULL_SPHERICAL_INTEGRAL_COMPLETED`: all angular terms, including derivatives of `Y_20`, are integrated.
- `FULL_QUADRATIC_ACTION_REDUCED`: all terms involving `H0,H1,H2,K` and their time/radial derivatives are present, with integration-by-parts convention recorded.
- `EULER_LAGRANGE_SYSTEM_DERIVED`: four variational equations and the principal symbol are generated from that action.
- `INDEPENDENT_REPLAY_PASSES`: a clean run reproduces canonical hashes of the action and equations.
- `CONVENTION_COMPARISON_RECORDED`: ordinary matrix trace versus unrestricted contraction is resolved from the stated physical action, not inferred from a match.

## Explicit non-claims

The previous principal-part tests are useful local checks, but they are not a complete quadratic-action derivation. The new one-component radial test is also not a substitute for this calculation. Until every acceptance test passes, the full action, its complete field equations, and any physical degree-of-freedom conclusion remain unproved.

`FRONTIER := FULL_EVEN_PARITY_QUADRATIC_ACTION_NOT_YET_DERIVED`
