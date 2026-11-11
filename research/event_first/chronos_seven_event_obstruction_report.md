# Chronos causal-event finite-horizon audit — seven-event obstruction

Status: finite classification COMPUTATION_PASS using exact Fraction arithmetic; conditional finite no-go PROVED from exhaustive enumeration; Lean NOT_RUN; physical spacetime emergence OPEN. No Git modifications.

Reference: `inaciovasquez2020/chronos-urf-rr`, preserved remote PR #1347 SHA `abef2b3e61dcb24a3ebb65ad0df7a76f63d4869f` (not local HEAD).

## Six-event terminal probability law

Select the following unlabeled 6-poset, then uniformly select one of its linear extensions as birth labeling:

- Antichain `(0,0,0,0,0,0)` with probability `37/70`.
- Branching poset `(0,0,1,2,5,10)` with probability `1/35`.
- Three disjoint two-chains `(0,0,0,1,2,4)` with probability `31/70`.

The tuples record predecessor bitsets, with event labels 0...5. This is a terminal-distribution construction, not a fundamental gravitational law. Independently enumerating all 720 permutations (and filtering linear extensions) establishes exactly:

- expected comparable-pair fraction `1/10` for `N=2,...,6`;
- expected three-chain fraction `1/350` for `N=3,...,6`;
- expected induced-2+2 fraction `37/350` for `N=4,...,6`.

The distribution has consistent prefix marginals and satisfies discrete general covariance through six births. It does not match the complete Minkowski causal-set distributions, only these few moments.

## Exhaustive seventh-event classification

There are 26 supported naturally labeled six-poset states. Adding an arbitrary ideal as predecessor set of a seventh event produces 629 distinct naturally labeled candidate seven-posets. For a seven-poset to have positive mass under discrete general covariance, *every* natural labeling must have a supported six-prefix; equivalently deleting every maximal element must yield one of the three six-poset isomorphism classes. Exactly 27 candidates survive, in four unlabeled isomorphism classes:

1. Seven-antichain (one labeled order), whose six-prefix is the antichain.
2. Cone over six-antichain (one labeled order), whose six-prefix is the antichain.
3. Cone over branching (ten labeled orders), whose six-prefix is branching.
4. Cone over three disjoint edges (15 labeled orders), whose six-prefix is three disjoint edges.

The probability masses of classes 3 and 4 are therefore fixed at `1/35` and `31/70`. Mass `37/70` may be split arbitrarily between classes 1 and 2. The exact seven-event conditional feature vectors `(P2,P3,P22)` are:

- antichain: `(0,0,0)`;
- antichain cone: `(2/7,0,0)`;
- branching cone: `(4/7,8/35,9/35)`;
- matching cone: `(3/7,3/35,3/35)`.

Thus every discretely generally covariant seventh-event extension of **this particular six-terminal law** satisfies the **sharp** exact bounds and equality

`101/490 <= E[P2(7)] <= 5/14`,

`E[P3(7)] = 109/2450`,

`E[P22(7)] = 111/2450`.

Sharp endpoints of the pair range are realized by placing all antichain mass on the seven-antichain or its cone. Since `101/490 > 1/10` and `109/2450 > 1/350`, none preserve the two Minkowski reference moments at size seven. The exact, smaller earlier five-terminal obstruction remains a separate result, and neither result excludes all other terminal distributions.

## Reproducibility

Run `python3 /mnt/data/chronos_three_class_exact_check.py` for an independent 2–6 exact moment and 51 positive-square audit. Run `python3 /mnt/data/chronos_seven_event_exact_obstruction.py` for the bounded, exact seven-event classification and sharp bounds. Both use standard-library integers, fractions and permutations; no packages, downloads, or repository writes.

Resource counts for seven-event class search: 26 supported six labeled posets; 629 candidate labeled seven-posets; 27 all-deletion-supported seven-posets; four unlabeled classes. No unrestricted seven-poset census is claimed.

## Open boundary

No infinite order-invariant precursor dynamics is obtained from this six-terminal fit. The necessary next step is a mechanism whose full prefix distributions are defined coherently at *all* `N`, with moment conditions and physically meaningful four-dimensional causal-interval scaling not chosen by terminal fitting. Lean kernel formalization NOT_RUN. Mac repo HEAD/status NOT_INSPECTED. No remote changes, commits, or merges.