# Chronos H4.1/FGL Observation Extraction Witness Interface — 2026-05-10

Status: WITNESS_INTERFACE_ONLY

## Input frontier

`H4_1_FGL_FinalCarrierObservationExtraction`

## New weakest missing object

`H4_1_FGL_MissingObservationExtractionWitness`

## Required witness fields

- `selected_final_carrier_domain`
- `observation_map_exists`
- `observation_separates_final_carrier_gap`
- `observation_preserves_selected_carrier_soundness`

## Reduction

A complete observation-extraction witness implies the final-carrier observation extraction target.

## Boundary

- This is a reduction interface only.
- It does not construct the observation-extraction witness.
- It does not prove final selected-carrier soundness.
- It does not prove unrestricted H4.1/FGL closure.
- It does not prove UniversalFiberEntropyGap.
- It does not prove Chronos-RR.
- It does not prove P vs NP or any Clay-problem closure.
