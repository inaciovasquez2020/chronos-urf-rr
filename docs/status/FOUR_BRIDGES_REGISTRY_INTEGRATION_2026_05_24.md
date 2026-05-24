# Four Bridges Source registry integration

Status: `FOUR_BRIDGES_REGISTRY_INTEGRATION_CONDITIONAL_EXTERNAL_ONLY`.

This record wires 4bS into the registry layer without declaring any active native registry instance.

Native finished theorem layer:

- `R1FinishedTheorem`
- `R2FinishedTheorem`
- `R3FinishedTheorem`

Native theorem proofs:

- `R1FinishedTheorem_proved`
- `R2FinishedTheorem_proved`
- `R3FinishedTheorem_proved`

Bridge source:

- `FourBridgesSource`

Registry class:

- `URF11BridgeRegistry`

Extraction surfaces:

- `R1_from_4bS`
- `R2_from_4bS`
- `R3_from_4bS`
- `RepositoryNativeR1R2R3InstanceTarget_from_4bS`
- `R4_from_4bS`
- `CompleteOpaqueSystem_conditional_on_4bS`
- `R1_registered_extraction`
- `R2_registered_extraction`
- `R3_registered_extraction`
- `R4_registered_extraction`
- `CompleteOpaqueSystem_registered`

Policy:

External 4bS certification supplies the `URF11BridgeRegistry` instance.

Rejected paths:

- native active registry instance
- global bridge declaration
- macro or meta-program injection
- unconditional opaque-target closure without 4bS

Boundary:

- does not provide an active URF11BridgeRegistry instance
- does not prove unconditional opaque R1
- does not prove unconditional opaque R2
- does not prove unconditional opaque R3
- does not prove unconditional R4
- does not prove unconditional NON_FACTORISATION
- does not prove Chronos-RR
- does not prove H4.1/FGL
- does not prove P vs NP
- does not prove any Clay problem
