# Chronos Repository Native Carrier Iso

Status: CONDITIONAL_REPOSITORY_NATIVE_ISO_INTERFACE

## Closed Surface

This artifact defines the conditional interface needed to transfer the model native trace carrier into a repository-native carrier.

Closed Lean objects:

- `CPDLGate`
- `ValidChr`
- `MissingCPDLCCSLWitness`
- `ModelTraceCarrier`
- `modelTracePredicate`
- `modelTraceEncode`
- `modelTraceDecode`
- `modelTraceDecodeEncode`
- `RepositoryNativeCarrierIso`
- `repoCPDL`
- `repoEmbed`
- `repoEmbed_injective`
- `repo_missingCPDLCCSLWitness`
- `repo_validity`

## Required Missing Object

The remaining object is an actual repository instance:

```lean
RepositoryNativeCarrierIso TRepo
for the real repository-native Chronos certificate carrier TRepo.
Boundary
This is a conditional repository-native iso interface only.
This does not construct the actual repository-native Chronos certificate carrier.
This does not identify any existing repository certificate type with `ModelTraceCarrier`.
This does not define `C_n^Chr`.
This does not define `nu_n`.
This does not prove the entropy bridge.
This does not prove ChronosCertificateEmbedding.
This does not prove H4.1/FGL theorem closure.
This does not prove P vs NP closure.
