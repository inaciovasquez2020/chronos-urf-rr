# Finite covariant causal-growth calculation — 2026-11-10

Repository audit target: `inaciovasquez2020/chronos-urf-rr`, PR #1347 HEAD `abef2b3e61dcb24a3ebb65ad0df7a76f63d4869f`.
Repository unchanged; Mac/Lean NOT_RUN.

## General finite-horizon parameterization

Let `L_5` be the set of 357 naturally labeled five-element posets; they form 63 unlabeled isomorphism classes. Choose any probability distribution `q` on the 63 classes. For `U`, let `l(U)` be the number of distinct naturally labeled representatives of that class. Give each representative terminal probability `q(U)/l(U)`. For a naturally labeled prefix `C` of size `n<=5`, put `M_n(C)` equal to the sum of these terminal probabilities over all five-element extensions with prefix `C`. For every nonzero-mass parent, set `w_n(C,P)=M_{n+1}(C+_P x)/M_n(C)` for each down-set `P` of `C`.

Then `w` is a normalized precursor-Markov kernel, its unlabeled-history probabilities are invariant under natural-labeling swaps (covariance-square equalities), and prefix restrictions of the five-element law reproduce every earlier law. Conversely, every normalized finite-horizon precursor-Markov law satisfying equality of natural-labeling history probabilities has a unique terminal distribution on the 63 unlabeled classes, and agrees with this construction on positive-mass states. The resulting finite solution space is the 62-simplex. **This is only projectivity across sizes 0..5; no compatible infinite extension is established.**

## Exact explicit witness

Terminal five-element poset | Class probability | naturally labeled representatives
---|---:|---:
Empty order | 11/70 | 1
One two-element chain, three isolated points | 5/7 | 10
One three-element chain, two isolated points | 1/35 | 10
Two disjoint two-element chains, one isolated point | 1/10 | 15
Every other class | 0 | 321 labeled representatives combined

The five-element expectations of sample-subset densities are exactly

- Comparable pair `E[P2]=1/10`.
- Three-chain `E[P3]=1/350`.
- Induced 2+2 `E[U_2+2]=1/50`.

The first two are imposed by design, not predicted by an independently motivated dynamics. The positive 2+2 moment holds **only at five events**; it is not a limiting statement.

The full-support Bell-causality-style ratio test has a nonzero transition witness: for the two-element antichain parent, precursor sets `P=empty` and `Q={0}` have weights `247/315` and `34/315`, respectively. In the reduced one-element spectator-free parent, the corresponding weights are `9/10` and `1/10`. The cross difference is `-59/3150`, so spectator independence fails. Thus this candidate is outside the Bell-causal subclass of classical sequential growth. This is **not** a demonstration of new physics.

## Reproducibility

`chronos_finite_covariant_growth_audit.py` uses standard-library `fractions.Fraction`. Exhaustively converts all 1024 forward-edge configurations on 5 elements to 357 transitive orders, enumerates 63 isomorphism classes, checks 36 supported labeled terminal states and their marginal laws, verifies all 218 tested reachable covariance squares and computes the nonzero Bell-causality witness. Executed in analysis container, not on Mac.

## Formal verification boundary

Pinned repository `lean-toolchain`: `leanprover/lean4:v4.29.0`. Direct GitHub tree at exact PR HEAD inspected; no source mutation. No Lean binary in analysis container. Suggested Lean declarations: finite precursor ideal; natural labeled poset; terminal mass; prefix-mass marginal; normalized kernel on positive-mass states; two-step square identity; telescope of history probability; finite-projectivity; explicit 5-event rational certificate. No Lean file is claimed compiled. Build and axiom audit needed on the Mac before branch/push.

Overall emergence and gravitational dynamics remain OPEN.