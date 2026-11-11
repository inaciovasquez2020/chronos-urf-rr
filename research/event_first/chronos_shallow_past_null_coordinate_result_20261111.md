# Chronos–URF–RR: limiting null-coordinate intensity of shallow-past events

Date: 2026-11-11. Status: **PROVED analytically**, finite Monte Carlo **PASS**, **LEAN NOT_RUN**; uniform-linear-extension selection weights and Minkowski birth-prefix statistics **OPEN**. No claim of original novelty.

## Set-up

Take the four-dimensional Minkowski Alexandrov interval with normalized past and future endpoints `p=(0,0)` and `q=(1,0)`. Use null radial coordinates `u=t+r`, `w=t−r`, `0≤w≤u≤1`. The normalized spacetime-volume measure is `12(u−w)^2 du dw`. The causal-past volume fraction is `S=(uw)^2`; the causal-future volume fraction is `F=[(1−u)(1−w)]^2`.

Place `N` independent volume-uniform events. Given that a distinguished event is at `(u,w)`, its number of predecessors among the other `N−1` events is `Bin(N−1,S)`.

## Theorem: shallow-past expected intensity

Let `C_{N,j}` be the counting measure of events having exactly `j` predecessors. For each counted point record `(U,T)` where `U=u` and `T=NS`. Fix a nonnegative integer `j`. As `N→∞`, the expected counting measure, divided by `sqrt(N)`, converges weakly to the finite measure on `0<u<1`, `t>0` with density

`(6/j!) u t^(j−1/2) exp(−t) du dt`.

In particular,

`E[# C_{N,j}] ~ 3 sqrt(N) Γ(j+1/2)/j!`.

After normalization by its mass, the limiting **expected-intensity** law factors as

`U ~ Beta(2,1)` with density `2u` and `T ~ Gamma(j+1/2,1)`, independently.

For events with fewer than `n` predecessors, fixed `n`, the same limiting U-law holds. The T-law is the mixture with unnormalized density `t^(−1/2) exp(−t) Σ_{j=0}^{n−1} t^j/j!`.

**Proof outline:** In the original volume law, make the substitution `t=N(uw)^2`, or `w=sqrt(t/N)/u`. Then

`N · 12(u−w)^2 du dw = sqrt(N) [6(u−w)^2/(u sqrt(t))] du dt`.

For fixed `u>0,t>0`, `w→0`, so the normalized prefactor approaches `6u/sqrt(t)`. The exact binomial mass of predecessor count `j`,

`binom(N−1,j)(t/N)^j(1−t/N)^(N−1−j)`, tends to `t^j exp(−t)/j!`.

The geometric domain imposes `w≤u`, i.e. `t≤Nu^4`; the region `u=O(N^(-1/4))` has negligible `sqrt(N)`-normalized intensity. Standard binomial exponential tail bounds control large `t` and allow dominated convergence; integration gives the stated gamma factor. The limit is a statement about **expectations of counting measures**. It does **not** establish empirical concentration of the random measure, or the distribution of a uniformly selected event from each realized candidate pool.

## Consequence: future-volume fraction of shallow-past candidates

For each candidate in the limit, `w→0`. Therefore the future-volume fraction satisfies `F→(1−U)^2`. Its limiting expected-intensity CDF is

`Pr(F≤f)=2 sqrt(f)−f`, `0≤f≤1`,

and its mean is `E[F]=1/6`.

Thus the shallow-past pool is not geometrically homogeneous even along the null boundary: candidates vary greatly in the number of future descendants. This is relevant to insertion-window selection weights, which depend on the relative ranks of successors.

## Computational check

`chronos_shallow_past_null_coordinate_audit_20261111.py` simulates 300,000 independent volume-uniform distinguished locations at each of `N=1000` and `N=10000`, weighting locations by their exact conditional probability `(1−S)^(N−1)` of zero predecessors. Fixed seeds; standard library; no repo mutations.

Output:

```
N=1000 P(minimal)=0.14541833 mean_U=0.704918 mean_future=0.121611
N=10000 P(minimal)=0.04984770 mean_U=0.683622 mean_future=0.145310
NULL_COORDINATE_EXPECTED_INTENSITY := MONTE_CARLO_PASS
U_LIMIT_DENSITY := 2*u
T_LIMIT_CONDITIONAL_EXACTLY_J_PREDECESSORS := Gamma(j+1/2, 1)
LINEAR_EXTENSION_SELECTION_WEIGHT_LIMIT := OPEN
```

Limiting values: `E[U]→2/3`, `E[F]→1/6`. At finite N convergence need not be fast.

## Hard open boundary

The resulting intensity law is **not** the law of the first event under a uniformly selected natural linear extension. The latter reweights candidates by `e(P\{x})/e(P)` and can strongly favor events with more future successors. The exact insertion-window formula in `chronos_insertion_rank_result_20261111.md` identifies the missing rank distribution.

**NEXT:** Prove a limit theorem for the earliest-successor insertion-window rank `R_x` for geometry-conditioned minimal elements, or determine the resulting first-birth density by an independently reproducible bounded coupling calculation. Only after that should the iterated Minkowski uniform-subset limit be asserted.

References: De Loof–De Meyer–De Baets (2006) on linear-extension rank methods, DOI 10.3233/FUN-2006-712-309; Brightwell–Łuczak (2012) on order-invariant measures, DOI 10.1017/S0963548311000721. These sources do not assert the geometric limit proved here.
