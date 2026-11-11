# Chronos: Optimal Bayes ideal concentration audit (2026-11-11)

## Scope
Read-only analysis in container. Preserved remote checkpoint `inaciovasquez2020/chronos-urf-rr`, PR 1347, `abef2b3e61dcb24a3ebb65ad0df7a76f63d4869f`. No Git operations, Lean NOT_RUN. Complete executable: `chronos_bayes_ideal_concentration_audit.py`, SHA-256 `9da970d43b9caeb5569da652577791bdca7847ac66db11adc380782041d4b1c5`.

## Theorem (unrestricted finite poset)
Let P be a finite poset with N vertices; let I_n be the n-vertex initial ideal under a uniformly random linear extension. Let q_n(x)=Pr(x in I_n | P). If x<y, q_n(x)>=q_n(y). Thus A*={x:q_n(x)>1/2} is an ideal. For any fixed subset A, conditional expected symmetric difference is sum over x in A of (1-q_n(x)) plus sum over x outside A of q_n(x). Consequently the minimum over all ideals (indeed all subsets) equals sum_x min(q_n(x),1-q_n(x)); it is attained at A*. For exactly n vertices, a topological tie-breaking of the n largest q values defines an ideal and the minimum expected symmetric difference equals 2[n-sum_{j<=n}q_(j)].

The unrestricted Bayes risk / n tends to zero iff there exists a measurable, poset-dependent deterministic ideal with expected normalized symmetric difference tending to zero. Necessity follows from conditional optimality; sufficiency uses A*. For fixed-size n ideal, same conclusion with fixed-size Bayes risk. This statement does not imply the ideal has a geometric subdiamond limit or that induced order statistics converge to Minkowski geometry.

## Computational method
Four-dimensional flat-diamond iid spacetime volume sampling (floating point); exact integer dynamic programming over ideals for total linear extensions and n-prefix marginal inclusion probabilities (Python Fraction). Prefix count n = round(alpha N), alpha=1/4,1/2,3/4. Fixed seed 20261111, independent sprinklings: N=8 (120 per alpha), N=12 (120), N=16 (100), 1020 total. State cap 150000; all these configurations completed. Each threshold-set ancestor closure is checked exactly; optimal risk <= fixed-cardinality optimal risk; optimal risk <= anchored subdiamond risk.

N n reps BayesRisk/n FixedNBestRisk/n AnchoredDiamondRisk/n
8 2 120 0.918862 1.133581 1.225342
8 4 120 0.757375 0.760264 0.815931
8 6 120 0.304786 0.386777 0.451015
12 3 120 0.888750 1.090236 1.135842
12 6 120 0.679477 0.680588 0.784635
12 9 120 0.294350 0.361110 0.427992
16 4 100 0.878823 1.026111 1.140041
16 8 100 0.659437 0.662304 0.747400
16 12 100 0.291514 0.344548 0.409507

Attempted N=20 with original state limit hit STATE_GUARD and is INCOMPLETE; deliberately excluded from standalone published verification script. Do not regard these finite measurements as asymptotic lower bounds or evidence of nonexistence of a general covariant growth law. If one can prove liminf E[BayesRisk/n]>0 at fixed n/N=alpha, then no poset-measurable deterministic ideal can concentrate in normalized symmetric difference. However, even that would not alone refute convergence of induced k-point order laws.

## Literature
De Loof, De Meyer, De Baets (2006), *Exploiting the Lattice of Ideals Representation of a Poset*, DOI 10.3233/FUN-2006-712-309 establishes exact ideal-lattice computations. Limit-shape techniques for random Young tableaux exist (e.g., Pittel and Romik 2007), but their hypotheses are not a theorem for Minkowski sprinklings. Novelty not established.

## Status
PROVED: finite Bayes optimality and equivalence to deterministic ideal concentration. COMPUTATION_PASS: 1020 samples, exact conditional linear-extension marginals. OPEN: positive asymptotic Bayes risk / exact limit shape; all-k uniform tail sampling stability; metric-free selector; emergent gravity. Mac build and Lean NOT_RUN.