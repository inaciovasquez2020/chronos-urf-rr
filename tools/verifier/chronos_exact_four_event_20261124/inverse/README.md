# Inverse reconstruction: low-order causal census non-identifiability

Scope: abstract measured strict partial orders, with IID sampling. This does not assert non-identifiability within smooth Lorentzian manifolds.

## Minkowski-matched example

Take the disjoint union of a nonatomic totally ordered component of mass h=(1/350)^(1/3), a height-two component with lower and upper type masses (a,b) each, incidence matrix [[1,1],[1,0]], and an unrelated antichain of remaining mass. Distinct samples of a single bipartite type are incomparable. No relations cross components.

Put k=(1/10-h^2)/2 and b=(k-a^2)/(2a). Pair comparability is h^2+2(a^2+2ab)=1/10. Three-chain probability is h^3=1/350. Each induced three-event fork probability is 3[a(a+b)^2+b*a^2]=3(a^3+3a^2*b+a*b^2). Set this to 9/350. The certificate brackets h and a rationally, checks opposite signs uniformly in the allowed k interval (the fork expression increases with k for positive a,b), and verifies positive masses and total assigned mass below one. Continuity and the intermediate value theorem give a root. Expected comparable pair count and normalization then give the remaining triple probabilities 33/175 and 53/70.

Four-chain probability is h^4, strictly greater than the flat 4D Minkowski value 1/29400 (standard chain-abundance formula). This separates the distributions without relying on the candidate exact common-future formula. The common-future second moment of this construction is h^4/6+a^4+4a^3*b+2a^2*b^2. The script checks a rational lower bound greater than 9/10000.

## Eight-type examples

Two equally weighted height-two orders have bipartite comparability graphs C8 and C4 disjoint union C4. Exhaustive enumeration of IID ordered tuples, including repeated types, verifies identical labeled censuses through size three and distinct common-future moments 3/512 and 1/128.

## Reproduction

Run in this directory with Python 3 (standard library only):

    shasum -a 256 -c SHA256SUMS
    python3 -B chronos_inverse_reconstruction_certificate.py

Compare output with chronos_inverse_reconstruction_receipt.txt. The script verifies rational inequalities and finite enumerations; the measured-order construction and IVT argument are paper-level. Minkowski census constants are inputs from the parent research program, not independently derived by this script. No Lean verification or scholarly novelty claim. This is an additive companion to PR #1379.
