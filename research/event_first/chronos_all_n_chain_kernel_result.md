# All-N intrinsic disjoint-chain kernel: exact audit

**Status:** PROVED analytical statements conditional on the stated model; independent finite rational audit `chronos_all_n_chain_kernel_audit.py` PASS for n <= 7, theta = 1, 3/2, 9. Lean NOT_RUN. No repository mutation.

## Definition
For a finite causal order C which is the disjoint union of chains of cardinalities s_1,...,s_r, n=sum_i s_i, and fixed theta>0, a new maximal event has precursor empty with probability theta/(theta+n) or precursor the entire i-th chain with probability s_i/(theta+n). All other precursors have probability 0. The empty-state transition is 1.

## All-n identities
1. Normalization: (theta + sum_i s_i)/(theta+n)=1.
2. Local covariance squares: whenever newly added events x,y are incomparable, positive products contain the same factors theta, s_i, s_j in either order, over denominators (theta+n)(theta+n+1); all prohibited nonmaximal-component attachments have zero on both routes.
3. Each complete natural-labeling history of a disjoint union of chains of lengths s_i has probability
   theta^r prod_i (s_i-1)! / prod_{j=0}^{n-1}(theta+j),
   hence is independent of the natural labeling. This is *discrete general covariance*, not full exchangeability of birth labels.
4. Restriction to the first n births is the n-step law by construction; Kolmogorov extension gives an infinite law on naturally labeled orders. This is prefix projectivity, not uniform deletion projectivity of oriented birth labels.
5. For a uniformly selected subset of vertices, the pair and triple chain frequencies have expectations independent of the sample size:
   P2 = 1/(theta+1); P3 = 2/((theta+1)(theta+2)); P22 = 3 theta / ((theta+1)(theta+2)(theta+3)).
   The last probability is the induced two-plus-two probability for a four-element subset; choose two blocks of size two, one per chain, with no cross-comparabilities.
6. The inclusive fork probability equals P3, and the strict fork probability equals zero; the support consists only of chain unions, so there is no branching.

## Target rejection
P2=1/10 forces theta=9, hence P3=1/55 rather than 1/350; P22=9/440 > 0. Positive 2+2 alone does not imply dimensional agreement.

## Entire exchangeable disjoint-chain-mixture class: no-go
Let an infinitely exchangeable random partition have Kingman paintbox block frequencies (s_i), potentially with dust of total mass 1-sum_i s_i. Given the frequencies, probabilities that independent sampled vertices lie in the same nontrivial block are q2=sum_i s_i^2 and q3=sum_i s_i^3. By Cauchy-Schwarz,
(q2)^2 <= (sum_i s_i^3)(sum_i s_i) <= q3.
Averaging and Jensen imply P3=E[q3] >= E[q2^2] >= (E[q2])^2=P2^2.
Thus P2=1/10 forces P3 >= 1/100 > 1/350. This rules out *all infinitely exchangeable partition-into-chains processes*, including mixing theta and Pitman-Yor variants. It does NOT rule out branching, inter-chain comparabilities, nonexchangeable partition laws, or other covariance-preserving causal growth dynamics.

## Audit
Exact enumeration of each labeled chain-assignment state (Bell numbers 1,2,5,15,52,203,877 for n=1,...,7) at theta=1,3/2,9; exact rational normalization and pair/triple/2+2 moments all PASS. No external packages, no cloning or downloading. A failed preliminary script with typo and a wrong state-count assertion was corrected; only the final executed script constitutes a PASS.

## Repo / status
Target: inaciovasquez2020/chronos-urf-rr, preserved prior SHA abef2b3e61dcb24a3ebb65ad0df7a76f63d4869f; remote lean-toolchain at that SHA leanprover/lean4:v4.29.0. Mac HEAD, dirty state, Lean compilation and axiom audit NOT_RUN. No GitHub writes.

## Open obligation
An all-N intrinsic **branching** growth mechanism with positive induced 2+2 density, exact P2=1/10 and P3=1/350, and an independently justified dimensional/manifoldlikeness limit. Establish the finite covariance squares before treating it as discrete generally covariant; check the full distribution rather than fitting moments.