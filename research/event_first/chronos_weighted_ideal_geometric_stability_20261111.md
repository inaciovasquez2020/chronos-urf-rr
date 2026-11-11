# Chronos: weighted-ideal geometric stability audit — 2026-11-11

## Scope and evidence
Remote checkpoint: `inaciovasquez2020/chronos-urf-rr` PR #1347, HEAD `abef2b3e61dcb24a3ebb65ad0df7a76f63d4869f` (previously inspected). No repository mutations. Lean NOT_RUN. Analysis code: `chronos_geometric_ideal_concentration_audit.py`; Python standard library only. The Monte Carlo geometric samples are floating-point; the conditional linear-extension probabilities are exact integer/rational results.

## Geometric anchored ideal
Let D be the Minkowski diamond between p=(-1,0,0,0) and q=(1,0,0,0). For 0<alpha<1, s=alpha^(1/4), q_s=(-1+2s,0,0,0), and A_s=D intersect J^-(q_s). It is a causal down-set of D, has volume alpha vol(D), and the normalized causal-order distribution of k iid points in A_s is identical to that of k iid points in D (homothetic Lorentz transformation).

Given N iid uniformly sampled points in D, let P_N be their causal poset, L a uniformly random linear extension, and I_n be its first n elements. Let A_N be those sampled points belonging to A_s, with M=|A_N|. For any two finite subsets I,A of a common finite poset with |I|=n, |A|=m>=k, c=|I intersection A|, a maximal coupling of their uniform k-subset samples agrees with probability at least

    binom(c,k)/max(binom(n,k),binom(m,k)).

The associated TV bound is

    dTV(Law(S_k(I)), Law(S_k(A)) | I,A) <= min(1, k |I triangle A|/(n-k+1))

for n>=k. If m<k we use the trivial bound 1. Indeed in that case |I triangle A| >=n-m>=n-k+1. Averaging and replacing the missing A-sample on m<k by an independent ideal A_s sample establishes

    dTV(Law(S_k(I_n)), Q_k^4)
    <= min(1, k E|I_n triangle A_N|/(n-k+1) + Pr(M<k)).

On M>=k, conditional on M, the k-subset of A_N consists of k iid uniform points in A_s, hence induces exactly Q_k^4. Here M~Binomial(N,alpha).

Therefore, for any n(N)->infinity with n(N)/N->alpha in (0,1), if E|I_n triangle A_N|/n ->0, then dTV(Law(S_k(I_n)),Q_k^4)->0 for every fixed k. This is a SUFFICIENT criterion, not a necessary one. It does not establish the N->infinity THEN n->infinity order of limits from the previous program, and does not imply a non-circular metric-free dynamics.

## Exact conditional mismatch
For any fixed N-poset P and n-element ideal J,

    Pr(I_n=J | P) = e(J)e(P\\J)/e(P).

The conditional inclusion probabilities are evaluated by exact integer forward/backward ideal dynamic programming. Thus

    E[|I_n triangle A_N| | P_N] = sum_{v in A_N} (1-Pr(v in I_n|P_N)) + sum_{v notin A_N} Pr(v in I_n|P_N).

## Bounded experiment
Seed 20261111, N=8 (100 replicates), 12 (100), 16 (80); alpha=1/4,1/2,3/4; guard 150000 cached ideal states, 35 seconds total. Total 840 independent sprinklings (a fresh sprinkling per N,alpha,replicate). Exact fraction arithmetic for conditional ideal inclusion. No resource guard triggered.

N,n,reps,mean E[|I_n triangle A_N|]/n,SE,mean M
8,2,100,1.234614,0.031597,2.11
8,4,100,0.811961,0.012458,3.83
8,6,100,0.444367,0.011691,5.92
12,3,100,1.131541,0.026322,2.78
12,6,100,0.808524,0.012457,6.18
12,9,100,0.403695,0.008415,9.27
16,4,80,1.097272,0.022448,3.888
16,8,80,0.744170,0.012950,8.162
16,12,80,0.400213,0.008835,12.05

An event mismatch divided by n can exceed 1 because |I triangle A| counts both additions and removals, and M is random. Standard errors estimate Monte Carlo uncertainty across independent sprinklings; they do not quantify asymptotic uncertainty. All exact ideal probabilities computed conditionally on floating-point-generated posets. Small exact checks: four-point antichain and four-point total chain PASS.

## Open boundary
No concentration theorem of the required type was established for this Minkowski random-linear-extension construction. Fixed-fraction geometric concentration is a stricter, sufficient property, and its finite-N mismatch is appreciable. Moreover, fixed-fraction convergence is not the iterated N->infinity then n->infinity uniform-tail condition. A useful next theorem is asymptotic control of the relative weighted ideal symmetric difference against *some* homothetic subdiamond, or a weaker bound directly in induced-suborder distance.

The 2006 paper by De Loof, De Meyer, and De Baets treats ideal-lattice counting and random linear extensions; it does not establish the required geometric concentration. See https://doi.org/10.3233/FUN-2006-712-309.

STATUS: universal coupling PROVED; simulation COMPUTATION_PASS; geometric concentration OPEN; spacetime emergence OPEN; Lean NOT_RUN.