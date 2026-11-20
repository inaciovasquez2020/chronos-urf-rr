# Chronos four-point geometry and infinite-prefix weight audit — 2026-11-15

## Scope and scientific boundary

**Independent derivation / exact arithmetic:** the mixed causal-pair integral, the N/K22 linear identity, angular harmonic zero-mode, and one- through five-mode Hilbert–Schmidt masses. Finite exact-extension enumeration and finite predecessor-count identities tested.

**OPEN:** closed-form or otherwise exact full E[J_+(X,Y)^2]; exact p_(4,2); Minkowski N→∞ finite-prefix limits; n→∞ outer limit. No Lean compilation, independent review, mathematical novelty determination, Git promotion, or local Mac inspection occurred.

## Four-point poset identity

D is the unit four-dimensional Minkowski Alexandrov diamond with volume π/24. Define W_-(x)=Vol(J^-(x)∩D)/Vol(D), W_+(x)=Vol(J^+(x)∩D)/Vol(D), and J_+(x,y)=Vol(J^+(x)∩J^+(y)∩D)/Vol(D).

For C≺B, define I(C,B)=Vol(Alexandrov interval(C,B))/Vol(D), A(C,B)=W_-(B)-W_-(C)-I(C,B), B(C,B)=W_+(C)-W_+(B)-I(C,B). The probability (under four fixed labels) of the indicated three causal edges with both endpoint pairs spacelike is X=E[1_(C≺B) A(C,B) B(C,B)]. By full induced-poset enumeration, each N4 contributes once and each K22 four times, so 24X=Pr(N4)+4Pr(K22).

Expand and integrate X. Mixed moments and two-, three-, four-chain constraints reduce X to T-227/705600, where T=E[1_(C≺B) W_-(B) W_+(C)]. In null coordinates a=t−r,b=t+r, joint normalized radial density is 144 (bc−ac)^2(bb−ab)^2. Angular causality probability equals 1 if ac<bc<ab<bb, and (ab−ac)(bb−bc)/[(bc−ac)(bb−ab)] if ac<ab<bc<bb. Each domain is an ordered four-simplex; rational polynomial integration yields T=29663/36036000+266113/504504000=953/705600 and therefore Pr(N4)+4Pr(K22)=121/4900.

With previously certified exact 4-poset algebra Pr(K22)=6E[J_+²]−19/29400, and p_(4,2)=1727/19600−(2/15)Pr(N4)−(1/3)Pr(K22), this yields:

- **Pr(N4)=401/14700−24E[J_+²].**
- **p_(4,2)=3557/42000+(6/5)E[J_+²].**

The unknown remains the full E[J_+²].

## Angular spectral decomposition and certified bound

Use normalized radial/time measure 96r² dr dt on 0<r<min(t,1−t), and normalized spherical measure on S². The causal kernel 1_(x≺y) has angular eigenvalues λ_l(h)=1/2∫_h^1 P_l(u)du (when −1<h<1), extended by 0 when no angle is causal, and λ_0=1, λ_l=0 for l>=1 when all angles are causal. Here h=(r_x²+r_y²−(t_y−t_x)²)/(2r_xr_y) when t_y>t_x.

Write K_l for the radial/time integral operator with kernel λ_l. Set b_l=||K_l||_HS², A_l=(2l+1)Tr[(K_l K_l*)²]. Independence of two lower and two upper points and spherical harmonic orthogonality give E[J_+²]=Σ_l A_l. Every A_l is nonnegative and A_l≤(2l+1)b_l². Also Σ_l(2l+1)b_l=Pr(x≺y)=1/20.

The l=0 term was evaluated by exact integer Dirichlet gap integration over 152 admissible orderings of eight null endpoints: A_0=513/875875. For a single directed pair, b_0=1/35 from two exact ordered-simplex integrals (each 1/70). Therefore Σ_{l≥1}(2l+1)b_l=3/140.

For l≥1, λ_l=f(1−f)R_(l−1)(f), where f=λ_0, and R_(l−1)=2P'_l(1−2f)/(l(l+1)). The exact angular moment integrals reduce to rational partial fractions and ζ(2)=π²/6, yielding:

- b_1 = 6π²−829/14
- b_2 = 258π²−35649/14
- b_3 = 3336π²−32925
- b_4 = 23400π²−8083206/35
- b_5 = 112650π²−155653531/140

Let R=3/140−Σ_{l=1}^5(2l+1)b_l≥0. Because 2l+1≥13 for l≥6, the rigorous residual bound is Σ_{l≥6}A_l≤R²/13. Thus

E[J_+²] ≥ 513/875875,
E[J_+²] ≤ 513/875875 + Σ_{l=1}^5(2l+1)b_l² + R²/13.

A fail-closed standard-library certificate bounds π using Machin's identity  π=16 arctan(1/5)−4 arctan(1/239) with exact rational alternating-series remainders. It proves:

**17950529/210210000 ≤ p_(4,2) < 0.08543935.**

Approximate displayed range: 0.0853933162 to 0.08543935. The upper bound is rigorous; it is NOT a numerical point estimate. QMC exploratory four-event geometry (8×2^20 samples) estimated E[J_+²]≈0.00059813 and p_(4,2)≈0.08540824 with replicate standard error ≈2.72×10⁻⁶ on E[J_+²], but no stochastic confidence guarantee or exact value is claimed.

## Infinite-growth prefix weights

Let H_(N,0) be number of minimal elements, H_(N,1) number with exactly one predecessor. Two-element ideals consist of C: H_(N,1) comparable ideals and A: binom(H_(N,0),2) antichain ideals. Let w(I)=e(P_N\I), and let ρ_N be the mean w over C divided by the mean w over A (when both nonempty). The number of linear extensions with first two forming ideal I is e(I)e(P_N\I). Hence:

p_(N,2) = H_(N,1) ρ_N / [H_(N,1) ρ_N+H_(N,0)(H_(N,0)−1)].

The predecessor-volume fraction W_− of one uniform diamond event has density f(w)=3w⁻¹ᐟ²−3w¹ᐟ²+3ln(w) for 0<w<1. Exact binomial expansion gives for fixed j:

E[H_(N,j)] = 3N binom(N−1,j) B(j+1/2,N−j+1) + 3(H_j−H_N),

where the rightmost H symbols are harmonic numbers, not the predecessor-count random variables. Therefore E H_(N,j)~3Γ(j+1/2)√N/j!, and E H_(N,0)~3√π√N, E H_(N,1)~(3√π/2)√N.

**CONDITIONAL theorem:** If H_(N,0)/√N→3√π and H_(N,1)/√N→3√π/2 in probability, and ρ_N/√N→c≥0 in probability, then p_(P_N,2)→[(3√π/2)c]/[9π+(3√π/2)c] in probability, and its expectation has the same limit. To obtain 1/10 at n=2 requires c=2√π/3. If ρ_N=o_P(√N), this n=2 limit is zero. Neither count concentration nor the weight-ratio scaling is proved for Minkowski sprinklings. This n=2 result alone never determines the full double limit n→∞ after N→∞.

The finite exact-extension sweep N=8,12,16,18,20 is computational evidence, not an asymptotic theorem. Bounds and failed/aborted scripts are not counted as passing proofs.

## Reproduction files

The accompanying archive includes one exact symbolic certificate requiring sympy, three standard-library exact certificates, independent exact normalization audit, and two exploratory scripts (NumPy/SciPy) with an execution receipt and SHA-256 manifest. No source files require Mac access, and no Git write has been made from these results.
