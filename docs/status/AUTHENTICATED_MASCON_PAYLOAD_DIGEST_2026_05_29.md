# Authenticated MASCON Payload Digest — 2026-05-29

Status: `AUTHENTICATED_MASCON_PAYLOAD_DIGEST_BOUND_BYTES_NOT_COMMITTED`

This closes the digest-certificate object after `MASCON_PAYLOAD_DIGEST_CERTIFICATE_2026_05_29`.

## Closed object

- `AUTHENTICATED_MASCON_PAYLOAD_BYTES_AND_SHA256_DIGEST`

## Bound fields

- `payload_bytes_bound: true`
- `digest_bound: true`
- `payload_bytes_committed_to_git: false`

## Artifact

- `artifacts/gravity/authenticated_mascon_payload_digest_2026_05_29.json`

## Boundary

This is a digest certificate only. Payload bytes are locally hashed but not committed to git. CI verifies the committed digest manifest and collection hash without requiring the local payload bytes to be present. This does not execute MASCON schema validation, execute model comparison, assert an empirical gravity result, assert GR failure, assert new gravity, assert dark matter replacement, assert Lambda-CDM failure, assert quantum gravity, or assert any Clay-problem closure.

## Next admissible object

- `MASCON_SCHEMA_VALIDATION_EXECUTION_RESULT`
