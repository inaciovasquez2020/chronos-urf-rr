# Coordinate or Row Binding Certificate — 2026-06-01

## Status

`COORDINATE_ROW_BINDING_CERTIFICATE_SUPPLIED_FROM_LOCAL_NETCDF_METADATA`

## Object

`COORDINATE_OR_ROW_BINDING_CERTIFICATE`

## Decision

`PASS`

This packet records the coordinate and row binding certificate for the authenticated GRACE/GRACE-FO netCDF payload.

## Source Payload

- Dataset short name: `TELLUS_GRAC-GRFO_MASCON_CRI_GRID_RL06.3_V4`
- Granule filename: `GRCTellus.JPL.200204_202603.GLO.RL06.3M.MSCNv04CRI.nc`
- SHA256: `6554527f30e77923eae9f9793bcb315577551ad86ed763aa8a86110df463fd29`
- Byte count: `45289360`

The payload bytes are local external data and are not committed to git.

## Binding Rule

Each array row/index is bound by the ordered netCDF dimensions recorded for its variable.

Coordinate variables are bound by their own named netCDF dimensions and attributes.

Data variables are bound by their ordered dimension names and shapes.

## Resolved Missing Input

`coordinate_or_row_binding_certificate`

## Remaining Missing Inputs

1. `baseline_gravity_vector`
2. `model_or_deficit_mass_vector`
3. `unit_conversion_certificate`
4. `predeclared_comparison_metric`
5. `reproducible_comparison_run_output`

## Certified Non-Claims

This packet records:

- coordinate and row binding only;
- payload bytes are local external data and are not committed to git;
- no baseline gravity vector supplied;
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

`BASELINE_GRAVITY_VECTOR`
