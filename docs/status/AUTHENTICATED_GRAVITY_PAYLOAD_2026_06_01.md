# Authenticated Gravity Payload — 2026-06-01

## Status

`AUTHENTICATED_PO_DAAC_GRACE_GRACE_FO_MASCON_PAYLOAD_DIGEST_BOUND_LOCAL_BYTES_NOT_COMMITTED`

## Object

`AUTHENTICATED_GRAVITY_PAYLOAD`

## Decision

`PASS`

This packet records the authenticated GRACE/GRACE-FO gravity payload digest.

## Source

- Source agency: `NASA/JPL PO.DAAC`
- Provider: `POCLOUD`
- Mission: `GRACE/GRACE-FO`
- Dataset short name: `TELLUS_GRAC-GRFO_MASCON_CRI_GRID_RL06.3_V4`
- Granule filename: `GRCTellus.JPL.200204_202603.GLO.RL06.3M.MSCNv04CRI.nc`
- Payload format: `netCDF`

## Local Payload

`external_payloads/gravity/download/GRCTellus.JPL.200204_202603.GLO.RL06.3M.MSCNv04CRI.nc`

The payload bytes are local external data and are not committed to git.

## Digest

`6554527f30e77923eae9f9793bcb315577551ad86ed763aa8a86110df463fd29`

## Byte Count

`45289360`

## Resolved Missing Input

`authenticated_gravity_payload`

## Remaining Missing Inputs

1. `coordinate_or_row_binding_certificate`
2. `baseline_gravity_vector`
3. `model_or_deficit_mass_vector`
4. `unit_conversion_certificate`
5. `predeclared_comparison_metric`
6. `reproducible_comparison_run_output`

## Certified Non-Claims

This packet records:

- payload bytes are local external data and are not committed to git;
- no coordinate or row binding certificate supplied;
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

`COORDINATE_OR_ROW_BINDING_CERTIFICATE`
