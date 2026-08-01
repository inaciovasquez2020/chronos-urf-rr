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

## Closed scalar-curvature first-variation formula

`PrizcarbonOddParityLinearizedScalarCurvature.lean` now defines:

- the background Ricci contraction from the existing Schwarzschild Riemann;
- the odd-parity linearized Ricci contraction from the existing linearized
  Riemann;
- the inverse-metric-variation contribution
  `δg^{μν} R̄_{μν}`;
- the Ricci-variation contribution
  `ḡ^{μν} δR_{μν}`;
- their sum as the complete scalar-curvature first variation.

The contraction is not defined to be zero.

Still open:

- prove the contraction vanishes for the concrete vacuum odd-parity CPM jet,
  or compute its nonzero value if it does not vanish;
- derive the remaining seven action-scalar first variations;
- derive all second variations;
- form the action Hessian;
- eliminate nondynamical variables and derive the master equation.

## Closed vacuum CPM scalar-curvature specialization

`PrizcarbonOddParityVacuumCPMLinearizedScalarCurvature.lean` now evaluates
the general scalar-curvature first-variation contraction on:

- `reggeWheelerOddParityVacuumCPMDerivedMetricFirstJet`;
- `reggeWheelerSchwarzschildConnectionFirstJetOfFrame`;
- `reggeWheelerOddParityVacuumCPMDerivedLinearizedConnectionFirstJet`.

It specializes both product-rule contributions and the first-order epsilon
polynomial. The contraction is not declared to vanish.

Still open:

- componentwise simplification of both specialized Ricci contributions;
- proof or disproof that their exact sum vanishes;
- the other seven action-scalar first variations;
- every second variation;
- the action Hessian and master-equation derivation.

## Closed Schwarzschild Ricci contribution

`PrizcarbonSchwarzschildRicciContractionZero.lean` proves componentwise that
the explicit Schwarzschild Ricci contraction vanishes on the certified
exterior static frame.

Consequently, the `δg^{μν} R̄_{μν}` contribution vanishes, and the concrete
vacuum CPM scalar-curvature variation reduces exactly to
`ḡ^{μν} δR_{μν}`.

The CPM-derived linearized Ricci contraction remains open.
