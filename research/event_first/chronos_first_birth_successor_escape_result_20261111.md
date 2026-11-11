# Four-dimensional first-birth successor escape and null-rim marked intensity

Date: 2026-11-11. Status: PROVED analytically (finite-poset theorem + four-dimensional integral estimates); bounded numeric quadrature PASS. Lean: NOT_RUN. Independent novelty: NOT_ESTABLISHED. Full Minkowski prefix limit and emergent gravity: OPEN.

## Model and notation

In the normalized 4D Minkowski Alexandrov interval with past tip p=(0,0) and future tip q=(1,0), write the radial null coordinates as u=t+r and w=t-r, with 0<=w<=u<=1. The normalized volume density is 12(u-w)^2 du dw. For a point z=(u,w), its causal-past and causal-future volume fractions are

s(z)=(uw)^2; f(z)=((1-u)(1-w))^2; a(z)=1-s(z)-f(z).

Sample N i.i.d. volume-uniform points; let D(z) and V(z) denote the counts of strict predecessors and successors of distinguished z, respectively. Let X_1 be the first event of an independently uniform random linear extension of the sampled poset. Let m=N-1.

## Exact marked-candidate count

For every nonnegative integer ell<=m, the expected number of minimal events with exactly ell successors is

E M_{0,ell} =
 N binom(m,ell) * 12 ∫_{u=0}^1 ∫_{w=0}^u (u-w)^2 f(z)^ell a(z)^(m-ell) dw du.

Reason: given z, the remaining points fall into past, future, incomparable cells with multinomial cell probabilities (s,f,a). The event D(z)=0,V(z)=ell has probability binom(m,ell) f^ell a^(m-ell).

## Theorem A: exact null-rim corner asymptotic

For each fixed ell>=0,

lim_{N→∞} E M_{0,ell} = 3π binom(2ell,ell)/4^ell.

Proof: the only closure point of the normalized (u,w) domain with s=f=0 is the null-rim corner (u,w)=(1,0). Substitute v=√N(1-u), y=√N w. Then for fixed v,y>=0:

N s→ y², N f→v², a^(N-1-ell)→exp(-v²-y²),
binom(N-1,ell) f^ell→v^(2ell)/ell!,
12N (u-w)^2 du dw→12 dv dy.

Gaussian domination holds after splitting off regions u<1/2 or w>1/2 (these are exponentially suppressed for fixed ell), and on the corner region via binomial/Gaussian estimates. Thus dominated convergence yields

12 ∫_0^∞ exp(-y²)dy ∫_0^∞ exp(-v²)v^(2ell)/ell!dv
=3√π Γ(ell+1/2)/ell!
=3π binom(2ell,ell)/4^ell.

In particular, E[#isolated events]→3π, because isolated means D=V=0.

For N=2, exact E[#isolated]=9/5.
For N=3, exact E[#isolated]=123/50, using E[s]=1/20, E[s²]=1/105 and E[s f]=1/2100.

## Theorem B: actual first-born event has many descendants

For each finite poset P of size N, for any minimal x with u_x strict successors,

Pr(X_1=x | P) <= (u_x+1)/N.

This is the previously verified successor-size bound, following from hypergeometric survival domination of the earliest successor insertion rank. Consequently, for any integer K>=0,

Pr(V(X_1)<=K) <= (K+1)/N * E[# {z : D(z)=0, V(z)<=K}].   (*)

For N>=2 and 0<=K<=(N-1)/64, the expected candidate count obeys the explicit estimate

E[# {z : D(z)=0, V(z)<=K}]
<= C * N/(N-1) * sqrt(K+1)
   + N [exp(-9(N-1)/512) + exp(-(N-1)/16)],

where C=12 sqrt(π)(sqrt(8)+sqrt(8π)) <167.

Proof of uniform estimate: for fixed location z,
Pr(D=0,V<=K) <= exp(-m s(z)) Pr(Bin(m,f(z))<=K).
Here conditioning D=0 changes the future success parameter from f to f/(1-s)>=f, so the inequality holds by stochastic monotonicity.

Partition the (u,w) triangular domain into:
(i) u>=1/2,w<=1/2 (the null-rim corner);
(ii) u<1/2; and (iii) w>1/2.

On (i), s>=w²/4 and f>=(1-u)²/4. Integrating the past factor over w gives at most sqrt(π/m). For t=1-u, the future binomial mean is μ=m t²/4. If μ<=2(K+1), the t-interval has length at most sqrt(8(K+1)/m); otherwise the multiplicative Chernoff inequality bounds the lower tail by exp(-μ/8)=exp(-m t²/32), whose integral is at most sqrt(8π/m). Multiply these estimates by normalized volume-density upper bound 12.

On (ii), f>=1/16 and K<=m/64 implies K<=μ/4, so Chernoff gives Pr(V<=K|D=0)<=exp(-9m/512). On (iii), s>=1/16 gives Pr(D=0)<=exp(-m/16). Each complementary region has normalized measure at most one.

Combining with (*) gives the explicit uniform first-birth bound:

Pr(V(X_1)<=K)
<= C (K+1)^(3/2)/(N-1)
   + (K+1)[exp(-9(N-1)/512)+exp(-(N-1)/16)].

Hence for every integer sequence K_N=o(N^(2/3)),

Pr(V(X_1)<=K_N)→0.

In particular, for each fixed ε with 0<ε<2/3,
Pr(V(X_1)>N^(2/3-ε))→1.

**This statement concerns the ACTUAL first event selected by a uniform random linear extension, not merely the candidate intensity.** It does NOT imply that V(X_1)/N stays bounded away from zero.

## Corollary: isolated first-birth rate

For an isolated x in any N-poset, Pr(X_1=x|P)=1/N. Summing and averaging,

Pr(X_1 isolated) = E[#isolated]/N ~ 3π/N.

## Independent checks

The companion numerical certificate used exact rational low-N checks, exact gamma/binomial identities ell=0..6, and Gaussian-scaled deterministic two-dimensional quadrature with SciPy Gauss-Legendre 200×200 nodes.

Expected marked counts for ell=0,1,2:
N=100: 8.2916535,3.8391060,2.7228615
N=1000: 9.0822460,4.4538012,3.2966383
N=10000: 9.3178239,4.6320179,3.4605650
Limit: 3π, 3π/2, 9π/8 =9.4247780,4.7123890,3.5342917

Quadrature and finite checks are NOT substitutes for the above analytic proofs. This exercise does not formally prove source originality.

## OPEN boundary

The first-birth successor count is now shown to exceed any o(N^(2/3)) threshold in probability. The theorem does not identify its order-N distribution or the uniformly selected first-n prefix's causal comparability profile. The geometry-conditioned insertion-barrier correlation penalty remains unbounded at the scale needed for that objective; iterated Minkowski uniform-subset convergence and emergent gravitational dynamics remain OPEN.

Neither PR #1347 nor any production branch was modified; research is isolated on research/event-first-audit-staging-20261111.
