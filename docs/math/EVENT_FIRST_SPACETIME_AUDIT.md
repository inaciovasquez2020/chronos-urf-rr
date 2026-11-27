# Event-first spacetime: exact causal-order benchmarks and finite identifiability obstruction

**Status (2026-11-10):** exact symbolic calculations and bounded finite-poset enumeration **COMPUTATION_PASS**; elementary poset statements **PROVED (paper)**; Lean **NOT_RUN**; intrinsic four-dimensional continuum limit, gravitational field equations, and fifth physical dimension **OPEN**.

## Scope

These receipts audit geometric observables on an *assumed* 4D Minkowski diamond and prove a limitation of global chain-count reconstruction. They do **not** derive spacetime, infer a unique geometry from finite data, prove a Lorentzian continuum limit, or supply a gravitational action.

## 4D flat causal diamond

Use signature (-+++), speed of light 1, and endpoints p=(-1,0,0,0), q=(1,0,0,0). Let D=I(p,q), r=|x|, A=(1+t)^2-r^2, B=(1-t)^2-r^2. Spatial sections have radius 1-|t|, so

- V(D)=2*pi/3; for endpoint proper-time separation tau, V_4(tau)=pi*tau^4/24.
- For independent uniformly volume-sampled X,Y in D, P(X<Y)=1/20, so P(X,Y comparable)=1/10.
- For three independent events, P(X<Y<Z)=1/2100 for a specified ordering; P(the three form a total chain in any ordering)=1/350.
- Consequently E[C_2]=binomial(n,2)/10 and E[C_3]=binomial(n,3)/350 for an independent n-point sprinkling. Chains are counted as **unoriented subsets** whose inherited order is total; do not multiply E[C_2] by an extra factor of 2.

The chain integral uses V(p,y)=pi*A^2/24 and V(y,q)=pi*B^2/24. Exact arithmetic, rather than a floating-point Monte Carlo approximation, checks all coefficients.

## Conformal perturbation

Take h=(A^2+B^2)/16, g_eps=c_eps(1+eps*h)g_0, and c_eps=(1+eps/5+eps^2/50)^(-1/2). This scalar prefactor preserves the *total 4-volume* of D because in dimension four the volume form multiplies by [c_eps(1+eps*h)]^2. Require the conformal factor positive.

Under the normalized volume-sampling law,

- E_0[h]=1/10; Var_0(h)=1/100.
- d/d eps P_eps(X,Y comparable)|_0 = 1/25.
- d/d eps R_{g_eps}(0)|_0 = 9, with R=-6 exp(-2phi)(box phi + |grad phi|^2), g=exp(2phi)g_0, box=-partial_t^2+Delta.

These values are **restricted-family** identities. They are not an intrinsic universal curvature estimator.

A separate 2D conformal counterexample is g_A=-dt^2+dx^2 and g_B=(1+eps*x)g_A on a symmetric diamond where 1+eps*x>0. They have identical order and equal total volume but different local scalar curvature: R_A=0, R_B=eps^2/(1+eps*x)^3 under the stated convention. Thus causal order plus a *single total volume* does not determine pointwise curvature.

## Finite causal-order theorem

For antichains of positive sizes a_1,...,a_m, let P=A_1 ⊕ ... ⊕ A_m be their ordinal sum. Every chain chooses zero or one vertex from each antichain. Hence the exact chain polynomial is

    1 + sum_{k>=1} C_k(P) z^k = product_i (1+a_i z).

Permuting the block sizes preserves **all** global chain counts but need not preserve the poset's isomorphism type. Explicitly, orders with block sizes (1,1,2) and (1,2,1) share (C_1,C_2,C_3,C_4)=(4,5,2,0), while the first has two maximal elements and the second has one. Their multisets of interior sizes |{z:x<z<y}| over comparable pairs are respectively (0,0,0,1,1) and (0,0,0,0,2). Therefore global chain counts alone cannot distinguish finite causal orders. The result is elementary and **novelty is not established**.

The scripts independently compare dynamic-programming chain counts with direct subset enumeration, canonicalize under all permutations, and enumerate 16 nonisomorphic orders on 4 events and 63 on 5 events. Exhaustive finite checks do not prove asymptotic geometry.

## Minimal intrinsic growth control

In transitive-percolation sequential growth, a new maximal element selects each existing element independently with probability p and transitive closure supplies the rest. At n=2, pair comparability has probability p. At n=3, a total chain requires two successive direct edges, and has probability p^2. Matching the Minkowski two-point probability requires p=1/10, giving three-chain probability 1/100 rather than 1/350. This excludes exact agreement of the **two- and three-point finite distributions with one constant p**; it does not exclude all asymptotic continuum limits, and sequential growth is established prior work, not claimed novel here.

## Reproduce

From the repository root, in a Python environment with SymPy installed:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 tools/verifier/event_first_exact_audit.py
PYTHONDONTWRITEBYTECODE=1 python3 tools/verifier/event_first_poset_n4.py
PYTHONDONTWRITEBYTECODE=1 python3 tools/verifier/event_first_poset_n5.py
```

Expected markers: `EXACT_AUDIT = PASS`; `THREE_EVENT_GROWTH_MISMATCH = PASS`; two `WITNESS_VERIFIED := PASS` lines. The poset verifier scripts use only the Python standard library. A nonzero exit or unobserved marker is not a PASS.

## Open boundary

The missing result is an intrinsic, label-invariant growth law with a **specified probability topology and scaling** that converges to a manifoldlike four-dimensional causal structure and supports consistent local volume and curvature reconstruction. Convergence of selected chain moments is insufficient for metric convergence. Deriving Einstein dynamics additionally requires a justified variational or equivalent dynamical law, not merely a curvature statistic.

**Repository promotion:** Documentation and bounded audit only. No claim of a kernel proof, physical fifth coordinate, Einstein dynamics, or independent mathematical review. Treat CI and subsequent review as separate gates.

## References for comparison (not certificates)

- D. P. Rideout and R. D. Sorkin, *A classical sequential growth dynamics for causal sets*, Phys. Rev. D 61, 024002 (2000).
- D. M. T. Benincasa and F. Dowker, *The scalar curvature of a causal set*, Phys. Rev. Lett. 104, 181301 (2010).
