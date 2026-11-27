# Minkowski three-event distribution

Status: LEAN_VERIFIED

This standalone certificate establishes exact three-event
causal probabilities for the specified four-dimensional
Minkowski causal diamond and a quantitative obstruction
for the specified common-scalar prefix statistic.

## Exact distribution

| Configuration | Probability |
|---|---:|
| Antichain | 53/70 |
| Single comparable pair | 33/175 |
| V | 9/350 |
| Inverted V | 9/350 |
| Chain | 1/350 |

## Load-bearing declarations

- Chronos.ThreeDistribution.distribution
- Chronos.ThreeDistribution.physical_prefix_gap
- Chronos.ThreeDistribution.coherent_prefix_obstruction

Two-event comparability: 1/10.

Specified physical prefix statistic: 16/175.

Exact discrepancy: 3/350.

## Verification

- Lean compilation: PASS
- Axiom audit: 111 declarations
- Allowed axioms: propext, Classical.choice, Quot.sound
- Unauthorized axioms: zero
- Linter warnings: zero
- Directed configurations: 64
- Strict partial orders: 19
- Generator reproducibility: PASS

From the repository root:

    lake env lean research/certificates/minkowski_three_distribution_20261126/MinkowskiThreeDistribution.lean

To reproduce the generated source, copy GeneratorBase.lean
to a temporary file, execute generate_partition.py with
that file as its argument, and compare the resulting file
against MinkowskiThreeDistribution.lean.

## Scope restrictions

The prefix statistic is the specific expression defined
by physicalPrefix in the Lean source. It is not the
ordinary two-point marginal of an IID three-point sample.

The obstruction does not disprove relativity, establish
spacetime emergence, or exclude all event-first models.

Independent mathematical novelty is not established.
