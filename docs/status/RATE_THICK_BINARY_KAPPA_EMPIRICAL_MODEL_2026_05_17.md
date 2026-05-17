# Rate-Thick Binary Kappa Empirical Model

Status: EMPIRICAL_MODEL_ONLY / NO_THEOREM_PROMOTION

## Empirical findings

- Binary kappa positivity passed on the sample.
- Train-minimum kappa domination failed on holdout.
- Holdout-safe alpha passed only after empirical slack.
- LOOCV detected one train-minimum domination failure.
- Observed maximum slack required: `0.016941176470588237`.

## Recorded values

- `alpha_train_min = 1.0196078431372548`
- `alpha_holdout_safe = 1.0026666666666666`
- `delta_loocv = 0.016380952380952385`
- `delta_holdout = 0.016941176470588237`
- `delta_observed_max = 0.016941176470588237`
- `epsilon_train_min = 0.05`

## Boundary

Empirical comparison only.

Does not prove:

- entropy-minimum domination
- ratio stability
- uniform fiber-mass bound
- unrestricted certificate construction
- unrestricted RateThickFiberCoercivity
- unrestricted UniversalFiberEntropyGap
- unrestricted Chronos-RR
- H4.1/FGL
- P vs NP
- any Clay problem
