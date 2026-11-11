# Exact upper bound on first-birth selection from future-set size

2026-11-11. Mathematical theorem PROVED (proof by shuffle association). Independent finite check COMPUTATION_PASS. Lean NOT_RUN. Novelty NOT_ESTABLISHED. Minkowski uniform-tail convergence OPEN.

## Theorem

Let P be a finite poset with N elements, and let x be minimal. Write U(x)={y∈P: x<y}, s=1+|U(x)|. Under a uniformly chosen linear extension of P,

  1/(N-|U(x)|) ≤ Pr(x first) ≤ (1+|U(x)|)/N.

The lower bound comes from inserting x into linear extensions of P\{x}: if B is the position of the first successor (or N when none exists), then Pr(x first)=1/E[B] and B≤N−|U(x)|.

## Proof of upper bound

Set C={x}∪U(x), an upset of size s. Its complement D is a downset of size d=N−s. Condition on the internal linear orders σ_C and σ_D induced by a uniform linear extension of P. Each admissible interleaving of those two orders appears equally often; x is the first member of C because x precedes every other element of C.

Encode a binary interleaving by h=(h_1,...,h_s), where h_i is the number of D symbols preceding the ith C symbol. The unconstrained set of interleavings is the distributive lattice

  L={0≤h_1≤...≤h_s≤d},

ordered coordinatewise. The uniform measure on this finite distributive lattice is positively associated (FKG lattice inequality): increasing events are nonnegatively correlated.

The actual cross-order constraints all have the form D_j<C_i, because C is an upset. For the fixed internal orders, these constraints require h_i≥a_i for certain integer thresholds a_i. Thus the admissibility event E={h_i≥a_i for all i} is increasing. The event H={h_1≥1}, equivalently 'the first interleaving symbol belongs to D', is also increasing.

By positive association,

  Pr(H|E) ≥ Pr(H) = d/N.

Consequently, conditionally on σ_C and σ_D,

  Pr(first symbol C | admissible shuffle) ≤ s/N.

Average over the internal linear orders. Since the first C symbol is x, this proves Pr(x first)≤s/N. Cases s=N or d=0 are immediate. This completes the proof.

The use of FKG is standard; this is an exact finite-poset bound, not a Minkowski limit or a novelty claim.

## Exhaustive independent certificate

`chronos_minimal_future_upper_bound_20261111.py` enumerates all 32,768 forward-edge configurations on six vertices, plus all smaller configurations, closes transitively, counts extensions exactly by ideal-bitmask DP, and tests N e(P\{x}) ≤ (1+|U(x)|)e(P) for every minimal x. Total 66,633 minimal-event instances: PASS. Ran locally in isolated container, not on Mac. Resource bound: N≤6, 32,768 configurations maximum.

## Selection-bias obstruction

The two inequalities depend only on strict future size. They are generally wide. Together with the direct-sum example in `chronos_component_selection_result_20261111.md`, they establish that neither minimal-event counts nor candidate volume-fraction distributions alone identify uniform-linear-extension birth probabilities.

For a four-dimensional Minkowski sprinkled causal diamond, these bounds do not determine E[B_x] in the insertion formula or the large-prefix induced-order profile. GLOBAL MINKOWSKI SAMPLING LIMIT remains OPEN; intrinsic emergence/gravity OPEN.