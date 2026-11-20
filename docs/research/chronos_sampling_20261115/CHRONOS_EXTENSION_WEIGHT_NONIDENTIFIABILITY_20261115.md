# Chronos: fixed-predecessor profile and global-density non-identifiability

**Date:** 2026-11-15. **Status:** PROVED (self-contained combinatorial construction); finite exact-arithmetic checks PASS; Lean NOT_RUN; Minkowski sampling-stability OPEN; novelty and independent review NOT_ESTABLISHED. No repository mutation.

## Target

Does knowledge of the concentration profile `H_{N,j}/sqrt(N) -> c_j = 3 Gamma(j+1/2)/j!` for every fixed `j`, possibly augmented by a global comparable-pair density tending to `1/10`, determine the limit of the probability that the first two positions of a **uniform random linear extension** are comparable? No.

## Theorem

There are two deterministic sequences `P_N^(0), P_N^(1)` of posets on `N=k^2` elements (`k -> infinity`) such that

1. For every fixed nonnegative integer `j`, `H_{N,j}(P_N^(0)) = H_{N,j}(P_N^(1))` for all sufficiently large `k`, and both values divided by `sqrt N` converge to `c_j`.
2. The fraction of comparable unordered vertex pairs tends to `1/10` in both sequences.
3. The probability that the first two elements of a uniformly random linear extension are comparable tends to `0` for `P_N^(0)` and `1` for `P_N^(1)`. Indeed the same limits hold for the expected comparable-pair fraction in every fixed-length prefix `n>=2`, and therefore for the corresponding iterated limit.

This theorem is **not** about the distribution of an actual Minkowski sprinkling; neither sequence is claimed to be its typical outcome.

## Exact chain-profile construction

Set `N=k^2`, `J=floor(sqrt(k))`, and `M_j=floor(k c_j)` for `0<=j<=J`. The recurrence `c_(j+1)/c_j=(2j+1)/(2j+2)` makes `M_j` nonincreasing. Build a disjoint union `S` of chains: `M_(j-1)-M_j` chains of length `j` for `1<=j<=J`, plus `M_J` chains of length `J+1`. Then for every `0<=j<=J`, exactly `M_j` vertices of `S` have `j` predecessors. Write `s=|S|=sum_(j=0)^J M_j`.

The central-binomial bound `c_j=3sqrt(pi)*binom(2j,j)/4^j=Theta((j+1)^(-1/2))` implies

` s = O(k sqrt J) = O(k^(5/4)) = o(N), `

and `M_J=Theta(k/sqrt J)->infinity`. In particular `s>>J` and `s<N` for large `k`.

## Family with prefix probability tending to zero

Take `S` as the bottom poset. Above **all** its vertices put a two-layer poset `B_1 ⊕ B_2`, where each `B_i` is an antichain, every `B_1` element precedes every `B_2` element, and `|B_1|=floor(beta*(N-s))`, `|B_2|=N-s-|B_1|`, with

` beta=(1-sqrt(4/5))/2. `

All vertices of `B_1∪B_2` have at least `s>J` predecessors. Hence `H_(N,j)=M_j` for `j<=J`.

Every linear extension must finish all of `S` before entering `B_1`. A uniform extension restricts to a uniform extension of `S`. For a disjoint union of chains of lengths `l_i` totaling `s`, chain labels in a uniformly random extension form a uniformly random permutation of the multiset of labels. Thus

` p_(N,2) = sum_i l_i(l_i-1)/(s(s-1)) <= (J+1)/(s-1) -> 0. `

The total unordered comparable-pair count is

` sum_i binom(l_i,2) + s*(N-s) + |B_1|*|B_2|. `

Dividing by `binom(N,2)` and letting `N->infinity` gives `2 beta(1-beta)=1/10`.

## Family with prefix probability tending to one

Remove one of the `M_J` chains of length `J+1` from `S`, calling the remainder `S'` (`|S'|=s-(J+1)`). Let `C` be a single chain of length `L=floor(alpha*N)` with

`alpha=1-sqrt(9/10).`

Set `Q = S' ⊔ C`, and above **all** its vertices put an antichain of size `N-|Q|`. This is feasible for large `k` since `|S'|=o(N)` and `0<alpha<1`.

For `j<=J`, the removed scaffold chain and the new long chain contribute the same one vertex each: `H_(N,j)=M_j`. The bulk antichain has `|Q|>J` predecessors and contributes no fixed-j count.

Every linear extension begins with all `Q`. By the same chain-label shuffle identity,

` p_(N,2) = [L(L-1)+sum_(i in S') l_i(l_i-1)]/[|Q|(|Q|-1)] ->1, `

since `L=alpha*N+o(N)` and `|S'|=o(N)`.

The number of comparable unordered pairs is

` binom(L,2)+sum_(i in S') binom(l_i,2)+|Q|*(N-|Q|). `

Its ratio to `binom(N,2)` tends to `alpha^2+2alpha(1-alpha)=2alpha-alpha^2=1/10`.

**Fixed-length prefixes.** More generally, for any disjoint union of chains, a uniformly random extension induces a uniformly random word in the chain labels with fixed multiplicities. Every unordered pair of distinct word positions has the same probability of carrying the same label, namely `sum_i l_i(l_i-1)/(m(m-1))`, where `m` is the size of the union. The expected comparable-pair fraction within the first `n` word positions therefore equals this same value for every `2<=n<=m`. The lower portions `S` and `Q` must both be fully consumed before their upper bulk is available, so for each fixed `n` the preceding `p_(N,2)` formulas equal `p_(N,n)` for all sufficiently large `N`. Hence the two deterministic families have opposite values of the entire iterated limit `lim_(n->infinity) lim_(N->infinity) p_(N,n)`, despite their matching fixed-j profiles and global comparable-pair densities.

This proves the theorem and its fixed-prefix strengthening.

## An even stronger observation without fixing global density

For two disjoint-union-of-chains families of total size `N` with the **same** `M_j` for every `j<=J`, distribute the surplus `N-s` by giving fraction `a` to one long chain and spreading the remainder evenly among the other `M_J-1` length-`J+1` chains. Then all fixed-j profiles agree, and

` p_(N,2) -> a^2, for any a in [0,1]. `

Thus every target limit in `[0,1]` is compatible with the same entire fixed-j predecessor profile. The two stronger families above additionally fix the global comparable-pair density to `1/10`.

## Consequence for extension-weight ratios

There are `H_(N,1)` comparable two-element ideals and `binom(H_(N,0),2)` antichain two-element ideals. If `bar_w_C`, `bar_w_A` are the averages of `e(P\I)` over these two classes and `rho=bar_w_C/bar_w_A`, the first two positions of a uniform extension give

`p_(N,2)=H_(N,1)*rho / [H_(N,1)*rho + H_(N,0)*(H_(N,0)-1)]`.

The factor of 2 in the antichain weight is essential: each antichain ideal has two internal linear extensions. Since the denominator counts differ by a factor `Theta(sqrt(N))`, our paired counterexamples necessarily have `rho^(0)/sqrt(N)->0` and `rho^(1)/sqrt(N)->infinity` even though their fixed-j counts and global densities match.

A proof of Minkowski-specific stability must therefore use genuinely geometric constraints on the **extension weights**, not only the predecessor statistics and global density. For example, it must estimate the law of `e(P_N\I)` conditioned on the spatial geometry of the ideal `I` and its future relations. The general theory of order-invariant measures is relevant but does not automatically identify this dense-Minkowski limit.

## Tests

- `chronos_matching_all_fixed_predecessor_counts_counterexample_20261115.py`: six finite fixtures, precise rational `p_(N,2)` for two disjoint-chain realizations.
- `chronos_extension_weight_nonidentifiability_audit_20261115.py`: independent brute-force uniform-linear-extension enumeration of six small posets; rational `rho` identity on six larger fixtures.
- `chronos_full_prefix_limit_range_certificate_20261115.py`: rational `a` sweep for continuum of limiting values.
- `chronos_matching_global_density_counterexample_20261115.py`: exact counting in the two stronger fixed-global-density families.

All four scripts PASS locally (std-lib Python); asymptotic conclusions follow from the displayed proof, not numerical extrapolation.

## Open boundaries

Actual four-dimensional Minkowski `rho_N/sqrt(N)` law: **OPEN**. Fixed-n Minkowski linear-extension limits: **OPEN**. Double limit `n->infinity` after `N->infinity`: **OPEN**. Lean: **NOT_RUN**. Repo commit/push/merge: **NOT_PERFORMED**.
