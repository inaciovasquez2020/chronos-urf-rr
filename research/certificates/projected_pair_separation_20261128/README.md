# Projected 5D comparable-pair separation — exact rational certificate

**Status:** PROVED with an exact computational enclosure under the specified sampling laws; COMPUTATION_PASS (fresh Python replay, 2026-11-28). Continuum Lean formalization, independent review and novelty remain OPEN. No physical detection or necessity of 5D is claimed.

## Model and scope

Use the expanding-circle metric and a common-lift causal diamond as in the pinned [direct 5D calculation](https://github.com/inaciovasquez2020/chronos-urf-rr/blob/951e0be09895080446cb374c79a87d90d048b1dd/docs/status/CHRONOS_DIRECT_5D_COMPARABLE_PAIRS.md). In dimensionless coordinates the diamond is |s|+||X||<1, X in R^4. The full 5D sampling density relative to flat volume is proportional to (1-epsilon*s)^(-5). The observable projects out one spatial coordinate and tests comparability in the visible 3+1 flat conformal order. The comparator is the [matched 4D Einstein-frame volume sampling prescription](https://github.com/inaciovasquez2020/chronos-urf-rr/blob/951e0be09895080446cb374c79a87d90d048b1dd/docs/status/EXPANDING_CIRCLE_CHRONOS_PAIR_MATCH_2026_11_15.md), with density proportional to (1-epsilon*s)^(-6) in its own 4D diamond. Assume IID event sampling, 0 <= epsilon < 1, and no circle wrapping as in the antecedent. These are different observation/sampling prescriptions, not a test against all 4D models.

The flat full-5D pair probability is 128/3003 and the flat matched-4D probability is 1/10 (as derived in the pinned antecedents).

## Exact enclosure proof

At epsilon=0 the time marginal is (5/2)(1-|s|)^4. Conditional on s, the visible spatial radius r=(1-|s|)u has u density proportional to u^2 sqrt(1-u^2) on [0,1]. Indeed the projection of the uniform 4-ball has visible density proportional to the hidden-coordinate interval length 2 sqrt(R^2-r^2), with R=1-|s|. The visible direction is uniform on the 2-sphere and independent of u and s.

For two radii r1,r2>0, the dot product of independent unit directions is uniform on [-1,1]. Hence conditional visible comparability is clamp((d^2-(r1-r2)^2)/(4*r1*r2),0,1), where d=|s1-s2|. Zero radii are a null event. The flat probability is the expectation of this function under the two independent time/radius laws.

Divide s into 2n uniform bins and u into m uniform bins. A time bin has exact probability (h^5-l^5)/(2*n^5), with l=n-max(|i|,|i+1|), h=n-min(|i|,|i+1|). On each u subinterval [k/B,(k+1)/B], B=128m, the unnormalized radial integrand is bounded below by its left u^2 endpoint times its right square-root endpoint, and above by its right u^2 endpoint times its left square-root endpoint. Integer square roots rounded down/up give rational enclosures; common mesh factors cancel on normalization. Dividing lower bin mass by upper total mass and upper bin mass by lower total mass preserves the probability bounds. Products of time/radial bin masses are rounded outward on scale W=10^7.

The radius range of each cell is enclosed by the nonnegative endpoint products. For each pair of cells, use the minimum/maximum absolute time separation and the maximum/minimum absolute radius difference to bound the positive-part numerator. Use maximum/minimum radius products for the respective lower/upper denominators. Clamp at one and round outward on scale P=10^4. When the lower denominator is zero, use upper bound one unless the numerator upper bound is zero, in which case the angular probability is zero almost everywhere in the cell. The lower denominator used for the lower bound is the maximum product; the code also guards zero denominators. Nonnegative cell mass and angular bounds multiply monotonically. Summing all ordered pairs proves the rational enclosure; it does not rely on quadrature convergence. Integer overflow guards are included for the fixed-width array operations.

At n=64, m=48, the replay checks 6,144 cells and 37,748,736 ordered cell pairs:
- lower = 8275160238605137/125000000000000000
- upper = 4742794168850431/50000000000000000

The lower exceeds 128/3003 and the upper is below 1/10.

## Explicit nonzero interval

Let B_k(e)=((1-e)^(-k)+(1+e)^(-k))/2. For a reflection-invariant pair indicator I and independent flat points, the weighted probability for exponent k is E[I w(s1) w(s2)] / E[w(s)]^2, w(s)=(1-e*s)^(-k).

Time reflection gives E[w]>=1: the reflected average is at least the geometric mean (1-e^2*s^2)^(-k/2)>=1. Convexity gives E[w]<=B_k(e). By AM-GM, the reflected average of w(s1)w(s2) is at least one. By the inequality ab<=(a^2+b^2)/2 and reflection, that average is at most B_(2k)(e), since the even reflected average of w(s)^2 is increasing in |s|<=1. Consequently P_flat/B_k(e)^2 <= P(e) <= P_flat*B_(2k)(e).

Apply the upper bound with k=5 to the projected 5D sample and the lower bound with k=6 to the matched 4D sample. At e=1/50, exact arithmetic yields the projected upper bound 0.09695359476771978 and matched lower bound 0.09833699565070085 (decimal displays only). Monotonicity of B_k gives strict separation for every 0 <= e <= 1/50. Full 5D comparability is also strictly smaller than projected comparability at each such e: the former implies the latter, and the explicit strict collision in [PR #1392](https://github.com/inaciovasquez2020/chronos-urf-rr/pull/1392) persists on an open set of positive density.

## Replay and provenance

With Python and NumPy already available, run from this directory:

    python3 -B projected_pair_exact_bounds.py

Fresh replay in the assistant execution environment reproduced all exact fractions in the original receipt; Python 3.13.5 and NumPy 2.3.5. No Mac build is claimed. The optional SciPy quadrature is exploratory only and is not used in the proof. The original three artifacts are preserved byte-for-byte:

    d665d7229b83946fcdfa9c07c0fb733dd0b2a5a1e354d6a1da001e3bfc707699  projected_pair_exact_bounds.py
    dd4389050e13f796d7153ac51e7c9cea52c6f166e6aef716db0ae6d500eb8c3d  projected_pair_exact_receipt.txt
    9764e8ae0c42e582db70f9bdd1b3df30ddd9b92a88636e6a4579b0e64f562d1b  projected_pair_quadrature.py

Treat a timeout, missing dependency, or guard exit as INCOMPLETE, not PASS. The reported enclosure is not a closed-form evaluation of the integral. The projected event law can be reproduced by a four-dimensional model with a matching probability measure. Physical discrimination, extra-dimension stabilization, empirical validation, and full Lean verification remain open.
