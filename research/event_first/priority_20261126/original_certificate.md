# Chronos: sharp three-birth covariance / sampling tradeoff

Remote main inspected: 8ada6fe6715806fabbe43115b7d337f45df99f5a. Local Mac not inspected. Paper proof, exact rational computation; Lean NOT_RUN; novelty NOT_ESTABLISHED.

## Model
A naturally labeled strict poset on [n] has i<j for every relation i precedes j. Prefix restriction is maximal-element birth growth. Let L be any law on naturally labeled triples and P its unlabeled law. U(P) chooses uniformly among the distinct natural label presentations of each class. This is equivalent to uniform linear extensions after forgetting automorphism multiplicities (constant within each class). Let Q3 be the unordered three-point IID uniform law in a 4D Minkowski diamond and Q2 the analogous pair law. Write e2=TV(prefix2(L),Q2), e3=TV(P,Q3), e_cov=TV(L,U(P)).

## Independent moment derivation
Use null variables 0<=u<=v<=1 with normalized volume density 12(v-u)^2. The normalized common endpoint future-diamond volume of one point is J=[(1-u)(1-v)]^2. Substituting w=1-u, z=(1-v)/(1-u) yields E[J^s]=3/(s+1) Beta(2s+1,3). In particular E[J]=1/20 and E[J^2]=1/105. The pair comparability probability is 2E[J]=1/10. Given a designated earliest point with both others in its future, the two others are comparable with probability 1/10 by similarity of flat causal diamonds. Thus triple chain probability is 3 E[J^2]/10=1/350. The induced bottom fork probability is 3 E[J^2] minus chain probability =9/350; reflection gives the same upper fork probability. The expected number of comparable pairs is 3/10, so one-edge probability is 3/10-3/350-4*9/350=33/175; remaining antichain probability is 53/70.

The natural-prefix comparability weights for antichain, one-edge, bottom fork, upper fork, chain are 0,1/3,1,0,1. The uniform naturalization of Q3 has pair prefix comparability 16/175, giving delta=3/350.

## Sharp theorem
By the triangle inequality and contraction of total variation under stochastic kernels,
 e2+e3+e_cov >= TV(prefix2(U(Q3)),Q2)=delta.
Indeed TV(prefix2(L),prefix2(U(P)))<=e_cov and TV(prefix2(U(P)),prefix2(U(Q3)))<=e3. The unlabeled pair law is Bernoulli in comparability.
For any x,y,z>=0 with x+y+z=delta, move mass y from antichain to chain in Q3, forming P. Next start with U(P) and move mass z from one natural presentation of the one-edge class with first pair incomparable to its comparable-first presentation. This is feasible since 53/70>delta and (33/175)/3>delta. The resulting L has errors e2=x, e3=y, e_cov=z, exactly. This is a valid finite maximal-birth law by taking conditionals of the prefix distributions (arbitrary valid transitions on null histories). Thus the full lower boundary is sharp. In particular under exact covariance e_cov=0, inf max(e2,e3)=3/700; with all three errors allowed, inf max=1/350. Exact Q2,Q3 requires covariance defect at least 3/350, attainable. These are finite-prefix constraints, not obstructions to asymptotic uniform-subset sampling or all non-CSG growth. No independent intrinsic continuum dynamics is constructed. No density law or physical prediction is derived.

## Reproduce
Run `python3 -B verify.py` (stdlib only) and compare to receipt.txt. The computation enumerates seven natural presentations, confirms moment arithmetic, and checks 176850 rational tradeoff parameter cases; the analytic argument proves the continuum of cases. The finite check is not a Lean proof. Prior art: Brightwell and Georgiou, Continuum limits for classical sequential growth models; Brightwell and Luczak, Order-invariant measures on causal sets (arXiv:0901.0240); existing repo tools/verifier/chronos_exact_four_event_20261124/inverse/README.md gives the Q3 census. The new application is not claimed novel pending theorem-level review.
