# 4D Minkowski sprinkling: fixed predecessor-count concentration

**Status:** PROVED analytical theorem (independent argument); Lean NOT_RUN; independent external mathematical review NOT_PERFORMED; novelty NOT_ESTABLISHED. This result concerns predecessor counts and **does not** establish uniform-linear-extension prefix sampling stability.

## Setup

Let D be the 4D Minkowski Alexandrov diamond of height 1 between (0,0) and (1,0), with uniform measure and N independent points. For each point q, let `pred(q)` be the number of *other sampled points* in its causal past. Define H_{N,j}=#{q:pred(q)=j}. Null variables a=t−r, b=t+r satisfy 0≤a≤b≤1. Spatial directions n are uniform on S² and independent of (a,b), whose density is 12(b−a)² da db. The past volume fraction is W_−=(ab)².

**Theorem (fixed-j law of large numbers in L²).** For each j≥0 fixed,

    H_{N,j}/sqrt(N) -> c_j = 3 Gamma(j+1/2)/j!

in L². Moreover, for any finite list j_1,...,j_k, the normalized joint factorial moments of the associated predecessor-count variables converge to the products of the corresponding c_j. In particular the covariance between any two fixed-j counts divided by N tends to 0.

## Proof

**One-point scaling.** For b>0 set a=x/(b sqrt N), with 0≤x≤b²sqrt N, so W_−=x²/N. The scaled radial measure is

    sqrt N * 12(b−a)² da db = g_N(b,x) db dx,
    g_N(b,x)=12(b−x/(b sqrt N))²/b * 1_{0≤x≤b²sqrt N}.

Thus 0≤g_N≤12b, and g_N→12b pointwise for b∈(0,1). Conditional on this event's position, its predecessor number is Binomial(N−1,x²/N). For fixed j, the probability converges to exp(−x²)x^{2j}/j!.

For N sufficiently large depending on j, a universal integrable bound is

    Pr(Binomial(N−1,x²/N)≤j) ≤ C_j(1+x^{2j})exp(−x²/2).

This follows from binomial coefficients ≤(N−1)^i/i! and (1−p)^{N−1−i}≤exp(−(N−1−i)p), with (N−1−j)/N≥1/2. Dominated convergence therefore gives

    E[H_{N,j}]/sqrt N -> 12*(int_0^1 b db)*(int_0^∞ exp(−x²)x^{2j}/j! dx)
                          = 3 Gamma(j+1/2)/j!.

**Geometric overlap lemma.** Take two points x_i=(t_i,r_i n_i) with null coordinates (a_i,b_i), fixed b_i>0, a_i→0, and distinct unit directions n_1≠n_2. Any z=(τ,ρ m) in both causal pasts lies in D, so 0≤τ−ρ≤a_i. From the timelike/null relation z≺x_i, the exact identity

    (t_i−τ)²−|r_i n_i−ρ m|²
      = (a_i−(τ−ρ))(b_i−(τ+ρ))−2r_iρ(1−n_i·m)

implies 2r_iρ(1−n_i·m)≤a_i b_i. Put γ=arccos(n_1·n_2)>0 and δ=1−cos(γ/2)>0. For every m, some i has 1−n_i·m≥δ. Eventually r_i=(b_i−a_i)/2≥b_i/4, hence ρ≤2(a_1+a_2)/δ. Also τ−ρ≤min(a_1,a_2), so τ≤[2/δ+1](a_1+a_2). Since the normalized D-volume at τ≤h≤1/2 is 8h⁴, the common-past volume J_−(x_1,x_2) obeys

    0≤J_−≤8([2/δ+1](a_1+a_2))⁴ = O((a_1+a_2)⁴).

Under a_i=x_i/(b_i sqrt N), this implies N J_−→0 at every fixed b_i>0, finite x_i and distinct directions. The pair also becomes incomparable because two distinct future null generators are spacelike separated.

**Two-point factorial moment.** Conditional on the positions of two labeled sampled events, the N−2 other points fall into the past of the first only, the past of the second only, their overlap, or neither, according to a multinomial law with respective probabilities W_1−J, W_2−J, J, 1−W_1−W_2+J. At the scaled positions above, W_i=x_i²/N and N J→0, so for each fixed j,k their predecessor counts converge jointly to independent Poisson(x_1²), Poisson(x_2²). Contributions from the two distinguished events to each other's predecessor counts vanish eventually because they are incomparable.

To justify exchanging limit and integrals, if both full predecessor counts equal fixed j,k, the N−2 other-point counts into each individual past are at most j,k. By Cauchy–Schwarz, the joint probability is bounded by the square root of the product of these two marginal binomial lower tails. The one-point bound gives a constant times

    (1+x_1^{2j})(1+x_2^{2k}) exp(−(x_1²+x_2²)/4),

which is integrable after multiplication by g_N(b_1,x_1)g_N(b_2,x_2)≤144 b_1b_2. Coincident directions and b_i=0 have zero measure. Dominated convergence yields

    E[H_{N,j}(H_{N,j}−1)]/N -> c_j²,
    E[H_{N,j}H_{N,k}]/N -> c_j c_k  (j≠k).

The mean limits imply Var(H_{N,j})/N→0, proving L² convergence.

**Finite multi-point extension.** For any fixed m, choose m distinct null-generator directions. Each pairwise common past has volume o(1/N), so the total probability of points in any overlap of ≥2 individual pasts is o(1/N). The resulting m-variate multinomial predecessor law converges to independent Poisson(x_i²). The joint lower-tail probability is bounded by generalized Hölder using m marginal binomial tails, producing an integrable dominating product. Hence all fixed mixed factorial moments of (H_{N,j}) normalized by N^{m/2} converge to products of c_j. This strengthens, but is not needed for, L² concentration.

## Consequence for two-element ideals

For any finite poset with at least one comparable and antichain two-ideal, define rho_N as the average extension weight e(P\I) on comparable two-ideals divided by that on antichain two-ideals. Then exactly

    p_{N,2} = H_{N,1}rho_N / (H_{N,1}rho_N + H_{N,0}(H_{N,0}−1)).

The theorem now removes **count concentration** from the conditional limit statement. If additionally rho_N/sqrt N -> c in probability for a constant c∈[0,∞), then

    p_{N,2} -> [(3sqrt(pi)/2)c]/[9pi+(3sqrt(pi)/2)c]

in probability (and in expectation by boundedness). The extension-weight ratio asymptotics remain OPEN, as do convergence of p_{N,n} at each fixed n and the outer n→∞ limit. In particular, the global double limit does **not** logically require that the n=2 limit equal 1/10.

## Source assumptions and verification status

The causal relation is Minkowski chronological/causal order (null coincidences have measure zero); N independent uniform events in the fixed diamond; j fixed as N→∞; no curvature, boundary perturbations, or variable j. The proof above uses elementary Lorentzian geometry, binomial-to-Poisson convergence and dominated convergence. It is not a Lean kernel proof. No claims of mathematical novelty or external review are made. Previous exact first-moment certificates are present in the accompanying Chronos archive, but the second-moment concentration argument is new to this audit.
