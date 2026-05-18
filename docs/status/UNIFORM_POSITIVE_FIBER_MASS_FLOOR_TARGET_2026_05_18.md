# Uniform Positive Fiber-Mass Floor Target

Status: `OPEN_TARGET_SURFACE_ONLY`

Global verdict preserved: `OPEN`

This file formalizes the first global URF sink from the sink-resolution matrix.

## Formal objects

Lean module:

`Chronos.Frontier.UniformPositiveFiberMassFloorTarget`

Objects:

- `FiberMassDomain`
- `UniformPositiveFiberMassFloor`
- `NoUniformPositiveFiberMassFloorCountermodel`
- `UniformPositiveFiberMassSinkResolution`

## Closed surface theorems

- `uniform_positive_floor_closure_resolves_sink`
- `no_uniform_positive_floor_countermodel_resolves_sink`
- `countermodel_excludes_uniform_positive_floor`

## Weakest missing object

`UniformPositiveFiberMassFloor`

Minimal form:

`exists epsilon > 0 such that every admissible fiber mass is at least epsilon`

## Countermodel alternative

`NoUniformPositiveFiberMassFloorCountermodel`

Minimal form:

`an admissible positive-mass sequence with masses arbitrarily close to zero`

## Boundary

Does not prove:

- existence of `UniformPositiveFiberMassFloor`
- absence of `NoUniformPositiveFiberMassFloorCountermodel`
- finite-support-to-admissible-domain lift
- unrestricted `UniversalFiberEntropyGap`
- unrestricted Chronos-RR
- unrestricted H4.1/FGL
- P vs NP
- any Clay problem
