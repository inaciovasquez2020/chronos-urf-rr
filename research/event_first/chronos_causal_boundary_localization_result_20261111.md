# Causal-boundary localization and shallow-past counts in 4D Minkowski diamonds

Date: 2026-11-11. Research status: analytical finite-N theorems PROVED (paper proof), independent numeric checks PASS; Lean NOT_RUN; Minkowski prefix limit OPEN. No intrinsic event dynamics or gravity is derived.

## Model and volume fraction

Let D=I(p,q) be a 4D Minkowski Alexandrov interval. Condition on N independent uniform spacetime events. The causal order is the induced timelike order. Let I_n be the first n events in *any* natural linear extension, n fixed as N increases.

For z in D, let S(z)=Vol(I(p,z))/Vol(D)=[tau(p,z)/tau(p,q)]^4. Conditional on z, the number D_N(z) of other sprinkled events preceding z is Binomial(N-1,S(z)).

## Theorem 1: uniform fixed-prefix localization (no random-extension hypothesis)

For every fixed n >= 1 and c > 1, delta_N=c log(N)/N, for all sufficiently large N,

  Pr(max_{z in I_n} S(z) > delta_N)
    <= N Sum_{j=0}^{n-1} binom(N-1,j) delta_N^j (1-delta_N)^(N-1-j)
     = O_n(N^(1-c) (log N)^(n-1)) -> 0.

Proof: every member of an n-prefix has <= n-1 predecessors in the complete poset. At a location with S >= delta_N, the lower binomial tail is bounded by the tail at delta_N. Apply the union bound over N iid points; use binomial lower-tail estimates. The probability bound holds for *every* possible natural labeling chosen from that sprinkled poset, even if selected adversarially.

Geometric interpretation: S(z)->0 in probability for all fixed early births. This describes approach to the *past null-cone boundary*, not necessarily the past endpoint (the "Big Bang"). It does not prove an antichain profile limit.

## Theorem 2: exact four-dimensional causal-past volume-fraction distribution

Normalize endpoints to p=(0,0), q=(1,0). In radial null coordinates u=t+r, w=t-r, the diamond is 0<=w<=u<=1. The normalized spacetime-volume density is 12(u-w)^2 du dw. Proper interval volume fraction is S=(u w)^2.

For 0<s<1, integration over uw <= sqrt(s) gives

  Pr(S<=s) = 6 sqrt(s) - 3s + 3s log(s) - 2 s^(3/2)

and its density is

  f_S(s) = 3 / sqrt(s) + 3 log(s) - 3 sqrt(s).

In particular, Pr(S<=s) ~ 6 sqrt(s) as s->0. This formula was checked against independent volume-uniform point sampling (160,000 draws, fixed seed); sampling is validation, not proof.

## Theorem 3: exact expected shallow-past population and square-root asymptotics

Let H_{N,n} be the number of the N sprinkled points with fewer than n predecessors in the full induced order. For fixed n, all n-prefix events lie in H_{N,n}.

Exact expectation, 1<=n<=N:

  E[H_{N,n}] =
  3 N Sum_{j=0}^{n-1} binom(N-1,j) *
      B(j+1/2, N-j) * (N-j)/(N+1/2)
   + 3 Sum_{j=0}^{n-1}(H_j - H_N),

where B is Euler's beta function and H_j=Sum_{i=1}^j 1/i, H_0=0.

Proof: integrate Pr(Bin(N-1,S)=j) against the exact density. The density terms integrate to beta functions and the log term to beta derivatives; after using
  binom(N-1,j) B(j+1,N-j)=1/N,
the logarithmic contribution becomes H_j-H_N.

For fixed n, gamma ratios and H_N=log N+EulerGamma+o(1) yield

  E[H_{N,n}] =
      3 sqrt(N) * Sum_{j=0}^{n-1} Gamma(j+1/2)/j!
      - 3 n log N + O_n(1).

In particular the expected number of minimal events is asymptotic to 3 sqrt(pi N), and the expected number with <=1 predecessor is asymptotic to (9/2) sqrt(pi N). These are eligible candidates, not uniform selection probabilities.

## Theorem 4: pair profile from one-point marginal rank inclusion

For arbitrary finite P and a uniformly random linear extension, define q_n(y)=Pr(y belongs to first n births | P). Then

  E[comparable-pair count in I_n | P]
      = Sum_{y in P} |Past_P(y)| q_n(y).

Therefore

  E[p_n | P]
    = [Sum_y |Past(y)| q_n(y)] / binom(n,2).

The formula is valid for every finite poset, because if y belongs to an ideal, all its ancestors belong. Moreover q_n(y)=0 for |Past(y)|>=n. The 4D expectation of p_n can thus be evaluated using the geometry *and the linear-extension-weighted inclusion probabilities*, but the latter have no proved asymptotic control.

## Reproducibility

Analytical equations proved by direct integration/combinatorics. Standalone Python scripts in this research branch:
- chronos_ancestor_marginal_audit_20261111.py (4,306 exact small-poset tests)
- chronos_shallow_past_asymptotics_20261111.py (CDF and beta/harmonic checks)
- chronos_past_volume_boundary_bound_20261111.py (finite-N union-bound evaluation).

The container-based checks used Python's standard library. No Mac checkout/build or Lean kernel check was run.

## OPEN boundary

A fixed n-prefix is selected from a shallow-past population whose expected size is Θ(sqrt N). The size and geometry of this pool do NOT determine the relative uniform-linear-extension weights. An asymptotic estimate for q_n(y) or the weighted expected newborn-ancestor fraction is still required to decide whether the iterated uniform-prefix sampling law tends to the Minkowski target.

Do not interpret boundary localization as spacetime emergence, physical proper-time dynamics, or gravity.

Background reference: Surya, The causal set approach to quantum gravity, Living Reviews in Relativity (2019), DOI 10.1007/s41114-019-0023-1 (Myrheim-Meyer ordering fraction).
