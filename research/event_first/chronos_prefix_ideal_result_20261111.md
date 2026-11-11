# Chronos causal-prefix order-ideal audit — 2026-11-11

Repository reference only: inaciovasquez2020/chronos-urf-rr; preserved PR #1347 HEAD abef2b3e61dcb24a3ebb65ad0df7a76f63d4869f. This study did not mutate the repository.

## Theorem (exact finite conditional prefix law)
Let P be an N-element finite poset, let E be uniformly chosen among its e(P) linear extensions, and let I_n be the set of its first n elements. For every n-element order ideal I,

    Pr(I_n=I | P) = e(I) e(P\I) / e(P).

Proof: a linear extension with prefix I is exactly a concatenation of a linear extension of I and of the induced complement; downward closure ensures every concatenation is allowed. Counting gives the formula. Other subsets have probability zero.

For any induced-order k-subset statistic T_k, interpreted as the count of subsets possessing a specified k-point order,

    E[ T_k(I_n) / binom(n,k) | P ]
      = sum_{I ideal, |I|=n} e(I)e(P\I) T_k(I) / (e(P)binom(n,k)).

The pair statistic T_2 counts comparable unordered pairs; T_3 counts totally ordered triples.

## Exact computational methodology
Minkowski diamond D={|t|+r<1}, sampled uniformly in 4-volume: abs(t)=1-U^(1/4), sign equally likely, r=(1-abs(t))*V^(1/3), direction a normalized three-component Gaussian. All coordinate operations are pseudorandom floating point; causal-order predicate uses strict Minkowski comparison. Every linear-extension count and conditional prefix-ideal probability is then computed with integer dynamic programming over predecessor ideals. Independent brute-force enumeration for four small test posets agrees with DP for each prefix length. Fixed RNG seed 20261111, Python standard library only, no installs.

Bounded test: N=8,12,16; repetitions=80,80,70, respectively. Max visited dynamic-program states across test orders: 256, 3072, 65536. Complete, runtime about 11 seconds on analysis container. Resource guards MAX_IDEALS=150000, MAX_SECONDS=35; resource/time guard triggers INCOMPLETE not PASS.

|N|n|Mean comparable-pair fraction in prefix|Mean full-sample fraction|Paired difference|SE of difference|
|--:|--:|--:|--:|--:|--:|
|8|2|0.0575385|0.1044643|-0.0469258|0.0094932|
|8|4|0.0733935|0.1044643|-0.0310708|0.0064543|
|8|6|0.0874354|0.1044643|-0.0170289|0.0044209|
|12|2|0.0879975|0.1039773|-0.0159798|0.0130166|
|12|6|0.0842789|0.1039773|-0.0196983|0.0055706|
|12|10|0.0937446|0.1039773|-0.0102326|0.0028967|
|16|2|0.0536426|0.0980952|-0.0444526|0.0093053|
|16|8|0.0691607|0.0980952|-0.0289346|0.0053768|
|16|14|0.0874812|0.0980952|-0.0106140|0.0024064|

These are Monte Carlo estimates over finite sprinklings, NOT exact expectation integrals and NOT a theorem of asymptotic nonconvergence. Each per-realization conditional prefix average is exact. Full-sample uniform-pair expectation is 1/10.

## Open boundary
The metric-free future target is a generally covariant, projectively consistent all-N law with uniform-subset induced-order limit Q_k^(4), for every k. For the presupposed-Minkowski test construction, show or refute

    lim_{n->infty} limsup_{N->infty} d_TV(R_{N,n,k}, Q_k^(4)) = 0.

Control of weighted order ideals e(I)e(P\I)/e(P) is a concrete analytic route. A limit for the first two births alone neither proves nor refutes this uniform-tail condition.

STATUS: exact ideal theorem PROVED; code checks COMPUTATION_PASS; N->infty and intrinsic dynamics OPEN; Lean NOT_RUN; repository unchanged.