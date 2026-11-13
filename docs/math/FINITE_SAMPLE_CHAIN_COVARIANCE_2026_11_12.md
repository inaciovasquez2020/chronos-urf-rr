# Exact finite-sample covariance of 4D causal-chain fractions

**Status (2026-11-12):** PROVED by finite-index overlap counting, rational flat-diamond monomial integration and exact polynomial integration on ordered simplices. An independent stdlib-only exact-arithmetic verifier and numerical cross-check are described below. This is **not** Lean verification or a derivation of emergent spacetime or gravitational dynamics. Novelty NOT ESTABLISHED. Mac execution NOT_RUN.

## Exact sampling model

Fix the four-dimensional flat Minkowski causal diamond D between p=(-1,0) and q=(1,0) (volume 2π/3), and condition on **exactly N≥3 independent uniform events**. This is fixed-cardinality/binomial sprinkling, not unconditioned Poisson sampling. Let U2 be the fraction of unordered pairs that are causally comparable, U3 the fraction of unordered triples that form totally ordered 3-chains. Their exact means are p2=1/10 and p3=1/350. We follow the previously merged [restricted local-identifiability result](../status/CAUSAL_CHAIN_LOCAL_IDENTIFIABILITY_2026_11_10.md).

## Complete exact covariance for N≥3

```
Var(U2)    = (2N+5)/(50 N(N-1))

Cov(U2,U3) = 9(N+3)/(3500 N(N-1))

Var(U3)    = (527N^2+4990N+26355)/(2695000 N(N-1)(N-2)).
```

This fully specifies the **finite-N joint covariance matrix** for the two observables at the flat baseline. No asymptotic approximation is used in these three entries.

### One-point conditional kernels

Let r=|spatial x| and set

```
A=((1+t)^2-r^2)^2, B=((1-t)^2-r^2)^2
h=(A+B)/16, K=AB+(A^2+B^2)/20, q=K/128.
```

Then h(x)=P(x comparable with X), and q(x)=P({x,X,Y} forms a chain). The three disjoint roles of x contribute B²/2560 (earliest), AB/128 (middle) and A²/2560 (latest). Flat uniform integration over the diamond reduces even monomials to E[t^i r^j]=12 i!(j+2)!/(i+j+4)! for i,j even. Exact rational evaluation gives

| Moment | Exact |
|---|---:|
| E[h] | 1/10 |
| E[h²] | 1/50 |
| E[q] | 1/350 |
| E[hq] | 1/1400 |
| E[q²] | 29/970200 |
| Var(h) | 1/100 |
| Cov(h,q) | 3/7000 |
| Var(q) | 527/24255000 |

### Exact subset-overlap counting

Index disjointness gives independence. When two pairs share one index, their kernel covariance equals Var(h); identical pairs give p2(1-p2). When a pair and triple share one index, covariance equals Cov(h,q); when the pair is contained in the triple, the triple-chain event implies pair comparability and the covariance equals p3-p2p3. The resulting exact coefficients are

```
Var(U2) = [2(N-2)/C(N,2)] Var(h)
        + [1/C(N,2)] p2(1-p2).

Cov(U2,U3) = [2 C(N-2,2)/C(N,3)] Cov(h,q)
           + [(N-2)/C(N,3)] (p3-p2p3).
```

For two 3-chain subsets, overlaps of size 1, 2 and 3 contribute

```
Var(U3) = [3 C(N-3,2)/C(N,3)] Var(q)
        + [3(N-3)/C(N,3)] (gamma2-p3^2)
        + [1/C(N,3)] p3(1-p3),
```

where gamma2 is the joint probability that (X,Y,Z) and (X,Y,W) both form chains for four iid events. It is **not** approximated by independent triples.

### Closing the four-event overlap integral exactly

Define F(x,y)=P({x,y,Z} is a chain). For x≺y, it is the sum of normalized volumes of past(x), interval(x,y) and future(y); F=0 for incomparable x,y. Thus gamma2=E[F(X,Y)²].

Let C(x,y)=V(I(x,y))/V(D)=[(Δt)²-|Δspatial|²]²/16 for x≺y, and define ordered interval-volume moments

```
I_m = E[1_{X≺Y} C(X,Y)^m].
```

**Exact lemma (m=0,1,2):**

```
I_0=1/20,  I_1=1/2100,  I_2=1/35280.
```

Proof by direct integration: introduce radial null coordinates a=t+r, b=t-r for X and c=s+R, d=s-R for Y. Each point satisfies -1≤b≤a≤1 (respectively -1≤d≤c≤1). Integrating the relative spatial angle μ analytically gives the difference of positive-part powers

```
[(c-a)(d-b)]_+^(2m+1) - [(d-a)(c-b)]_+^(2m+1).
```

With the correctly normalized angular/radial Jacobians, this reduces I_m to the prefactor 9/[16(2m+1)16^m] times two polynomial integrals over 0≤u,v,w, u+v+w≤2:

```
S1 = ∫ (2-u-v-w) uw
        [(v+w)^(2m+1)(u+v)^(2m+1)
          - v^(2m+1)(u+v+w)^(2m+1)] du dv dw,

S2 = ∫ (2-u-v-w) (u+v)(v+w)(uw)^(2m+1) du dv dw.
```

Here S1 comes from b<a<d<c, S2 from b<d<a<c. Expand the polynomials exactly and apply the Dirichlet simplex integral

```
∫_{u+v+w≤2} (2-u-v-w) u^i v^j w^k du dv dw
 = i!j!k! 2^(i+j+k+4)/(i+j+k+4)!.
```

This yields the three exact I_m values above, independently checking I0=p2/2 and I1=p3/6.

A fixed specified ordering of four iid events occurs with probability P4/24 when they form a chain. Conditioning on outer endpoints and requiring the two inner points in their interval to be comparable gives P4=24*(p2/2)*I2=1/29400. Independent radial rational integration gives E[A²B]=E[AB²]=256/2205. Expanding F(X,Y)² into the past², future², interval² and six cross-role terms now gives

```
gamma2 = E[A²B]/1024 + 2 I2 + P4/2
       = 1/8820 + 1/17640 + 1/58800
       = 11/58800.

gamma2 - p3² = 263/1470000.
```

Substitution into the size-1/2/3 overlap formula simplifies to the asserted closed finite-N Var(U3). The equality is valid for all integer N≥3 and does not depend on a numerical sampling fit.

## Parameter reconstruction uncertainty

The inverse-function checkpoint has Jacobian

```
J = [[1/25, 0],[9/3500,16/165375]], det(J)=16/4134375>0.
```

The *leading* covariance (bounded-kernel U-statistic central limit theorem) is

```
Cov((U2,U3)) = Sigma/N + O(N^-2),
Sigma = [[1/25,9/3500],[9/3500,527/2695000]].

J^(-1) Sigma J^(-T) = [[25,0],[0,145563075/45056]].
```

Consequently the local delta-method standard deviations are asymptotically about 5/sqrt(N) and 56.839375/sqrt(N); leading parameter errors are uncorrelated. **This is asymptotic**, not a nonasymptotic parameter confidence interval or a certified radius of invertibility. The exact covariance of observables above does not on its own imply an exact finite-N covariance of nonlinear parameter estimators.

## Reproducible verification and evidence tier

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -B tools/verifier/finite_chain_covariance_4d.py
```

The standard-library verifier performs exact Fraction-based polynomial integration for one-point moments, exact simplex integral certificates I0/I1/I2, P4 and gamma2, exact formula checks for N=3..17, and an independent exhaustive discrete-sample overlap oracle on N=3,4,5 (up to 3^5 sample tuples). It rejects optimized Python and runs in a dedicated short CI job. The discrete oracle checks overlap *counting*, not the continuum geometry; the simplex integrator independently verifies that geometric step. Additional independent numerical sampling (~2 million pairs per seed) agreed with gamma2 within sampling uncertainty, but is **not a proof**. No Mac or Lean run is claimed.

**OPEN:** Nonasymptotic reconstruction confidence bounds with a quantitatively controlled inverse neighborhood, robust estimates under an unknown conformal family, dimension reconstruction, spacetime emergence, curvature dynamics and Einstein equations. This calculation closes the stated fixed-N covariance problem at the flat baseline only.
