# Causal-order / URF observation-fiber obstruction from chains and forks

**Status:** Elementary proof below (PROVED as a paper argument; independent review pending); bounded exhaustive audit COMPUTATION_PASS in an isolated Linux environment; Lean NOT_RUN; novelty NOT_ESTABLISHED. No spacetime or fifth-dimensional physical derivation.

## Definitions and exact formulas

Let P be a finite causal poset. C_k(P) counts k-element total-chain subsets. F(P) counts triples (x,y,z) satisfying x<y, x<z and y incomparable with z; the pair {y,z} is unordered.

Write P(a_1,...,a_m) for the ordinal sum of nonempty antichains A_{a_1} ⊕ ... ⊕ A_{a_m}. Two distinct elements are incomparable precisely when they belong to the same block. Hence the ordered block-size sequence is an isomorphism invariant.

Every chain chooses at most one event from each level, giving

    sum_{k>=0} C_k(P) t^k = product_j (1+a_j t).

For a fork, the two incomparable upper elements lie in level j and the common lower element lies in an earlier level. Therefore

    F(P) = sum_j (sum_{i<j} a_i) * binomial(a_j,2).

These identities are elementary, unrestricted across ordinal sums of finite nonempty antichains.

## Exact six-event collision

Take P=P(1,2,2,1) and Q=P(2,1,1,2).

    (C1,C2,C3,C4,C5,C6)(P) = (6,13,12,4,0,0)
    (C1,C2,C3,C4,C5,C6)(Q) = (6,13,12,4,0,0)
    F(P) = F(Q) = 4.

The posets are not isomorphic: the minimal level contains one event in P and two in Q. In general, all levels are definable as incomparability equivalence classes and their temporal ordering is intrinsic.

Let O map a finite causet isomorphism class to its full chain-count vector and F statistic; let I be the causal-order isomorphism class. Because O(P)=O(Q) while I(P)≠I(Q), **no exact deterministic decoder D with D∘O=I can exist** on any class containing both. This directly instantiates the abstract URF observation-fiber obstruction. It does not rule out recovery with additional observables, restrictive dynamics, or a continuum-limit law.

A smaller positive example illustrates the value (but insufficiency) of the fork statistic: P(2,1) and P(1,2) have identical global chain counts (3,2,0) while F=0 and F=1, respectively.

## Bounded minimality: only the ordinal-sum family

The accompanying standard-library verifier independently enumerates (1) every ordered positive composition of n, (2) all chain subsets and fork triples from the actual strict order, and (3) the polynomial/fork formulas. For n=1,...,6 the number of compositions is (1,2,4,8,16,32); the number of different combined signatures is (1,2,4,8,16,31). The sole collision at n=6 is the displayed pair. This does **not** claim minimality among arbitrary six-element or smaller finite posets.

## Reproduction and evidence boundary

    PYTHONDONTWRITEBYTECODE=1 python3 tools/verifier/event_chain_fork_urf_obstruction.py

Expected completion marker: RESULT := COMPUTATION_PASS. Optimized Python is rejected. The exact finite check validates the formulas and enumerated signatures, not an unrestricted physical law or independent Lean proof.

The related Chronos event-first calculation is staged at PR #1345, while the URF abstract factorization/collision work is staged at URF Core PR #592. Neither draft is assumed merged here. The general manifoldlikeness, 4D continuum reconstruction, Einstein dynamics, and necessity of a physical fifth dimension remain OPEN.
