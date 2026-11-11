# Chronos–URF–RR: replica-overlap criterion (2026-11-11)

## Scope
For a finite poset P of size N, independently choose two uniform linear extensions and retain their first n elements as ideals I and J. Conditional on P, write q(x)=Pr(x in I | P), and let

R(P,n) = min_{A ideal} E[|I △ A| | P] = Σ_x min(q(x),1-q(x)),
D(P,n) = E[|I △ J| | P] = 2 Σ_x q(x)(1-q(x)).

## Theorem — exact comparison

D(P,n)/2 ≤ R(P,n) ≤ D(P,n).

Proof: For 0≤q≤1, q(1-q) ≤ min(q,1-q) ≤ 2q(1-q). Sum over all elements. The minimizer is the threshold {q>1/2}, which is an ideal by q(x)≥q(y) whenever x≺y.

For an optimal deterministic ideal A of cardinality n, with R_n(P,n) = min_{|A|=n, A ideal} E[|I △ A| | P],

D(P,n)/2 ≤ R(P,n) ≤ R_n(P,n) ≤ D(P,n).

The upper bound follows because sampling J independently gives a random size-n ideal with average loss D; a deterministic size-n ideal attains no greater loss. The minimizing size-n ideal consists of the n highest q-values, taking predecessors first when tied.

Thus, for any sequence of random finite posets P_N and n_N>0, the following are equivalent:
E[R(P_N,n_N)]/n_N → 0,
E[R_n(P_N,n_N)]/n_N → 0,
E[D(P_N,n_N)]/n_N → 0.

The equivalence holds with no geometry, covariance, or dimension assumptions, and is a concentration criterion only for deterministic-ideal approximation *conditional on the poset*. It does not imply/require Minkowski sampling statistics.

## Alternative representation

Let O(P,n)=E[|I∩J| | P]. Then O=Σ_x q(x)^2 and

D=2(n-O).

Hence deterministic-ideal concentration iff E[O]/n →1. This avoids selecting a geometric region and permits independent simulation of replicas if exact ideal-lattice dynamic programming is too expensive.

## Exact-rational validation

Standalone standard-library script `chronos_replica_overlap_audit.py`, seeded 20261111. Exhaustive verification of all transitive closures of forward-edge configurations of N=2..5, for each 1≤n<N: 4306 cases, including an independent enumeration of all linear extensions. PASS.

Four-dimensional causal-diamond numerical sprinklings (floating-point coordinates, exact rational conditional linear-extension weights):

| N | n | replicas | unconstrained R/n | fixed-size R_n/n | D/n |
|---:|---:|---:|---:|---:|---:|
| 8 | 4 | 60 | 0.756026 | 0.757901 | 0.834019 |
| 12 | 6 | 60 | 0.693770 | 0.695258 | 0.794445 |
| 16 | 8 | 40 | 0.676126 | 0.678124 | 0.779337 |

These values are mean Monte Carlo estimates; sample-level algebra is exact conditional on floating-point-generated posets. The computation does not establish any asymptotic lower bound.

## Boundary

- PROVED: exact replica-overlap comparison and asymptotic equivalence of the three normalized concentration criteria.
- COMPUTATION_PASS: 4306 exhaustive checks, and bounded simulated sprinklings through N=16.
- OPEN: asymptotic normalized replica disagreement for uniform linear extensions of four-dimensional sprinkled diamonds.
- OPEN: uniform-tail Minkowski sampling convergence, intrinsic metric-free selecting law, gravitational dynamics.
- NOT_RUN: repository Lean compilation / axiom audit.

Repository retained untouched, intended checkpoint `abef2b3e61dcb24a3ebb65ad0df7a76f63d4869f` from PR #1347; no local HEAD/dirty-state inspection.

## Literature context
Rank-probability calculation via ideal lattices is established: De Loof, De Meyer, De Baets, *Exploiting the Lattice of Ideals Representation of a Poset* (2006). Order-invariant measures: Brightwell and Luczak (2009/2011, 2012). Novelty of this elementary overlap inequality is NOT ESTABLISHED.