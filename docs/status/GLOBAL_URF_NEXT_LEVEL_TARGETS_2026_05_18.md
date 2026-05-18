# Global URF Next-Level Targets

Status: `NEXT_LEVEL_TARGET_SURFACE_ONLY`

Global verdict preserved: `OPEN`

This file converts the current audit, numeric snapshot, and dependency-DAG sink obstacles into ranked next proof targets.

## Snapshot inputs

- Total claims tracked: `4`
- Proved surface: `25%`
- Conditional: `25%`
- Open / countermodel-needed: `50%`
- Dependency-DAG sink obstacles: `3`
- Boundary warnings: `5`
- Tests passed after numeric snapshot: `961`
- Tests passed after dependency DAG: `964`

## Ranked next targets

### 1. Uniform positive mass or countermodel

Weakest sufficient next ingredient:

`Either prove a uniform positive fiber-mass/coercivity floor on the intended admissible domain, or construct a countermodel showing no such floor exists.`

Blocks:

- restricted `UniversalFiberEntropyGap` expansion
- restricted Chronos-RR expansion
- selected-domain H4.1/FGL expansion

### 2. Domain lift from finite support

Weakest sufficient next ingredient:

`Prove that the finite-support positive-mass domain embeds into the next intended admissible Chronos domain without losing the uniform floor.`

Blocks:

- finite-support-to-admissible-domain transfer
- admissible restricted Chronos-RR strengthening

### 3. Countermodel or closure dichotomy

Weakest sufficient next ingredient:

`For each remaining open sink, add either a Lean/Python-checkable closure theorem under explicit hypotheses or a machine-checkable countermodel schema.`

Blocks:

- audit-to-resolution conversion
- sink-obstacle elimination accounting

## Boundary

Does not prove:

- unrestricted `UniversalFiberEntropyGap`
- unrestricted Chronos-RR
- unrestricted H4.1/FGL
- P vs NP
- any Clay problem
