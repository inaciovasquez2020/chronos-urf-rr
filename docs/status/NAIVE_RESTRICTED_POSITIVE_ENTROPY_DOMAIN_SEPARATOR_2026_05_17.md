# Naive Restricted Positive-Entropy Domain Separator

Status: NEGATIVE_CLOSURE_ONLY

## Solved mathematical part

The naive restricted-domain route is refuted.

A construction of the form

- choose a nonempty restricted domain;
- map every restricted-domain element into the unrestricted witness type;

immediately reconstructs the already-refuted unrestricted positive-entropy uniform witness construction.

Lean theorem:

- `naiveRestrictedPositiveEntropyDomainConstruction_refuted`

Lean definition:

- `NaiveRestrictedPositiveEntropyDomainConstruction`

## Remaining admissible frontier

A viable restricted positive-entropy route must use a genuinely domain-indexed witness object, not a map into the refuted unrestricted witness type.

## Boundary

Negative closure only.

Does not prove:

- genuine restricted positive-entropy domain construction
- domain-indexed positive-entropy witness construction
- unrestricted RateThickFiberCoercivity λ
- unrestricted UniversalFiberEntropyGap
- unrestricted Chronos-RR
- H4.1/FGL
- P vs NP
- any Clay problem
