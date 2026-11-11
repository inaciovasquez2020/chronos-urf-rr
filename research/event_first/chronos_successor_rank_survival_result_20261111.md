# Exact successor-rank survival domination and correlation penalty

Date: 2026-11-11. Scope: finite-poset theorem. Lean: NOT_RUN. Independent novelty: NOT_ESTABLISHED. Minkowski sampling: OPEN.

## Model

Let P be a finite poset of N points, let x be minimal, and let Q=P\{x}. Write U={y in Q:x<y}, u=|U|, A=Q\U, a=|A|=N-1-u. U is an upper set of Q and A is a lower set. Choose a uniform linear extension tau of Q. Define B to be the position of the first member of U; if U is empty, define B=N. Put S_j=Pr(B>j), j=0,...,N-1.

## Theorem: hypergeometric tail domination

For every j=0,...,N-1,

    S_j >= C(a,j)/C(N-1,j),

where C(a,j)=0 if j>a; and S_j=0 for j>a when U is nonempty. The lower bound is attained whenever there are no cross-relations from A to U, in which case Q is a disjoint union of two induced subposets. The upper bound S_j <= 1_{j<=a} is attained if all A precede all U.

Proof: Fix the internal linear extensions of A and U. A full extension of Q is an interleaving of these two internal orders. The unconstrained interleavings are uniform lattice paths from (0,0) to (a,u), a finite distributive lattice under moving A symbols earlier. Because U is an upper set, the interleavings respecting the cross-relations form a lower ideal of this lattice. The event that the first j letters are all A is another lower ideal. Uniform probability on this distributive lattice satisfies positive association (FKG). Conditioning on one lower ideal cannot reduce the probability of the other lower ideal, so Pr(B>j | internal orders, valid cross-relations) >= C(a,j)/C(N-1,j). This bound is independent of the chosen internal orders, and therefore survives mixing their actual weights under a uniform extension of Q. For j>a no j-prefix can avoid U. The case u=0 gives S_j=1 by convention.

## Exact correlation penalty

For u>=1 define

    Delta_x = sum_{j=0}^{N-1} [S_j - C(a,j)/C(N-1,j)] >= 0.

The free-shuffle survival sum is N/(u+1). Therefore

    E[B] = N/(u+1) + Delta_x,
    Pr_P(x first) = e(P\{x})/e(P) = 1/E[B]
                  = (u+1)/[N+(u+1) Delta_x].

This is an exact identity. The correlation penalty is zero for a disjoint union of the A/U induced subposets and can be positive if they have cross-relations. It depends on the full poset, not only |U|.

## General prefix-selection bounds

The insertion identity also gives

    q_n(x) = [sum_{j=0}^{n-1} S_j]/[sum_{j=0}^{N-1} S_j]

and the explicit size-only inequalities

    [sum_{j=0}^{n-1} C(a,j)/C(N-1,j)]/(a+1)
       <= q_n(x)
       <= min(1, n*(u+1)/N).

The upper bound uses E[min(n,B)]<=n; the denominator E[B]>=N/(u+1). It is generally loose; in particular it does not determine selection inside a 4D causal-diamond shallow-past shell. If u=0, q_n(x)=n/N exactly.

## Four-event Minkowski-realizable example

P: x<b, x<a, z<a. Q: these same relations plus b<a. In both cases N=4, U(x)={a,b}, a=1, and the free-shuffle expected B is 4/3. In the first poset, S_1=2/3, Delta_x=1/3, E[B]=5/3, Pr(x first)=3/5. In the second, S_1=1/2, Delta_x=1/6, E[B]=3/2, Pr(x first)=2/3. Thus the correlation penalty accounts exactly for the different probabilities.

## Exact validation

A dependency-free Python script `chronos_successor_rank_survival_20261111.py` enumerated all forward-edge closures through N=6, verifying 358,906 nontrivial finite survival comparisons; it also verified insertion prefix probabilities against an independent full-poset extension-count DP for all prefix lengths. All assertions PASS. This finite validation is not a proof of a new 4D large-N limit.

## Genuine open boundary

For a 4D Minkowski sprinkling, establish the asymptotic law of Delta_x for geometry-conditioned minimal x, including correlations between future and incomparable events. The present inequalities leave a macroscopic gap. Do not infer order-ideal sampling convergence, spacetime emergence, or gravity.

Primary background: Brightwell–Luczak, *Order-Invariant Measures on Fixed Causal Sets* (2012), DOI 10.1017/S0963548311000721; De Loof–De Meyer–De Baets, *Exploiting the Lattice of Ideals Representation of a Poset* (2006), DOI 10.3233/FUN-2006-712-309. The elementary shuffle-lattice positive-association argument does not establish independent novelty.