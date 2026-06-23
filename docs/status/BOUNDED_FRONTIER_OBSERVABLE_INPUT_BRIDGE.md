# Bounded Frontier Observable Input Bridge

Status: `BRIDGE_INPUTS_ONLY`

## Selected observable target

`finite_radial_signal_travel_time_bound`

This page records one narrow frontier-observable-style bridge with the same bounded shape as the fixed Ohm's Law observation demo:

```text
finite declared inputs
-> computed scalar
-> tolerance check
-> explicit non-claim boundary
Observable map
delta_t_expected := radius_meters / signal_speed_meters_per_second
For each listed finite observation, the verifier checks:
abs(delta_t_seconds - delta_t_expected) / delta_t_expected <= relative_tolerance
The current tolerance is 0.005.
WHAT_THIS_DOES
Records one bounded bridge-input artifact.
Checks finite positive input values.
Checks a declared time-of-flight scalar against a declared computation rule.
Copies the bounded-observable pattern of the Ohm's Law fixed-observation demo.
WHAT_THIS_DOES_NOT_CLAIM
Does not claim quantum gravity closure.
Does not claim empirical prediction discharge.
Does not claim scientific validation.
Does not claim a completed physics theory.
Does not claim mainstream acceptance.
Does not claim that compilation proves physical truth.
Boundary
This is an input-bridge verifier only. It checks artifact shape, finite numeric inputs, tolerance arithmetic, and required non-claim language. It does not validate a physical theory.
