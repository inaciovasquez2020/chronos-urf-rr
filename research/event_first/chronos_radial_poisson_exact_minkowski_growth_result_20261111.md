# Exact Minkowski marginal laws from radial Poisson natural growth

Date: 2026-11-11. Status: PROVED (self-contained mathematical derivation); COMPUTATION_PASS (bounded Monte Carlo); Lean NOT_RUN; independent review and novelty NOT_ESTABLISHED. **Intrinsic, label-order invariant and background-free emergence: OPEN/NOT_ESTABLISHED.**

## Theorem: exact fresh Minkowski laws at every birth stage

Fix a point p=0, a future unit timelike vector e in 4D Minkowski space, and intensity λ>0. Sprinkle a homogeneous Poisson point process of intensity λ throughout the chronological future cone C=I⁺(p). Define for each point z=(t,spatial vector) in the rest frame of e

  h_e(z)=t+|spatial vector|.

For T>0, the sublevel D_T={z∈C:h_e(z)<T} is precisely the Alexandrov interval I(p,p+Te), and Vol(D_T)=κT⁴ with κ=π/24.

The number of Poisson points in each D_T is almost surely finite and tends to infinity as T→∞. Almost surely all heights are distinct. Enumerate events by increasing h_e as Z_1,Z_2,... . Each prefix {Z_1,...,Z_n} is a causal order ideal, because y≺z implies h_e(y)<h_e(z). Each event has finitely many causal predecessors (all lie in a finite-volume D_T). Therefore this is a **past-finite natural growth process**.

Let Q_n^(4) be the unlabeled order-type law of n independent four-volume-uniform points in the unit 4D Minkowski diamond I((0,0),(1,0)).

**Exact law:** For EVERY integer n>=1, the unlabeled poset induced by the first n births satisfies

    Law(P_n) = Q_n^(4).

In particular, uniform samples of k points from P_n have marginal law Q_k^(4) for every 1<=k<=n, not just asymptotically.

### Proof of exact law

In radial null coordinates u=t+r, w=t-r, the normalized 4D volume law in D_T is

  (12/T⁴)(u-w)² du dw, 0<w<u<T.

Set v=w/u. The joint density factors into

  f_u(u)=4u³/T⁴, 0<u<T;
  f_v(v)=3(1-v)², 0<v<1,

with independent uniform angular direction on S². A homogeneous Poisson process on C therefore has height-coordinate intensity 4λκu³du, i.e., transformed arrival times S_n=λκ h_e(Z_n)⁴ are the successive arrivals of a rate-one homogeneous Poisson process. Each arrival has independent mark (v,angular direction) with the distributions above.

Conditional on its n-th arrival height h_e(Z_n)=T, the previous n−1 points are iid volume-uniform in D_T and the n-th mark follows the boundary u=T law f_v(v)=3(1-v)², independently. If instead n iid points are drawn uniformly from D_1, condition on their maximal height M; given M, their n−1 other points are iid uniform in D_M, and the maximizing point has exactly the same boundary mark distribution. Dilation of all points by 1/M leaves causal order unchanged. Thus the induced unlabeled order of a fixed-volume iid n-sample has the same law as the first n Poisson arrivals. This proves Law(P_n)=Q_n^(4).

### Almost-sure convergence of all fixed-k profile statistics

For each unlabeled k-event order type H, write F_{n,k}(H)= (# k-subsets of P_n inducing H)/binom(n,k). From exact stage-law equality, F_{n,k}(H) has the same distribution as the bounded U-statistic of n iid points in D_1, with mean Q_k^(4)(H).

Changing one point changes at most binom(n-1,k-1) of the binom(n,k) subsets, so the bounded differences constant is k/n. McDiarmid yields

  Pr(|F_{n,k}(H)-Q_k^(4)(H)|>ε) <= 2 exp(-2ε²n/k²).

The tail is summable over n. Borel–Cantelli implies, for each fixed (k,H), almost-sure convergence to Q_k^(4)(H). Since the collection of (k,H) is countable, all these limits hold simultaneously almost surely.

This is exact intrinsic *sampling-statistic* agreement with Minkowski, arising from a process using Minkowski geometry as input, NOT a deduction of spacetime geometry from event axioms.

## Delimitation: why this does not contradict earlier nonprojectivity

The radial-Poisson birth order is NOT order-invariant (not a uniform linear extension conditional on the realized unlabeled P_n). Indeed:

- Since P_2~Q_2, Pr(Z_1≺Z_2)=1/10.
- Since P_3~Q_3, a *uniformly random* linear extension of P_3 would have its first two births comparable with probability 16/175.
- If the radial birth process were order-invariant, these two probabilities would coincide; they do not (difference 3/350).

Thus the exact all-stage Q_n laws are compatible with **a non-order-invariant natural growth**, but incompatible with an order-invariant one. The prior order-invariant no-go remains valid.

## Covariance, preferred frame, and lack of independent emergence

The Poisson sprinkling on C is Lorentz-invariant as an unmarked point process. The construction of height h_e(z) **uses a chosen future unit timelike vector e** (equivalently a worldline through p), which is external and not recovered intrinsically from causal order. The distribution of *unlabeled order-valued histories* is independent of which fixed e is chosen: Lorentz transformations sending e to e' preserve the intensity and causal relation. But an **embedded** labeled history and the rule for choosing the next event still require e.

Consequently:
- Background spacetime is GIVEN, not emergent.
- No frame-free intrinsic growth rule has been supplied.
- Discrete general covariance / order-invariance is REFUTED for this specific rule.
- The geometry of selected labels is not Lorentz invariant for a fixed e, even though unlabeled histories have e-independent laws.
- This does not construct gravitational field equations.

Bombelli–Henson–Sorkin, *Discreteness without symmetry breaking: a theorem*, arXiv:gr-qc/0605006, proves no equivariant measurable selection of a spacetime direction from a Minkowski sprinkling; this underlines why an externally supplied e is a substantive limitation, not a harmless coordinate convention. Brightwell–Łuczak, *Order-invariant measures on causal sets*, Ann. Appl. Probab. 21 (2011), DOI 10.1214/10-AAP736, supplies the distinct order-invariance framework.

## Bounded executable regression

Companion chronos_radial_poisson_growth_20261111.py (Python stdlib only): seed 20261111; 120000 independent three-birth Poisson trials; actual natural-growth causal checks; five three-event unlabeled-type frequencies compared with exact Q_3 rational probabilities; first-two comparability compared with Q_2=1/10; all PASS. The regression is numerical corroboration, not the proof. Script SHA256 d462e6b767170560358aa4240e594bc93f697422ec35d87a0d9642c740bbf5ad; Git blob 8c372cc8e280782074056986479f1340464d8579.

## Research status and next obstruction

EXACT_PAST_FINITE_NATURAL_GROWTH_WITH_Qn := PROVED.
ALL_FIXED_k_SUBSET_PROFILE_LIMITS := PROVED_A_S.
PREFERRED_FRAME_ASSUMPTION := PRESENT.
ORDER_INVARIANCE := REFUTED.
INTRINSIC_COVARIANT_GROWTH := OPEN.
EMERGENT_SPACETIME_AND_GRAVITATIONAL_DYNAMICS := OPEN.
LEAN_VERIFIED := NOT_RUN.
NOVELTY_AND_INDEPENDENT_REVIEW := NOT_ESTABLISHED.

The strongest next objective is to replace the external timelike vector / radial height by an **intrinsically defined, Lorentz-compatible natural-growth mechanism** while retaining the uniform-subset Minkowski laws. This example settles a different existence question and is a diagnostic benchmark, not the original full research target.

Branch research/event-first-audit-staging-20261111 only. No merge and no change to PR #1347.
