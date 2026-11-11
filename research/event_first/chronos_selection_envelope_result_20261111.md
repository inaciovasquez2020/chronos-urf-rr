# Four-dimensional causal-prefix selection envelope (2026-11-11)

Repository target: `inaciovasquez2020/chronos-urf-rr`, isolated branch `research/event-first-audit-staging-20261111`.

**STATUS:** finite-poset and binomial-Chernoff theorems PROVED by direct arguments; bounded exhaustive `N<=5` check COMPUTATION_PASS; Lean NOT_RUN; Minkowski sampling limit OPEN.

## Model

Let `D=J+(p) ∩ J-(q)` be a 4D Minkowski Alexandrov interval with normalized volume measure. Draw `N` independent uniform events and order them by spacetime causality. Choose **any**, possibly randomized, natural linear extension. Let `I_n` be its first `n` elements. For `z∈D`, set `s(z)=Vol(J+(p) ∩ J-(z))/Vol(D) = (tau(p,z)/tau(p,q))^4`.

## Theorem A — pointwise selection envelope

Under the Palm conditioning that a designated sprinkled event is at `z`, its inclusion probability in the first `n` births obeys

`q_{N,n}(z) <= sum_{j=0}^{n-1} binom(N-1,j) s(z)^j(1-s(z))^(N-1-j)`.

**Proof:** An event appearing in an `n`-element down-set has at most `n-1` predecessors in the full poset. The `N-1` other independently sprinkled events each fall in its causal past with probability `s(z)`. The predecessor count is `Binomial(N-1,s(z))`. Uniform extension weighting is not needed for this necessary-condition bound.

This is an upper envelope, not a selection-weight formula.

## Theorem B — growing sublinear prefix boundary layer

For `N >= n >= 1`, define

`delta = 8(n+ln N)/(N-1)`.

Whenever `delta < 1`, simultaneously for **all** natural linear extensions,

`Pr[there exists z in an n-prefix with s(z)>delta] <= N exp[-49/16 (n+ln N)] = N^(-33/16) exp(-49 n/16)`.

**Proof:** Conditional predecessor count at `z` with `s(z)>=delta` stochastically dominates `Binomial(N-1,delta)` of mean `mu=8(n+ln N)`. An `n`-prefix can only contain events with at most `n-1 <= mu/8` predecessors. Binomial Chernoff lower tail gives

`Pr[X <= mu/8] <= exp[-(1-1/8)^2 mu/2] = exp[-49/16 (n+ln N)]`.

Apply the union bound to the `N` sampled events. The bound is uniform over all possible choices of a natural labeling, even adversarial ones, because it constrains the entire pool of eligible events.

If `n=n(N)=o(N)`, then `delta->0` and the displayed probability tends to zero. Therefore

`max_{z in I_n} tau(p,z)/tau(p,q) <= delta^(1/4) = o(1)`

with probability tending to one. **This is a boundary-layer localization theorem, not a null-geodesic dynamics law.**

## Theorem C — quantitative shell volume and expected population

The exact normalized 4D volume fraction of points with `s(z)<=delta` is

`F(delta)=6 sqrt(delta)-3 delta+3 delta ln(delta)-2 delta^(3/2)` for `0<delta<1`.

Hence `0 <= F(delta) <= 6 sqrt(delta)`, and the number `K_N(delta)` of sprinkled events in this shell is `Binomial(N,F(delta))`, so

`E[K_N(delta)]/N = F(delta) <= 6 sqrt(delta) = O(sqrt((n+ln N)/N))`.

For `n=o(N)`, the candidate shell is a vanishing fraction of the complete sprinkling, yet contains every permissible first-`n` prefix with probability tending to one. This is not a lower bound on candidate count and does not identify the random-extension selection law.

## Audited computation

`python3 research/event_first/chronos_selection_envelope_20261111.py`

Run with standard-library Python; verified in isolated tool container on 2026-11-11:

- `FINITE_POSET_TESTS := 5404` (every forward-edge closure through five vertices; n=1..N).
- `EXACT_PREFIX_ANCESTOR_EXCLUSION := PASS`.
- Representative analytical finite-N certificates `(N,n,delta,failure_bound,expected_shell_fraction)`:
  - `(1000,2,0.0713334,1.42052e-9,0.785351)`
  - `(10000,10,0.0153698,2.81664e-22,0.501407)`
  - `(100000,100,0.00892112,4.83966e-144,0.411956)`.
- `N=1000000,n=1000` bound underflowed to 0 in ordinary floating-point arithmetic. **This is numerical underflow, not a mathematical zero probability.** The exponent formula supplies the actual positive upper bound.
- No timeout was counted as PASS. No Mac or Lean build performed.

## Exact remaining OPEN boundary

The selection envelope excludes deep-interior events, but does **not** bound the ratios of linear-extension counts selecting different shallow-past events. To establish Minkowski sampling, control the annealed causal-profile bias

`lim_{n->infty} limsup_{N->infty} || E[F_{N,n,k}] - Q_k^(4) ||`.

The new boundary theorem alone neither proves nor refutes this limit. In particular it cannot be promoted as an intrinsic emergence of geometry or a gravitational field equation.

**Novelty:** not established against the entire literature; the theorems are elementary applications of predecessor counts and a standard Chernoff inequality.