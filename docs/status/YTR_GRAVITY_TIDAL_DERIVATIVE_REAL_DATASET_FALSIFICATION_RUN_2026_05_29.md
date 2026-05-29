# YtR Gravity Tidal Derivative Real Dataset Falsification Run

Status: `REAL_DATA_FALSIFICATION_GATE_ONLY`.

This object replaces the elastic-language coefficient `K_g` with `tidalDerivativeCoefficient`, interpreted as the radial gravity gradient `dg/dr`.

It replaces normalized toy constants with Earth-scale constants:

```text
g0 = 9.80665 m/s^2
R  = 6371000 m
dg/dr = -2*g0/R = -1961330 / 637100000000 s^-2
It binds the first public dataset target:
GRACEFO_L2_JPL_MONTHLY_0063
NASA PO.DAAC / JPL
GRACE-FO Level-2 Monthly Geopotential Spherical Harmonics JPL RL06.3
It defines the comparison metric:
observable = radial_gravity_gradient_dg_dr
baseline   = standard_GR_or_Newtonian_geodesy_prediction
domain     = GRACEFO_L2_JPL_MONTHLY_0063_public_payload
tolerance  = measurement_uncertainty_plus_model_error_bound
It defines the falsification path:
pass = candidate_error < baseline_error under declared tolerance
fail = candidate_error >= baseline_error or no nontrivial residual survives uncertainty
Boundary:
No empirical execution.
No measured result.
No GR failure claim.
No new gravity claim.
No dark matter replacement claim.
No Lambda-CDM failure claim.
No quantum gravity proof.
No Clay problem claim.
