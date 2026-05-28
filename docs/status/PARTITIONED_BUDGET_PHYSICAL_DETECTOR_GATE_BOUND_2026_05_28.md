# Partitioned Budget Physical Detector Gate Bound

**Status:** `DERIVED_GATE_BOUND_FROM_PARTITIONED_BUDGET_CERTIFICATE`

## Theorem

A partitioned physical detector budget certificate consists of:

1. a finite budget assignment to detectors;
2. proof that every active physical reading is below its assigned budget;
3. proof that every active budget, multiplied by the number of active detectors, is below the extracted radius floor.

From this certificate, the restricted finite detector gate follows:

\[
extractedActiveMass(F) \le extractedRadiusFloor(F).
\]

## Why This Is Stronger Than the Previous Boundary

PR #541 closed a conditional bridge by assuming `gate_bound` directly inside admissibility.

This theorem removes that circularity at the finite detector layer.  The gate bound is no longer assumed directly.  It is derived from a finite, checkable, per-detector budget partition certificate.

## Proof Sketch

Let \(A\) be the active detector set and let \(n = |A|\).

The certificate gives:

\[
F.reading(d) \le budget(d)
\]

for every active detector \(d\), hence

\[
\sum_{d \in A} F.reading(d)
\le
\sum_{d \in A} budget(d).
\]

It also gives:

\[
budget(d)\cdot n \le extractedRadiusFloor(F)
\]

for every active detector \(d\).  Summing over active detectors gives:

\[
\sum_{d \in A} budget(d)\cdot n
\le
\sum_{d \in A} extractedRadiusFloor(F).
\]

The left side factors as

\[
\left(\sum_{d \in A} budget(d)\right)n
\]

and the right side is

\[
n\cdot extractedRadiusFloor(F).
\]

If \(n = 0\), the active mass is zero.  If \(n > 0\), canceling \(n\) gives:

\[
\sum_{d \in A} budget(d)
\le
extractedRadiusFloor(F).
\]

Therefore:

\[
extractedActiveMass(F)
\le
extractedRadiusFloor(F).
\]

## Concrete Instance

The module includes a two-detector example:

- two active detectors;
- reading \(1\) at each detector;
- radius \(6\) at each detector;
- budget \(2\) at each detector.

Since there are two active detectors,

\[
2 \cdot 2 \le 6.
\]

The gate closes by the derived theorem.

## Boundary

This artifact proves a finite partitioned-budget gate-bound theorem.

It does not prove:

- existence of a partitioned budget certificate for arbitrary physical detector fields;
- derivation of partitioned budget certificates from continuum GR data;
- arbitrary physical detector fields are admissible;
- physical detector-field extraction for continuum GR data;
- Einstein-matter PDE well-posedness;
- trapped-surface formation theorem;
- black-hole formation theorem;
- cosmic censorship proof;
- hoop conjecture proof;
- unrestricted `QL_CollapseGate`;
- unrestricted `UniversalBoundaryCompactness`;
- unrestricted `Chronos-RR`;
- unrestricted `H4.1/FGL`;
- `P vs NP`;
- any Clay problem.
