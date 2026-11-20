# Chronos: sharp transfer from first-choice weight to all fixed prefixes

Date: 2026-11-15. Status: PROVED conditional on published Fishburn correlation inequality; exact small-poset regression COMPUTATION_PASS. No claim of novelty or Minkowski convergence. Lean NOT_RUN; Git changes NOT_PERFORMED.

## Setting

Let P be a finite poset with N>=2, M its set of original minimal elements, and L a uniform random linear extension. Put q_x = e(P\\{x})/e(P) for x in M and q_* = max_{x in M} q_x. The random prefix I_n = {L_1,...,L_n} is an ideal. Let p(P,n) be the expected fraction of comparable unordered pairs in I_n.

For any n<=N define A_n={L_1,...,L_n subseteq M}, i.e. no originally nonminimal vertex is used in the first n positions.

## Main finite theorem

Define h_k = min(1, k (N q_* -1)/(N-k)) for 0<=k<N. Then for 1<=n<=N,

    Pr(A_n) >= product_{k=0}^{n-1} (1-h_k),
    0 <= p(P,n) <= Pr(A_n^c) <= 1 - product_{k=0}^{n-1}(1-h_k).

In particular for 2<=n<N,

    p(P,n) <= binom(n,2) * N q_* / (N-n).

The survival product is attained as equality for disjoint unions of m equal-length chains (for all n<=m). Hence the product bound is sharp as a universal theorem in terms of N and q_*.

## Proof

Fishburn's inequality (see Chan--Pak, survey, Section 7.1, Theorem 7.1) says for distinct minimal elements x,y of any r-element poset Q:

    e(Q)e(Q\\{x,y})/(e(Q\\{x})e(Q\\{y})) >= r/(r-1).

Equivalently q_y(Q\\{x}) >= [r/(r-1)] q_y(Q).

Fix an initial sequence S=(x_1,...,x_k) consisting of distinct original minima. Each y in M not selected is minimal throughout the deletion sequence. Iterating the inequality gives

    q_y(P\\S) >= [N/(N-k)] q_y(P).

Sum over the remaining originally minimal elements. The conditional probability of taking some originally nonminimal element next is at most

    1 - [N/(N-k)](1 - sum_{x in S} q_x(P))
      = [N sum_{x in S} q_x(P)-k]/(N-k)
      <= k(Nq_*-1)/(N-k).

Because the true hazard lies in [0,1], it is at most h_k. Multiplying the conditional survival probabilities proves the product bound. On A_n all selected vertices belong to M and are pairwise incomparable; hence p(P,n)<=Pr(A_n^c). Finally, by the union bound and N-k>=N-n,

    Pr(A_n^c) <= sum_{k=0}^{n-1} k N q_* /(N-k)
                <= binom(n,2) N q_* /(N-n).

The inequality Nq_*>=1 follows from sum_x q_x=1 and |M|<=N.

## Sharpness

For m disjoint chains of equal length L, N=mL, each original minimal has q_x=1/m. Conditional on k distinct chains already selected, the next vertex is from a previously selected chain with probability k(L-1)/(mL-k) = h_k. Therefore

    Pr(A_n)=product_{k=0}^{n-1}[1-k(L-1)/(mL-k)]
           =(m)_n L^n/(mL)_n,

for n<=m, attaining the survival-product bound. This does not imply the bound on p(P,n) itself is always sharp.

## Consequence for random Minkowski sprinklings

For the N-point sprinkled poset P_N, let Q_N=max_{x minimal} e(P_N\\{x})/e(P_N). For every fixed n,

    E[p(P_N,n)] <= binom(n,2)*N/(N-n)*E[Q_N].

Thus **if Q_N->0 in probability**, boundedness 0<=Q_N<=1 implies E[Q_N]->0; then the entire fixed-n prefix converges to an antichain in probability, and the iterated expected comparable-pair limit exists and equals ZERO:

    lim_{n->infty} lim_{N->infty} E[p(P_N,n)] = 0.

Consequently the proposed nonzero benchmark 1/10 cannot hold jointly with such first-choice delocalization. The first-choice delocalization hypothesis is OPEN for Minkowski; this theorem does NOT refute the conjectured benchmark.

More generally, if a positive iterated expected limit is proved, then the first-choice weights cannot vanish in probability. This is a **necessary**, not sufficient, condition for that particular positive limit.

## Regression

`chronos_first_choice_full_prefix_fishburn_20261115.py` computes uniform linear-extension counts using exact DP, all original-minimal-prefix probabilities, and the actual mean comparability of every prefix length 2..4 across all 219 labeled 4-posets: 657 checks PASS, 499 exact survival equalities and 158 strict cases. An additional 484 rational equal-chain product equalities PASS. Those finite tests do not establish the published Fishburn inequality.

Reference: Chan--Pak, *Linear Extensions of Finite Posets*, Section 7.1, Theorem 7.1, https://www.math.ucla.edu/~pak/papers/LEsurvey11.pdf (survey) and P. Fishburn's original correlation theorem.

OPEN: geometric distribution of Q_N, Minkowski fixed-n laws without extra assumptions, exact p_(4,2), Minkowski infinite double limit. Lean NOT_RUN. Repository unchanged.
