# Order-type Markovization of exact Minkowski growth

Date: 2026-11-11. Status: PROVED mathematically; COMPUTATION_PASS (exact fractions and bounded experiment); Lean NOT_RUN; novelty and independent review NOT_ESTABLISHED. Background-independent emergence and gravity OPEN.

## Theorem 1: exact Minkowski marginals with an unlabeled-poset Markov state

Let `Q_n` be the unlabeled isomorphism-class law of `n` iid volume-uniform events in a four-dimensional Minkowski Alexandrov diamond. The already proved radial-Poisson growth gives a past-finite natural history `R_n` with `Law([R_n])=Q_n` for every `n`. Its geometry uses a preferred timelike frame and is not order-invariant.

For unlabeled n-element types `C` and (n+1)-element types `D`, define `J_n(C,D)=Pr([R_n]=C,[R_(n+1)]=D)`. For `Q_n(C)>0` put `K_n(C,D)=J_n(C,D)/Q_n(C)`. For zero-probability parent types, choose any stochastic row supported on possible one-maximal-element extensions. Since radial growth adds maximal events, `K_n` has support only on legal causal births. The row sums are one. Starting at one element, use `K_n` as a stage-dependent Markov transition matrix on **unlabeled poset types**. By induction its n-stage law is exactly `Q_n`.

This is an existence result, not a tractable algorithm for computing all `K_n`: its probabilities incorporate the continuum Minkowski law through `J_n`. The Markovized chain generally does NOT reproduce the entire joint history law of radial-Poisson growth; it reproduces every one-time marginal and consecutive-stage pair law. To implement a birth on a concrete representative, select an eligible precursor ideal for the chosen child type by an automorphism-invariant distribution, such as uniform over eligible ideals. This respects relabeling, but not the much stronger physical path-covariance condition.

## Theorem 2: almost sure large-prefix Minkowski sampling statistics

For every fixed k and k-element unlabeled poset type H, let `F_(n,k)(H)` be the fraction of k-subsets of the n-event Markov state inducing H. Because the one-time n-event law is `Q_n`, this has the same distribution as the order-type U-statistic of n independent points in the unit diamond, with mean `Q_k(H)`. Replacing one point changes at most `k/n` of the subsets. McDiarmid therefore gives

`Pr(|F_(n,k)(H)-Q_k(H)|>epsilon) <= 2 exp(-2 epsilon² n/k²)`.

The tail is summable. First Borel–Cantelli (no interstage independence needed) proves `F_(n,k)(H)->Q_k(H)` almost surely for every fixed pair (k,H), simultaneously for all such pairs by countability.

This verifies the **sampling-statistic** goal in an isomorphism-class Markov model, but gives no intrinsic explanation of why the model's transition constants encode Minkowski geometry.

## Theorem 3: unique two-to-three type transition matrix

The two-event state probabilities are `Q2(comparable)=1/10` and `Q2(incomparable)=9/10`. The exact three-event type probabilities are: chain `1/350`; two minima/one maximum `9/350`; one minimum/two maxima `9/350`; single edge `33/175`; antichain `53/70`.

A three-chain and a one-minimum-two-maxima poset necessarily have a **comparable** initial pair in any natural birth order. A two-minima-one-maximum poset and an antichain necessarily have an **incomparable** initial pair. The single-edge poset permits both. Thus the single-edge/comparable-prefix joint mass is forced to equal `1/10-1/350-9/350=1/14`. The single-edge/incomparable-prefix mass is `33/175-1/14=41/350`.

| Two-event state | Three-event state | Exact transition probability |
|---|---|---:|
| Comparable | Three-chain | 1/35 |
| Comparable | One minimum, two maxima | 9/35 |
| Comparable | Single edge | 5/7 |
| Incomparable | Two minima, one maximum | 1/35 |
| Incomparable | Single edge | 41/315 |
| Incomparable | Antichain | 53/63 |

This type-level matrix is uniquely determined by the Q2 and Q3 marginals and natural birth order, independent of which particular natural-growth construction realizes them. Multiplying rows by Q2 and summing recovers all five Q3 probabilities.

## Stronger physical covariance is REFUTED for exact Q_n

An order-invariant process would obey `Q2=T Q3`, where T takes the first two events of a uniformly chosen linear extension of the final three-event poset. Yet `Q2(comparable)=1/10` and `(T Q3)(comparable)=16/175`, a difference of `3/350`. Hence no order-invariant birth-label law realizes exact `Q_n` at every stage. Isomorphism invariance of `K_n` is not the Rideout–Sorkin discrete general covariance or Bell causality (Rideout and Sorkin, Physical Review D 61, 024002 (2000), DOI 10.1103/PhysRevD.61.024002).

The process is therefore **weakly intrinsic only as an unlabeled state machine**. Its transition probabilities have been obtained from a spacetime background. No physical background-independent growth axiom, CSG compliance, intrinsic Lorentz-covariant embedded birth rule, or gravitational dynamics has been derived.

## Independent validation and remaining obstruction

`chronos_markovized_order_type_growth_20261111.py`: exact rational matrix audit; permutation enumeration of natural extensions; 150,000 radial-Poisson three-event histories; seeded and bounded. All six conditional transition frequencies and five unconditional order-type frequencies passed declared tolerances; every simulated birth respected causal order. General-n numerical construction of K_n NOT_RUN. Lean NOT_RUN.

**OPEN:** Compute tractable `K_n` for general n from causal order alone without precomputed continuum integrals, and determine whether an axiomatized intrinsic growth law can retain Minkowski large-prefix sampling while satisfying a defensible covariance condition. No merge performed; PR #1347 remains untouched.