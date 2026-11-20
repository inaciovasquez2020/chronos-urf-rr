# Chronos — first-choice successor-size sandwich (2026-11-15)

## Scope and statuses

**PROVED (finite-poset inequality).** For a finite poset P with N elements, a minimal element x, and d=|{y:x<y}|, the probability q_x that x appears first in a uniformly random linear extension satisfies

    1/(N-d) <= q_x <= (d+1)/N.

Both endpoints are attained for each N >= 2 and 0 <= d <= N-1. This proof does not establish Minkowski first-choice delocalization or an infinite-growth limit.

## Proof of lower bound

Let A be the N-1-d events incomparable with x and F the d strict successors. The induced poset P\{x} has no relation F < A. For any uniform extension L of P\{x}, let U be the 1-based rank of the first F event (or N if F is empty). There are exactly U insertion slots for x, so q_x=1/E[U]. Since at most |A| events precede the earliest F, U <= |A|+1=N-d. Thus q_x>=1/(N-d).

## Proof of upper bound

Fix arbitrary internal linear extensions alpha of A and beta of F. In a uniformly random extension of P\{x} conditional on these two orders, the F positions S=(k_1<...<k_d) form a uniformly chosen increasing d-tuple from [N-1], *conditioned on admissibility of the cross relations A_i<F_j*. Each such relation imposes k_j >= i+j. Therefore the admissible tuples form an increasing subset D of the distributive lattice of increasing d-tuples ordered coordinatewise.

The uniform measure on this finite distributive lattice satisfies the FKG lattice condition (all weights = 1, so mu(s meet t)mu(s join t)=mu(s)mu(t)); k_1 and the indicator of D are both increasing. Hence E[k_1 | D]>=E[k_1]. The unrestricted minimum position of d uniformly placed distinct slots among N-1 has expectation N/(d+1). Consequently E[U | alpha,beta]>=N/(d+1), and averaging over the actual conditional distribution of internal orders preserves that inequality. So q_x=1/E[U]<=(d+1)/N. For d=0, the probability is exactly 1/N.

Note: the FKG step can also be proved via the monotone lattice-path coupling of admissible shuffles. No Minkowski geometry is needed.

## Endpoint sharpness constructions

Let a=N-d-1. For the upper bound, take a chain of length d+1 beginning at x, disjoint from an a-element chain. Every interleaving is allowed; the probability the first position is occupied by x is (d+1)/N.

For the lower bound, make x incomparable with a chain A of length a, require every A element and x to precede a chain F of length d (if d=0, the model is an antichain x + A). Before F can start, x and all A must appear. There are a+1 insertion positions for x into A and exactly one begins with x; q_x=1/(a+1)=1/(N-d).

Thus d alone cannot determine q_x; the cross-order constraints between A and F matter.

## Computational receipt

`chronos_first_choice_successor_sandwich_20261115.py` was executed with Python 3 standard library. It exhaustively enumerated 1, 3, 19, 219, and 4231 labeled posets for N=1,...,5 and verified 8817 minimal-vertex instances. Both inequalities held, including 3473 equality instances of each. It separately verified 435 rational shuffle-count identities for the disjoint-chain equality family. A first run failed only a hard-coded expected case count (8816 vs actual 8817), because the N=1 case was included; the counter was corrected and rerun PASS. Neither failure nor correction affects the theorem's statement.

## Bounded Minkowski exact linear-extension experiment

Fixed-seed iid uniform 4D diamond sprinklings, subset-DP exact counts (the probabilities for each sampled poset are exact integer ratios, reported averages decimal):

N | samples | mean max_x q_x | median max_x q_x | mean # minimal elements | mean reachable DP states
8 | 100 | 0.2987783 | 0.25 | 6.06 | 150
12 | 100 | 0.2429993 | 0.2010101 | 8.57 | 1517
16 | 100 | 0.2494834 | 0.2090015 | 10.38 | 12697
20 | 40 | 0.2644233 | 0.2256322 | 11.7 | 101632

These sample sizes are too small to establish an asymptotic trend or a confidence interval for a limit. Experimental seeds: 10000*N through 10000*N+samples-1. Independent script `/tmp/chronos_firstchoice_test.py` in the ephemeral working container, not part of the downloadable certificate; no Git changes.

## Open

1. Asymptotic distribution of E[U_x] / q_x for minima in the tip and null-boundary layers of 4D Minkowski sprinklings.
2. Q_N=max_x q_x, fixed-prefix limiting law, and iterated double limit.
3. Exact p_(4,2) from the incomparable-pair overlap second moment.
4. Lean formalization/axiom audit: NOT_RUN.
5. GitHub promotion: NOT_PERFORMED.
