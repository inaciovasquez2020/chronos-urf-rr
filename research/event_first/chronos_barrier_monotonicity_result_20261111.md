# Successor barrier monotonicity and stronger first-birth bound

Date: 2026-11-11. Status: PROVED (paper proof); COMPUTATION_PASS (exact finite certificate); Lean NOT_RUN; independent review OPEN; Minkowski asymptotic OPEN.

## Setup

Let P be a finite poset of N points, x a minimal point, U={y:x<y} nonempty, u=|U|, A=P\({x}∪U), a=|A|. Define

r_x = min_{y∈Min(U)} |Past_P(y)∩A|.

On Q=P\{x}, choose a uniformly random linear extension and let B_x be the position of the first element of U.

Fix separately any linear extension alpha of A and beta of U. Permissible interleavings are characterized by a nondecreasing barrier c=(c_1,...,c_u), where at least c_i elements of alpha must precede beta_i. In particular c_1>=r_x.

## Theorem 1: barrier coordinatewise monotonicity

For two nondecreasing feasible barriers c<=d coordinatewise, the first-U rank under uniform valid c-interleavings is stochastically <= the first-U rank under uniform valid d-interleavings.

Proof: Encode interleavings as distributive-lattice paths ordered by moving A symbols earlier. Validity under c is a down-set and a sublattice. Validity under d is a down-set of the c-valid lattice. The event {B>j} is another down-set. Uniform measure on a finite distributive lattice is positively associated by FKG. Therefore conditioning the c-valid measure on d-validity cannot reduce Pr(B>j). This proves dominance simultaneously for all j.

## Theorem 2: explicit full-tail comparison

The first-U rank B_x stochastically dominates B_r=r_x+B_free, where B_free is the first-U position in a uniform shuffle of a-r_x A symbols and u U symbols.

Precisely, for every integer j=0,...,N-1,

Pr(B_x>j) >= L(j) = {
  1,                                            if j<=r_x;
  binom(a-r_x,j-r_x)/binom(a-r_x+u,j-r_x), if r_x<j<=a;
  0,                                            if j>a
}.

The convention is binom(top,bottom)=0 if bottom>top. This follows from Theorem 1 for each fixed alpha,beta, since the constant barrier (r_x,...,r_x) is coordinatewise below the actual barrier. Averaging the resulting inequalities over all (alpha,beta), **with their correct extension-count weights**, preserves the comparison.

## Corollary: improved correlation penalty and first-birth weight

Since E[B_free]=(N-r_x)/(u+1),

 Delta_x := E[B_x]-N/(u+1) >= r_x*u/(u+1),

 Pr(x is first | P) = 1/E[B_x] <= (u+1)/(N+r_x*u).

The previous bound sum_{j=1}^{r_x} (1 - binom(a,j)/binom(N-1,j)) is no stronger than this new bound, because Theorem 2 also controls the tail at j>r_x.

## Reproducible checks (local computational environment, Python stdlib)

- Compared 36,088 coordinatewise-ordered pairs of nondecreasing integer barriers for all 1<=a,u<=5, with exact rational survival distributions.
- Exhaustive forward-edge configurations, transitive closure, 2<=N<=6: 60,129 eligible minimal-event cases with u>0, including exact mean and **full-tail** bounds.
- Strict slack between exact Delta_x and new lower bound occurred in 33,642 such cases.
- Original independent tests re-run from local files: 2,121 barrier-vs-brute cases; 100/80/50 finite 4D sprinkled-poset fixtures at N=8/12/16, with no resource guard failures.

The independently rerun 4D diagnostic (same fixed seed, conditioned on u>0) was:

| N | Independent posets | Minimal x with u>0 | Mean exact Delta | Old lower bound | New lower bound |
|---|---:|---:|---:|---:|---:|
| 8 | 100 | 179 | 1.08810 | 0.31179 | 0.55214 |
| 12 | 80 | 249 | 2.16625 | 0.38569 | 0.88300 |
| 16 | 50 | 209 | 3.08369 | 0.53444 | 1.11448 |

**Warning:** These means exclude minimal x with u=0 (whose Delta is exactly zero); they cannot be compared directly to the earlier all-minimal candidate averages. Neither the samples nor the lower-bound improvement establishes asymptotic convergence.

Executable exact certificate created during this investigation: `chronos_barrier_monotonicity_audit_20261111.py` (SHA256 `8d3f4f0adb1f525513b56e3261ea6574c0647b01ee266d59e2ef515353bf015a`), provided as a conversation artifact; upload-back to this branch may be separate.

## Research boundary

Determine how the **full random barrier** (including extension-count weighting over internal orders) scales for geometrically conditioned minimal x in a 4D Minkowski-diamond sprinkling. The scalar r_x detects only part of the penalty and does not yield a uniform-in-N upper bound on Delta_x, hence it does not establish the first-birth selection density, the iterated Minkowski uniform-subset limit, intrinsic spacetime emergence, or gravitational dynamics.

Background: FKG positive association on finite distributive lattices (Fortuin-Kasteleyn-Ginibre, 1971); Graham-Yao-Yao and Shepp order comparisons; De Loof-De Meyer-De Baets (2006) ideal-lattice linear extension framework. Novelty beyond established methods NOT_ESTABLISHED.
