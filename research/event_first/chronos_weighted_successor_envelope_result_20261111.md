# Sharp successor-weighted envelope for first birth in a 4D Minkowski interval

Date: 2026-11-11. Scope: analytic expectation asymptotic and rigorous limit upper bound. Paper proof: PROVED. Deterministic numerical check: COMPUTATION_PASS. Lean NOT_RUN; independent review and novelty OPEN; spacetime emergence and gravitational dynamics OPEN.

## Definitions and exact finite-N identity

Let N independent volume-uniform events be sprinkled into the normalized 4D Minkowski Alexandrov interval. Let X_1 be the first element of a uniformly sampled natural linear extension. For each event z let D(z),V(z) be its numbers of predecessors and strict successors. Let

W_N(K) = E[Σ_z 1{D(z)=0,V(z)<=K}(V(z)+1)].

For any finite poset, P(X_1=z|P)<= [V(z)+1]/N when z minimal. Therefore, for every N and integer K>=0,

P(V(X_1)<=K) <= W_N(K)/N.                        (1)

With (u,w) null radial coordinates, 0<=w<=u<=1, normalized volume density 12(u-w)^2, s=(uw)^2, f=((1-u)(1-w))^2, a=1-s-f, m=N-1, the exact marked multinomial identity is

W_N(K) =
12N ∫_0^1 ∫_0^u (u-w)^2
 Σ_{ell=0}^{min(K,m)} (ell+1) binom(m,ell) f^ell a^(m-ell) dw du.        (2)

No linear-extension distribution is approximated in (1) or (2).

## Theorem: sharp weighted-candidate double asymptotic

For EVERY integer sequence K_N→∞ with K_N=o(N),

W_N(K_N) / K_N^(3/2) → 2 sqrt(pi).                 (3)

Consequently, uniformly along any such sequence,

P(V(X_1)<=K_N) <= (2 sqrt(pi)+o(1)) K_N^(3/2)/N. (4)

This sharpens the previous loose universal constant below 167 for the **candidate-weighted envelope**, but does not improve its N^(2/3) exponent.

### Proof of (3)

Condition on distinguished z having zero predecessors. Then V is Bin(m,p), p=f/(1-s). Thus the summand in (2) equals
(1-s)^m E[(V+1)1{V<=K}|D=0,z].

Set t=1-u, v=t sqrt(N/K), y=w sqrt(N). In the normalized integral for W_N(K)/K^(3/2), the Jacobian N dt dw equals sqrt(K) dv dy. The integrand becomes

12 (u-w)^2 (1-s)^m E[(V+1)1{V<=K}|D=0,z] / K.

For fixed (v,y) with v,y>=0 and v≠1, as N→∞, K→∞, K=o(N):
u→1, w→0, m s→y², mp/K→v², Var(V/K)→0.
Consequently the integrand converges pointwise to
12 exp(-y²) v² 1{0<=v<1}.

Justification for exchanging limit and integral: divide the triangle into the corner u>=1/2,w<=1/2 and its complement. In the corner, s>=(w/2)^2 implies (1-s)^m<=exp(-y²/8) for all large N. Since the truncated weight (V+1)/K is at most 1+1/K, on 0<=v<=5 the integrand is bounded by 24 exp(-y²/8). For v>=5, f>=t²/4, so the conditional mean mp>=m t²/4 >=K v²/8 for N>=2. Hence mp>=2K, and the binomial Chernoff lower-tail estimate gives Pr(V<=K)<=exp(-mp/8)<=exp(-K v²/64). The integrand is then bounded by 24 exp(-y²/8-v²/64), an integrable function independent of N (K>=1). This proves dominated convergence over the corner, extending the integrand by zero outside its moving domain.

On u<1/2, f>=1/16 and K=o(N), so the binomial lower-tail probability is <=exp(-cN) for an absolute c>0. On w>1/2, s>=1/16, so (1-s)^m<=exp(-m/16). Their total rescaled contribution is bounded by a polynomial in N and 1/K multiplied by an exponentially small factor, hence vanishes.

The limit integral is

12 ∫_0^∞ exp(-y²)dy ∫_0^1 v² dv
=12*(sqrt(pi)/2)*(1/3)
=2 sqrt(pi).

## Independent fixed-K check and consistency

For each fixed nonnegative integer ell, the earlier proved corner asymptotic yields

E[# {z:D(z)=0,V(z)=ell}] → 3 pi binom(2ell,ell)/4^ell.

Thus for fixed K,

lim_{N→∞} W_N(K)
=3 pi Σ_{ell=0}^K (ell+1) binom(2ell,ell)/4^ell.

Stirling yields that constant divided by K^(3/2) approaches 2sqrt(pi) as K→∞, independently confirming the leading coefficient of the triangular-limit calculation. The fixed-K limit ALONE would not justify interchanging growing K and N; that is supplied by the preceding dominated-convergence proof.

Exact finite checks:
N=2: E[#isolated]=9/5.
N=3: E[#isolated]=123/50, E[#minimal with exactly 1 successor]=6/25, and W_3(1)=147/50.
These follow from normalized moments E[s]=1/20, E[s²]=1/105, E[sf]=1/2100.

Quadrature diagnostic, 112-point Gauss–Legendre in each of the scaled null-corner variables (tail truncated at v<=4, y<=5; tails negligible for listed K but numerical values are NOT an exact integration certificate):

N,K | W_N(K)/K^(3/2):
3000,15 | 4.082011198
10000,40 | 3.641533681
30000,100 | 3.493770123
100000,220 | 3.466058559
The limiting constant is 2sqrt(pi)=3.544907702. Nonmonotone finite-size behavior is permitted; quadrature does not establish (3).

## Crucial interpretation

The exponent 2/3 is the barrier of **this particular first-birth candidate-weight union estimate**: since W_N(K)~2sqrt(pi)K^(3/2), inequality (1) becomes noninformative when K≫N^(2/3). This does NOT prove that V(X_1) is of order N^(2/3) or that no stronger theorem is possible from additional linear-extension geometry.

The actual first-birth successor distribution, location law, uniformly sampled causal-prefix profile, iterated 4D Minkowski sampling limit, intrinsic spacetime emergence, and gravitational dynamics remain OPEN. Novelty not established; related linear-extension ideal-lattice counting is developed by De Loof–De Meyer–De Baets (2006), DOI 10.3233/FUN-2006-712-309.

No PR #1347 modifications or merges. Research-staging only.
