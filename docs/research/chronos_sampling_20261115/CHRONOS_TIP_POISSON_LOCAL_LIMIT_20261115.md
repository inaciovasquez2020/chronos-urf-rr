# Chronos: exact bottom-tip Poisson local limit (2026-11-15)

## RESULT — PROVED, with exact-arithmetic checks

For N iid uniform events in the fixed unit-height four-dimensional Minkowski diamond
D={(t,x):0<=t<=1, |x|<=min(t,1-t)}, fix T>0 and N>=16T^4 (so that T N^(-1/4)<=1/2). Let D_{N,T} be the points with t<=T N^(-1/4) and rescale (t,x) -> N^(1/4)(t,x). The resulting random finite configuration in C_T={(tau,u):0<=tau<=T, |u|<=tau} is a binomial point process: its number of points K_N has law Bin(N,8T^4/N), and, conditional on K_N=k, its k positions are iid uniform on C_T under four-volume. Causal comparability is exactly preserved by rescaling.

Let Pi_T be a Poisson point process in C_T with constant four-volume intensity 24/pi. Its total mass is lambda_T=8T^4. Conditional on the total count, its points have the identical iid distribution to the rescaled binomial sample. Consequently the TOTAL VARIATION DISTANCE of the full rescaled marked causal configurations, including their partial-order structure, is no more than 2 lambda_T^2/N = 128 T^8/N (by the standard elementary binomial-to-Poisson coupling inequality). This gives the explicit O(1/N) fixed-window local limit, without linear-extension assumptions.

### Minimal events

Every predecessor of a point in the tip window also lies in the same window. Thus the events minimal in the induced tip poset are *exactly* the globally minimal points that lie in the tip window. Let M_N(T) count them. By distributional convergence, M_N(T) converges in total variation to M_T, the minimal-point count in Pi_T. Also, using conditional binomial predecessor counts and dominated convergence,

E M_N(T) -> E M_T = 96 int_{0}^{T} int_{0}^{tau} u^2 exp[-(tau^2-u^2)^2] du d tau.

Writing I_k(T) = 96 T^(4k+4)/(4k+4) sum_{j=0}^{2k} (-1)^j binom(2k,j)/(2j+3), we obtain the entire absolutely convergent series

E M_T = sum_{k>=0} (-1)^k I_k(T)/k!.

For T=1/2, lambda_T=1/2 and exact rational integration gives I_0=1/2, I_1=1/280, I_2=1/13860. Summing k=0,...,15 gives E M_T=0.49646430257308455... with certified absolute remainder bounded by I_16/16! < 10^-30. This is not the mean of K_N; it counts only causal-set minima.

Because K_N is tight and M_N(T)<=K_N, the number of global minima within each fixed rescaled tip window is O_p(1). The full number of global minima is of order sqrt(N), by the separately established predecessor-count concentration. Thus a uniformly chosen globally minimal event almost surely does *not* lie within any fixed rescaled tip window. **This last statement does NOT extend automatically to the first event of a uniformly sampled linear extension**, because extension weights may favor tip minima arbitrarily strongly.

### Infinite-growth boundary

This identifies a genuine *Poisson tip subproblem*: analyze the probability weight that a uniform linear extension of the entire N-event poset assigns to the O_p(1) global minima in a fixed tip window, and then control the complement consisting of nearly-null, extensive-radius minima. No bound on that weight, Q_N, or on the double limit is proved here.

### Verification

The accompanying pure-standard-library certificate `chronos_tip_poisson_local_limit_20261115.py` verifies the exact integral moments, alternating-series error, and illustrative finite-N binomial-vs-Poisson inequalities. This is a rigorous mathematical derivation with computational checks, not a Lean kernel verification.

- TIP_POISSON_LOCAL_LIMIT: PROVED.
- TIP_MINIMAL_EXPECTATION_SERIES: PROVED.
- EXACT_ARITHMETIC_TESTS: COMPUTATION_PASS.
- MINKOWSKI_FIRST_CHOICE_WEIGHTS: OPEN.
- EXACT FOUR-EVENT p_(4,2): OPEN.
- DOUBLE LIMIT: OPEN.
- LEAN: NOT_RUN.
- GIT CHANGES: NOT_PERFORMED.
