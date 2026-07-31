# Prizcarbon covariant odd-parity quadratic-variation target

Date: 2026-07-31

## Verified current surfaces

The encoded proposed action has type

`proposedPrizcarbonActionDensity :
  ℝ → ℝ → ProposedPrizcarbonCovariantScalars → ℝ`.

Its field argument contains these scalar summaries:

- `scalarCurvature`
- `scalarKinetic`
- `arealRadiusGradientSq`
- `arealRadius`
- `massAspect`
- `pseudoscalar`
- `multiplier`
- `currentMassDerivative`

Separately, the repository contains:

- an explicit Schwarzschild odd-parity metric perturbation;
- a gauge-invariant Regge-Wheeler master extraction;
- a CPM-derived odd-parity metric second jet.

## Missing metric-to-action map

No encoded declaration currently constructs
`ProposedPrizcarbonCovariantScalars` from the metric path

`g(ε) = g_Schwarzschild + ε h_odd`.

Consequently, the repository cannot yet compute

`d²/dε² S[g(ε)] | ε=0`

from the present action signature.

## Concrete next theorem object

Define every scalar consumed by the action as an explicit function of the
metric path, using the existing Schwarzschild background, odd-parity metric
perturbation, metric first jet, and metric second jet.

Then:

1. substitute those functions into `proposedPrizcarbonActionDensity`;
2. compute the exact second derivative with respect to `ε` at `ε = 0`;
3. eliminate nondynamical odd-parity variables through proved equations;
4. identify the surviving gauge-invariant master variable;
5. derive its Euler-Lagrange differential equation;
6. compare its potential coefficient with the proposed scalar
   mass-radius coefficient.

## Prohibited shortcuts

The target must not introduce:

- a container holding the desired master equation;
- a preselected quadratic density;
- a manually supplied potential;
- a manually supplied coefficient equality;
- an imported residual equality;
- a gravitational-instability claim.

## Boundary

The action and metric-jet surfaces are encoded, but their metric-to-scalar map
and action Hessian are absent. The covariant odd-parity reduction therefore
remains unproved.

## Closed Schwarzschild basepoint

`PrizcarbonSchwarzschildActionScalarBasePoint.lean` now constructs all eight
action-scalar values at the common Schwarzschild vacuum basepoint.

It also connects that basepoint to the background stored by:

- the existing Regge-Wheeler-gauge odd-parity metric components;
- the existing CPM third jet used for the metric second jet.

The following remain open:

- epsilon-linear metric-to-scalar contractions;
- epsilon-quadratic metric-to-scalar contractions;
- the second metric variation of the action;
- elimination of nondynamical odd-parity variables;
- derivation of the master equation from the varied action.

No perturbative coefficient or master equation is assumed by the basepoint.
