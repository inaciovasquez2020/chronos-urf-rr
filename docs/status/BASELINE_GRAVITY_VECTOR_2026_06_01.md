# Baseline Gravity Vector — 2026-06-01

## Status

`BASELINE_GRAVITY_VECTOR_SUPPLIED_FROM_AUTHENTICATED_NETCDF_PAYLOAD_DETERMINISTIC_FINITE_SAMPLE`

## Object

`BASELINE_GRAVITY_VECTOR`

## Decision

`PASS`

This packet records a deterministic finite baseline gravity vector extracted from the authenticated GRACE/GRACE-FO netCDF payload.

## Source Payload

- Dataset short name: `TELLUS_GRAC-GRFO_MASCON_CRI_GRID_RL06.3_V4`
- Granule filename: `GRCTellus.JPL.200204_202603.GLO.RL06.3M.MSCNv04CRI.nc`
- SHA256: `6554527f30e77923eae9f9793bcb315577551ad86ed763aa8a86110df463fd29`
- Byte count: `45289360`

The payload bytes are local external data and are not committed to git.

## Vector Rule

Flatten the finite entries of the selected baseline variable in netCDF storage order after excluding NaN, infinity, `_FillValue`, and `missing_value`.

Select evenly spaced sample indices across the finite flattened vector using:

`numpy.linspace(0, finite_value_count - 1, min(4096, finite_value_count), dtype=int64)`

## Resolved Missing Input

`baseline_gravity_vector`

## Remaining Missing Inputs

1. `model_or_deficit_mass_vector`
2. `unit_conversion_certificate`
3. `predeclared_comparison_metric`
4. `reproducible_comparison_run_output`

## Certified Non-Claims

This packet records:

- baseline gravity vector only;
- deterministic finite sample only;
- payload bytes are local external data and are not committed to git;
- no model or deficit-mass vector supplied;
- no unit conversion certificate supplied;
- no predeclared comparison metric supplied;
- no reproducible comparison run output supplied;
- no empirical gravity result supplied;
- no anomaly detection result;
- no model-favored result;
- no baseline-favored result;
- no DFM-MKC validation;
- no Lambda-CDM failure;
- no dark matter resolution;
- no dark energy resolution;
- no physical discovery claim;
- no Chronos-RR closure;
- no H4.1/FGL closure;
- no P vs NP claim;
- no Clay-problem claim.

## Next Admissible Object

`MODEL_OR_DEFICIT_MASS_VECTOR`
