# Carbon specimen measurement acquisition protocol

Sample ID: `CARBON-20260718T151252Z-001`

This protocol prepares the missing same-specimen measurement bundle. It does
not create or infer physical measurements.

## Specimen identity

The physical specimen, CT files, stress files, calibration records, and mass
record must all carry the exact identifier:

`CARBON-20260718T151252Z-001`

## Required metadata

Record these values in `sample_metadata.json`:

- exact carbon grade or composition;
- measurement status: `MEASURED`;
- shape: `sphere`;
- calibrated mass and standard uncertainty in kilograms;
- calibrated radius and standard uncertainty in metres;
- specimen temperature and standard uncertainty in kelvin;
- observer radius and standard uncertainty in metres;
- CT instrument manufacturer and model;
- CT calibration identifier and date;
- density calibration method;
- residual-stress instrument manufacturer and model;
- stress calibration identifier and date;
- actual acquisition timestamp with timezone;
- traceable provenance description.

## CT-density profile

Export at least four radial measurements to `ct_density.csv`.

Required columns:

`r_m,rho_kg_m3,rho_uncertainty_kg_m3`

Requirements:

- radii begin at or near the specimen centre;
- radii are strictly increasing;
- final radius agrees with the metadata radius;
- density is positive and finite;
- uncertainty is nonnegative and finite;
- every row comes from this specimen.

## Residual-stress profile

Export at least four radial measurements to `residual_stress.csv`.

Required columns:

`r_m,sigma_rr_pa,sigma_tt_pa,sigma_rr_uncertainty_pa,sigma_tt_uncertainty_pa`

Requirements:

- radii are strictly increasing;
- radial and tangential stresses are in pascals;
- signed compressive or tensile values are preserved;
- uncertainty columns are nonnegative and finite;
- every row comes from this specimen.

## Acceptance boundary

Do not mark the bundle complete unless the physical specimen and every
measurement record use the same sample ID. Do not substitute nominal material
properties, handbook values, simulated profiles, or values from another
specimen.
