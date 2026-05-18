# Sink Closure/Countermodel Dichotomy Target

Status: `OPEN_DICHOTOMY_TARGET_SURFACE_ONLY`

Global verdict preserved: `OPEN`

This file formalizes the third global URF sink: every remaining sink must exit by either a closure certificate or a countermodel certificate.

## Lean module

`Chronos.Frontier.SinkClosureCountermodelDichotomyTarget`

## Formal objects

- `SinkResolutionProblem`
- `SinkResolved`
- `CountermodelOrClosureDichotomyTarget`
- `CountermodelOrClosureDichotomyFailure`

## Closed surface theorems

- `closure_certificate_resolves_sink`
- `countermodel_certificate_resolves_sink`
- `unresolved_sink_excludes_dichotomy`

## Weakest missing object

`CountermodelOrClosureDichotomyTarget`

Minimal form:

`For each remaining sink, provide either a named-hypothesis closure certificate or a countermodel certificate.`

## Boundary

Does not prove:

- existence of closure certificates for every sink
- existence of countermodel certificates for every sink
- `CountermodelOrClosureDichotomyTarget`
- finite-support-to-admissible-domain lift
- unrestricted `UniversalFiberEntropyGap`
- unrestricted Chronos-RR
- unrestricted H4.1/FGL
- P vs NP
- any Clay problem
