# GRACEFO Schema Validation Execution Result — 2026-05-29

Status: `GRACEFO_SCHEMA_VALIDATION_EXECUTION_RESULT_CREATED`

Input artifact:

`artifacts/gracefo/authenticated_gracefo_payload_digest_certificate_2026_05_29.json`

Validated dataset:

`GRACEFO_L2_JPL_MONTHLY_0063`

Validated requirements:

- digest artifact exists;
- dataset short name matches the GRACEFO target;
- collection SHA256 is present;
- payload files exist locally;
- local file sizes match the digest certificate;
- local file SHA256 values match the digest certificate;
- two monthly periods are present;
- each period contains the required JPL monthly products:
  - `GAA BC01`
  - `GAB BC01`
  - `GAC BC01`
  - `GAD BC01`
  - `GSM BA01`
  - `GSM BB01`

Boundary:

- schema validation execution result only;
- no real GRACEFO tidal-derivative model execution yet;
- no empirical residual result;
- no GR failure claim;
- no new gravity claim;
- no dark matter replacement claim;
- no Lambda-CDM failure claim.
