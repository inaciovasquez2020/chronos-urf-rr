# R1 Native-Map Conditional Contract Constructor Status

Status: `R1_NATIVE_MAP_CONDITIONAL_CONTRACT_CONSTRUCTOR_STATUS`

Date: 2026-06-22

Input head: `dc451809`

## Constructor

`r1_concrete_newstein_fgl_to_native_map_input_contract_from_aligned_discharge_targets`

## Aligned input shape

`R1ConcreteNewsteinFGLToNativeMapAlignedDischargeTargets`

## Status

This is a conditional constructor only.

It assembles a full `R1ConcreteNewsteinFGLToNativeMapInputContract` after all
four evidence-bearing discharge targets have already been supplied and aligned
to the same concrete source object.

## Boundary

The full native-map input contract is not discharged unconditionally.

The unconditional non-factorization theorem is not proved.

The constructor does not supply:

1. compatibility invariant evidence;
2. diameter-separation filling-obstruction evidence;
3. uniform local-type capacity evidence.

## Preserved target projections

- `r1_native_map_input_contract_from_aligned_targets_long_chord_eq`
- `r1_native_map_input_contract_from_aligned_targets_diameter_eq`
- `r1_native_map_input_contract_from_aligned_targets_uniform_eq`
- `r1_native_map_input_contract_from_aligned_targets_compatibility_eq`

## Next bounded improvement

Connect the conditional constructor status back into the main decomposition
status without changing the missing-evidence boundary.
