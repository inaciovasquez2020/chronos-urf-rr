# Chronos–URF–RR: descendant marks of shallow-past candidates

Date: 2026-11-11. Scope: four-dimensional volume-uniform Minkowski sprinklings. Status: exact conditional law PROVED; expected-intensity asymptotic PROVED; finite rational certificate COMPUTATION_PASS; finite Monte Carlo diagnostic PASS; linear-extension selected-birth law OPEN; Lean NOT_RUN; novelty NOT_ESTABLISHED.

## Finite-N exact law

For a distinguished event Z=z in the Alexandrov diamond D=I(p,q), set S(z)=Vol(I(p,z))/Vol(D), F(z)=Vol(I(z,q))/Vol(D), D_N(z)=number of other points causally preceding z, and V_N(z)=number of other points causally succeeding z. All N points are iid uniform in four-volume. Causal past and future are disjoint cells with respective probabilities S and F; the incomparable region has probability 1-S-F.

For N>=1, 0<=j<=N-1 and S(z)<1:

V_N | {Z=z, D_N=j} ~ Bin(N-1-j, F(z)/(1-S(z))).

The j predecessors, N-1-j remaining outside-past points, and their conditional induced orders follow the corresponding iid conditional-volume laws. This is the elementary exact multinomial conditioning identity and involves no random linear extension.

## Theorem: joint normalized expected-intensity limit

For any fixed j>=0, let C_{N,j} be the random counting measure of events with exactly j predecessors. Consider its expected measure with marks (u(z), V_N(z)/N), normalized by E[#C_{N,j}], where u=t+r is the outgoing radial null coordinate in a normalized unit diamond. By the previously derived intensity limit,

u -> U ~ Beta(2,1),  w=t-r -> 0, and NS -> Gamma(j+1/2,1) independent of U.

Given position and j predecessors, V_N/N concentrates around [(N-1-j)/N] F/(1-S), since its conditional variance is at most 1/(4N). Along w->0, F=[(1-u)(1-w)]² -> (1-U)². Hence, under the normalized EXPECTED counting measure,

(u, V_N/N) => (U, (1-U)²).

This is not a concentration theorem for one realized random candidate pool and is not the distribution of a linear-extension-selected event.

## Exact limiting distribution and moments

For Q=(1-U)², U density 2u on [0,1]:

Pr(Q<=q)=2 sqrt(q)-q, 0<=q<=1;
Pr(Q>=theta)=(1-sqrt(theta))², 0<=theta<=1;
E[Q^k]=1/[(k+1)(2k+1)] for integer k>=0.

In particular E[Q]=1/6, E[Q²]=1/15, and Pr(Q>=1/4)=1/4.

The expected candidate count satisfies

E[#C_{N,j}] ~ 3 Gamma(j+1/2)/j! sqrt(N).

Therefore, for each fixed theta in (0,1),

E[# {z: D_N(z)=j, V_N(z)>=theta*N}]
 ~ 3 Gamma(j+1/2)/j! (1-sqrt(theta))² sqrt(N),

where an integer threshold can be implemented with ceil(theta*N). Similarly, the expected number of directed causal relations from exactly-j-predecessor candidates to their future successors is asymptotic to

(1/2) Gamma(j+1/2)/j! N^(3/2).

Proof: bounded continuous mapping and conditional binomial variance control; boundary theta has zero limiting atom. Bounded marks also give moment convergence. The asymptotic pertains to expected counts, not concentration.

## Reproducible validation

- `chronos_shallow_future_exact_audit_20261111.py`: 2,800 exact Fraction comparisons of multinomial and conditional binomial probabilities for N=3,...,10, past/future rational fractions, all possible feasible counts, PASS; exact moment algebra k=1,...,7 PASS.
- `chronos_shallow_future_marked_20261111.py`: three independent fixed-seed, 450,000-sample importance-weighted expected-intensity checks with no explicit large causal-set construction:
  * N=1000,j=0: expected candidate count 145.22935, mean V/N 0.121732, mean (V/N)² 0.035208, P(future fraction proxy>=1/4) 0.171482.
  * N=10000,j=0: count 509.52405, mean 0.145358, second moment 0.049492, high-future proxy 0.219658.
  * N=10000,j=1: count 239.06804, mean 0.128826, second moment 0.038097, high-future proxy 0.188816.
  * The proxy uses conditional future probability F/(1-S), not binomial-realized V/N, and is **not** a first-birth probability.
  * Limiting target mean 0.166667, second moment 0.066667, upper-tail fraction at 1/4 equals 0.25. Finite-size bias is non-negligible; no extrapolated numerical PASS is claimed.

A failed preliminary numerical test compared finite N=1000 with the N=infinity mean using an inappropriately narrow tolerance. The test was corrected to check finite arithmetic and clearly report finite-size deviations. No failed check was relabeled as evidence of convergence.

## Precise boundary

Mac repository/build state NOT_INSPECTED. Lean NOT_RUN. No effect on PR #1347. The law describes SHALLOW-PAST GEOMETRIC CANDIDATES. Their weight under uniform random linear extensions depends on global extension counts, equivalently extension-weighted successor barriers, and is not fixed by this mark distribution.

NEXT: Find geometry-conditioned estimates of E[B_x] or its rank-biased law that persist under whole-poset selection weights. MINKOWSKI PREFIX SAMPLING: OPEN. EMERGENT GRAVITY: OPEN.
