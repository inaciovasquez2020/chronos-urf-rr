# Chronos causal-growth: sharp 5→6 covariance obstruction

**Status:** PROVED conditional on the specified five-event terminal distribution and discrete general covariance; exhaustive exact rational computation `COMPUTATION_PASS`; Lean `NOT_RUN`; no repository mutation.

**Reference:** `inaciovasquez2020/chronos-urf-rr`, PR #1347, checkpoint `abef2b3e61dcb24a3ebb65ad0df7a76f63d4869f` (remote checkpoint, not a checked local HEAD).

## Assumptions

Five-event **unlabeled terminal class masses**: antichain 11/70; one 2-chain plus 3 isolated 5/7; one 3-chain plus 2 isolated 1/35; two disjoint 2-chains plus 1 isolated 1/10. Within every class each naturally labeled order has equal probability. Let `mu_6` be any probability distribution on 6-event naturally labeled partial orders satisfying (a) exact first-five-label prefix equal to `mu_5`, and (b) discrete general covariance: equal probability for naturally labeled realizations of each unlabeled terminal order. No Bell-causality assumption is used.

## Result

Exactly 132 of all 4824 naturally labeled 6-event posets, in 9 unlabeled isomorphism classes, have **all** five-event maximal-deletion ideals inside the support of `mu_5`. All other classes have zero `mu_6` mass by discrete general covariance and five-prefix support. Write `v_j` for the probability vector on the four five-event classes obtained by uniformly choosing a natural labeling in six-class j; write `s_j` for the corresponding 6-event pair, triple-chain, induced 2+2 densities. Every feasible six-event law is a convex combination of the nine six-classes with `sum_j w_j v_j=q`, `w_j>=0`.

Exact rational vertex enumeration and dual certificates establish the **sharp marginal ranges**

```
53/350 <= E[P2(6)]  <= 2/5
 2/175 <= E[P3(6)]  <= 9/175
 1/150 <= E[P22(6)] <= 1/50
```

The minima and maxima need not be simultaneously attainable. The extrema given in the script include nonnegative exact rational class weights that realize every bound.

Hence it is **impossible** to retain the exact four-dimensional diamond reference pair and three-chain probabilities `1/10` and `1/350` at size six while keeping the *specified* five-event terminal law and discrete general covariance. Already the lower bounds exceed the respective targets: `53/350 > 1/10`, `2/175 > 1/350`.

This is not an impossibility result for arbitrary intrinsic growth dynamics or four-dimensional manifoldlikeness; the original five-event law was a fitted artificial terminal distribution, not the complete 5-point Minkowski random-poset distribution.

## Dual proof certificates

Order the five classes as: antichain (A), single 2-chain (E), single 3-chain (C), two disjoint 2-chains (D). For every one of the nine admissible 6-classes, the rational class fractions satisfy

```
s_pair >= (-3/5)*v_A + (2/5)*v_E + 0*v_C + (-2/5)*v_D
s_three >= (-1/10)*v_A + (1/20)*v_E + (1/20)*v_C + (-1/10)*v_D.
```

These are verified over the complete nine-class enumeration in `chronos_six_event_exact_bounds.py`. Multiplying by arbitrary nonnegative six-class weights, summing, and inserting the five-class masses gives lower bounds `53/350` and `2/175`. Exact feasible primal witnesses prove both are sharp.

## Independent observations

One alternative non-cone extension is obtained by assigning probability `1/70` to the six-antichain, reducing the six-event cone over the five-antichain from `11/70` to `10/70`, and leaving the other cone distributions unchanged. This preserves the five-event marginal and general covariance, demonstrating nonuniqueness of the six-event extension (but not four-dimensional emergence).

The first-five-event prefix law is a chronology-weighted *stem distribution*. It must not be identified with uniformly sampled five-event induced suborders from the four-dimensional diamond. That mismatch is precisely why simultaneous fixed-N target frequencies can be inconsistent.

## Verification and reproduction

Run the standalone standard-library script `chronos_six_event_exact_bounds.py` using Python 3. It enumerates natural-labeled posets via downsets, canonicalizes under all relabelings (<=720 permutations), enumerates exact feasible vertices of the nine-class linear program, proves sharp bounds with rational primal witnesses and dual certificates, and prints `RESULT := COMPUTATION_PASS_EXACT`. No Git or Mac build required, no downloads or writes other than Python's optional bytecode cache if imported elsewhere. Environment-independent exact integer and Fraction arithmetic. This script was run in the analysis container; Mac verification and Lean kernel verification are NOT_RUN.

**NEXT:** Determine whether the five-event terminal law should instead be derived from intrinsic geometry as a full distribution rather than tuned to just three moments. Formalize the finite dual bounds in Lean after Mac source/toolchain and working-tree audit. Overall spacetime emergence remains OPEN.