# Fixed-N covariance of 4D causal-chain statistics (2026-11-12)

**RESULT: PROVED (elementary overlap formula and exact rational flat-diamond moments); COMPUTATION_PASS (independent bounded exact oracle).** The exact finite-N variance of three-chain counts is **OPEN**, with one explicit missing four-point overlap integral. No Lean, Mac, gravitational dynamics, fifth dimension or emergent-spacetime proof is claimed. Novelty NOT ESTABLISHED.

## Sampling model and notation

Use the 4D Minkowski diamond, volume measure and two-parameter conformal family fixed in [the local-identifiability checkpoint](../status/CAUSAL_CHAIN_LOCAL_IDENTIFIABILITY_2026_11_10.md). Condition on **exactly N>=3 independent volume-uniform points**; this is not an unconditioned Poisson process. Define unbiased U-statistics U2 and U3 as the fractions of unordered index pairs and triples whose induced causal orders are chains. Baseline p2=1/10 and p3=1/350.

For a point x=(t,spatial x) of radial coordinate r, put

```
A=((1+t)^2-r^2)^2,  B=((1-t)^2-r^2)^2
h=(A+B)/16,  K=AB+(A^2+B^2)/20, q=K/128.
```

**PROVED:** h(x)=P(X comparable to x), q(x)=P((x,X,Y) form a 3-chain). For q, the specified x can be the earliest, middle or latest event; the three disjoint contributions are B²/2560, AB/128, and A²/2560. In particular E h=p2 and E q=p3.

Exact diamond integration reduces every even monomial to

```
E[t^i r^j] = 12 i! (j+2)! / (i+j+4)!,  i,j even.
```

For fixed even nonnegative i,j this follows directly by the normalized measure 12 r² dr dt on 0≤t≤1 and 0≤r≤1-t. Independent integer/rational polynomial expansion gives:

| Moment | Exact |
|---|---:|
| E[h²] | 1/50 |
| E[hq] | 1/1400 |
| E[q²] | 29/970200 |
| Var(h) | 1/100 |
| Cov(h,q) | 3/7000 |
| Var(q) | 527/24255000 |

## Exact finite-N covariance: solved entries and one open integral

Count pairs of sample-index subsets by intersection cardinality; disjoint index subsets are independent. For any integer N≥3,

```
Var(U2)    = (2N+5) / (50 N(N-1))
Cov(U2,U3) = 9(N+3) / (3500 N(N-1))
```

The shared-one pair–triple covariance is Cov(h,q)=3/7000. When a pair is contained in a triple, that triple being a chain forces its pair to be comparable, and the covariance is p3-p2*p3=9/3500. Weight these by 2*C(N-2,2)/C(N,3) and (N-2)/C(N,3). The pair–pair shared-one covariance is Var(h)=1/100, with diagonal variance p2(1-p2).

The remaining diagonal is exactly

```
Var(U3) = 3*C(N-3,2)/C(N,3) * (527/24255000)
        + 3*(N-3)/C(N,3) * (gamma2 - 1/350^2)
        + 1/C(N,3) * (1/350)*(349/350).
```

Define gamma2 = E[H3(X,Y,Z)H3(X,Y,W)] for four iid continuous points. Equivalently gamma2=E[F(X,Y)^2], with F(x,y)=P((x,y,Z) is a 3-chain). For causally ordered x≺y, writing spatial positions as bold x and bold y,

```
F(x,y) = [ A(x) + B(y) + ((t_y-t_x)^2 - |bold y-bold x|^2)^2 ] / 16;
```

otherwise reverse roles for y≺x, or set F=0 if incomparable. The three terms are the normalized past of x, interval between x and y, and future of y. This explicit 8D geometric integral is the **weakest remaining obstacle** to fully numeric exact fixed-N covariance; its value is NOT claimed. Because E[F]=p3, P(F>0)≤p2 and 0≤F≤1, Cauchy–Schwarz and bounding give 1/12250 ≤ gamma2 ≤ 1/350. The bounds are intentionally coarse.

## Leading large-N covariance and local parameter uncertainty

The bounded-kernel U-statistic central limit theorem and first-point overlap contributions imply

```
Cov((U2,U3)) = Sigma/N + O(N^-2)
Sigma = [[1/25, 9/3500], [9/3500, 527/2695000]].
```

With the already verified local response Jacobian from the prior checkpoint,

```
J = [[1/25,0],[9/3500,16/165375]], det J=16/4134375
J^(-1) Sigma J^(-T) = [[25,0],[0,145563075/45056]].
```

By the delta method, **asymptotic** parameter standard deviations are approximately 5/sqrt(N) for a and 56.839375/sqrt(N) for b. Leading errors are uncorrelated but b is much more weakly identifiable. No nonasymptotic confidence region or guaranteed inversion radius follows from this calculation.

## Reproduction and exact scope of automated tests

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -B tools/verifier/finite_chain_covariance_4d.py
```

The verifier uses standard-library Fraction polynomial integration (no floating point), checks exact moments and inverse covariance, exact finite-N pair entries for N=3,...,17, and separately checks overlap coefficients by exhaustive enumeration of iid draws with replacement from a three-atom chain for N=3,4,5 (maximum 3^5 sample tuples). These discrete tests independently audit *combinatorial coefficients*, **not** the continuous 4D integral gamma2. Optimized Python cannot falsely PASS.

**OPEN:** independent exact evaluation of gamma2; finite-N parameter confidence bounds with controlled nonlinear inversion; manifoldlikeness, intrinsic 4D emergence, Einstein dynamics and any fifth physical dimension. All preexisting scientific status boundaries remain unchanged.
