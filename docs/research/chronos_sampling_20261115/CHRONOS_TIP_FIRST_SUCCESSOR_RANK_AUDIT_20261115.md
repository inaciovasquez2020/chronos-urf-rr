# Chronos — first-successor-rank reduction (2026-11-15)

## Theorem 1 (exact finite-poset identity)

Let P be a finite poset of size N and x a minimal element. For a uniformly selected linear extension L of P\{x}, let U_x(L) be the position (1-based) of the earliest strict successor of x in L, setting U_x=N when x has no successors. Inserting x anywhere in slots 1,...,U_x produces precisely all linear extensions of P, bijectively. Consequently

    e(P) = e(P\{x}) E[U_x],
    q_x := P(first=x) = e(P\{x})/e(P) = 1/E[U_x].

Writing d_x for the number of strict successors, there are N-1-d_x other non-successors; hence U_x <= N-d_x and

    q_x >= 1/(N-d_x).

Equality holds iff the first strict successor always follows all non-successors in every extension L of P\{x}; in particular this is true for a disjoint union of x with an antichain and x below all its strict successors in a chain following those antichain elements, when forced by other relations. No asymptotic assertion follows from the bound alone.

## Theorem 2 (uniform geometric lower bound within a fixed rescaled tip)

Let N iid points be uniformly sprinkled in the 4D Minkowski diamond D and 0<T fixed, with T N^{-1/4}<=1/2. Put R_N(T)={points x with time coordinate t_x <=T N^{-1/4}}. For any point x in R_N(T), the future-volume fraction is

    W_+(x)=((1-t_x)^2 - |x_spatial|^2)^2 >= (1-2t_x)^2.

Thus, conditional on its position x, the number B_x of sampled points NOT in the strict future of x, including x, is distributed as 1+Bin(N-1,1-W_+(x)), with binomial mean <=4T N^{3/4}. Let

    mu_max = 4T N^{3/4}, a=3 log N,
    K = mu_max + sqrt(2 mu_max a) + (2/3)a.

The additive Bernstein binomial tail implies

    P(B_x > 1 + K | x) <= N^{-3}.

By union bound over all N indexed samples (regardless of whether they lie in R_N(T)), with probability >=1-N^{-2}, simultaneously for every *minimal* x in R_N(T),

    q_x >= 1/B_x >= 1/(1+K).

This is an O(N^{-3/4}) **lower** bound for tip first-choice weights. It does not prove a nonzero limiting tip mass, nor upper-bound q_x, nor establish Q_N=max_x q_x delocalization.

## Exact finite verification

The companion stdlib script exhausts labeled posets through N=5 (including transitive closures) and checks the reciprocal-rank formula and the lower bound for 8,816 minimal-vertex instances. The geometric future-volume inequalities are checked at 4,995 rational configurations. This computation is not a substitute for the analytic proof and is NOT Lean verification.

## OPEN

1. Distribution/expectation of U_x when x is a tip-minimal point of a large 4D Minkowski sprinkling; estimate competing null-boundary minima.
2. Distribution of Q_N=max_x 1/E[U_x|P_N]; this depends on global order and is not determined by the local Poisson tip limit.
3. Exact four-event p_(4,2) and infinite-growth double limit remain OPEN.

Repository and Mac unchanged; no commit, PR edit, or merge. No Lean compilation.
