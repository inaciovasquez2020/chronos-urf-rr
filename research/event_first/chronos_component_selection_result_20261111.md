# Direct-sum selection bias: shallow-past scaling is not identifying

2026-11-11. STATUS: PROVED (elementary finite combinatorics); exact finite code COMPUTATION_PASS; Lean NOT_RUN; independent review OPEN; 4D Minkowski limit OPEN.

## Theorem — direct-sum linear-extension factorization

Let a finite poset be the disjoint union P = P_1 ⊔ ... ⊔ P_m, with |P_i| = L_i and N = Σ L_i. A uniform linear extension of P can be sampled by first choosing, independently, a uniform extension of each P_i and then choosing a uniformly random interleaving of the component words with fixed symbol counts L_i. Therefore:

1. The probability that the first birth belongs to P_i is L_i/N.
2. Conditional on its component, the identity of the first birth follows the corresponding local uniform-linear-extension distribution.
3. The first two births both belong to component i with probability L_i(L_i−1)/[N(N−1)]. Conditional on that event, their internal order is given by the first two births of a uniform extension of P_i.
4. As different components have no causal relationships, writing c(P) for the probability that the first two births are comparable,

   c(P) = Σ_i [L_i(L_i−1)/(N(N−1))] c(P_i).

For a disjoint union of chains c(P_i)=1 when L_i≥2, giving the exact formula

   c(P) = Σ_i L_i(L_i−1)/[N(N−1)].

This formula depends on component sizes quadratically. It cannot be determined merely from the number of minimal elements or the count of points with shallow causal past.

## Explicit asymptotic counterexamples

Let m=floor(sqrt(N)).

- Family A: one chain of length N−m and m singleton chains. The number of minima is m+1=Θ(sqrt(N)). The number with <n predecessors, for each fixed n, is m+min(n,N−m)=Θ(sqrt(N)). Yet c(P_N)=(N−m)(N−m−1)/[N(N−1)] → 1.
- Family B: m disjoint chains with balanced lengths floor(N/m),ceil(N/m). The number of minima is m=Θ(sqrt(N)). The number with <n predecessors, for fixed n and sufficiently large N, is mn=Θ(sqrt(N)). Yet c(P_N)=Σ_i L_i(L_i−1)/[N(N−1)] = O(1/m) → 0.

Thus matching Θ(sqrt(N)) scaling for all fixed-depth shallow-past populations neither fixes the early-birth pair statistic nor determines a target of 1/10. The counterexamples are not themselves Minkowski sprinklings and do not disprove their sampling limit.

## Validation

`chronos_component_selection_counterexample_20261111.py` uses exact rational arithmetic and integer extension-counting DP. It independently confirms the direct-sum formula and component first-birth weights on all 65 integer partitions of N=2..8, then computes the two families for N=100,10000,1000000. Exact source executed 2026-11-11 in the assistant's sandbox, PASS. No Mac/Lean/repository CI run is claimed.

N=100: family A c=89/110, family B c=1/11.
N=10,000: family A c=9899/10100, family B c=1/101.
N=1,000,000: family A c=998999/1001000, family B c=1/1001.

## Strict research boundary

The missing mathematical input is NOT the growth rate of shallow-past candidate counts; it is the **linear-extension-weighted selection law** among geometrically correlated candidates in a 4D sprinkled diamond. In particular the rank insertion-window mean E[B_x] conditional on the random geometric order remains uncontrolled. The results prove a genuine nonidentifiability theorem for abstract finite-poset models, not an asymptotic statement about Minkowski geometry, metric-free spacetime emergence, or gravity.

Novelty relative to literature: NOT_ESTABLISHED. The uniform interleaving formula for disjoint posets is standard; the construction is a targeted obstruction in the present program.