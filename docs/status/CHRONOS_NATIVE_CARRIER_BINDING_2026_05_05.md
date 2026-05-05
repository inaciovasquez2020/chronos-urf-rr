# Chronos Native Carrier Binding

Status: CONDITIONAL_NATIVE_BINDING_INTERFACE

## Closed Surface

This artifact defines a conditional native-carrier binding interface.

Closed Lean objects:

- `CPDLGate`
- `ValidChr`
- `MissingCPDLCCSLWitness`
- `NativeCarrierBinding`
- `nativeBindingCPDL`
- `nativeBindingEmbed`
- `nativeBindingEmbed_injective`
- `nativeBinding_missingCPDLCCSLWitness`
- `nativeBinding_validity`

## Binding Requirement

A native carrier is sufficient if it supplies:

```lean
encode : (n : Nat) -> (Fin n -> Bool) -> { t : TNative n // pNative n t }
decode : (n : Nat) -> { t : TNative n // pNative n t } -> (Fin n -> Bool)
decode_encode : forall n x, decode n (encode n x) = x
Boundary
This is a conditional native-binding interface only.
This does not construct the actual native Chronos certificate carrier.
This does not define `C_n^Chr`.
This does not define `nu_n`.
This does not prove the entropy bridge.
This does not prove ChronosCertificateEmbedding.
This does not prove H4.1/FGL theorem closure.
This does not prove P vs NP closure.
