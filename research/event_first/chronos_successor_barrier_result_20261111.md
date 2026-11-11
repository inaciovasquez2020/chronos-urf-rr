# Chronos–URF–RR: successor-rank barrier theorem and exact audit

Date: 2026-11-11. **Finite-poset theorem: PROVED.** Local finite tests: COMPUTATION_PASS. Four-dimensional selection-weight asymptotics: **OPEN**. Lean: NOT_RUN. Independent novelty: NOT_ESTABLISHED.

## Exact barrier representation

Let P be finite, x minimal, Q=P\{x}, U={y:x<y} (an upper set of Q), A=Q\U (a lower set), a=|A| and u=|U|>0. Fix any internal linear extensions α=(a_1,...,a_a) of A and β=(b_1,...,b_u) of U. Put

  c_j = max({i: a_i < b_l for some l<=j} ∪ {0}) (1<=j<=u).

Equivalently c_j is the running maximum position in α of all external A-predecessors of the first j members of β. Then 0<=c_1<=...<=c_u<=a.

An interleaving of α and β is a linear extension of Q exactly when, immediately before placing β_j, at least c_j letters from α have appeared. Equivalently, the interleavings are lattice paths (i,j) from (0,0) to (a,u), with a U step from (i,j) allowed iff i>=c_{j+1}.

Let W(i,j) count completions from state (i,j), with W(a,u)=1 and

  W(i,j)=[i<a]W(i+1,j)+[j<u and i>=c_{j+1}]W(i,j+1).

For u>0, the number of valid shuffles whose first U event appears in position d+1 is exactly W(d,1), c_1<=d<=a. Thus

  Pr(B_x=d+1 | α,β) = W(d,1) / Σ_{h=c_1}^a W(h,1).

Averaging with **weights proportional to the number of valid interleavings for the internal-order pair** (not uniformly over internal-order pairs) gives the unconditional first-successor rank law under a uniformly chosen extension of Q. Then

  Pr_P(x first)=1/E[B_x].

The barrier vector retains *all* A→U causal precedence information given α,β. It is an exact structural reduction, not an asymptotic geometric estimate.

## New geometry-sensitive lower bound for the successor penalty

Let M(U) be the set of minimal elements in the induced order on U. Define

  r_x = min_{y∈M(U)} |Past_Q(y) ∩ A|,

with r_x=0 if U is empty. For u>0, every first U event in an internal U extension belongs to M(U), so the first-U barrier c_1 is at least r_x for *every* internal A/U extension pair.

By the positive association of uniform unconstrained binary interleavings conditioned on monotone precedence barriers, the first-U survival distribution dominates the hypergeometric free-shuffle survival. Also the first r_x survival probabilities equal 1. Consequently

  Δ_x = E[B_x] - N/(u+1)
      >= Σ_{j=1}^{r_x} [1 - C(a,j)/C(N-1,j)] >= 0,

where N=|P|=a+u+1.

Thus

  Pr_P(x first)
    <= [ N/(u+1) + Σ_{j=1}^{r_x}(1-C(a,j)/C(N-1,j)) ]^{-1}.

For r_x>=1 this improves the existing successor-count upper bound. The result applies to any finite poset and therefore also to each realized four-dimensional sprinkling. It does not determine the distribution of r_x in the large-N geometry.

## Exact validation

- `chronos_barrier_rank_audit_20261111.py`: 2,121 independently compared minimal-event instances from every forward-edge configuration up to five vertices, with transitively closed orders. Each barrier-DP distribution matches full brute-force extension enumeration of Q. 1,149 cases have Δ_x>0. The new r_x lower bound passed in all instances.
- `chronos_barrier_minkowski_probe_20261111.py`: separate fixed-seed (20261111) 4D sprinkling test. Exact integer linear-extension DP conditional on each floating-coordinate sprinkled poset. The sampling procedure is volume-uniform, using radial spatial density ∝r².

| N | Independent sprinklings | Minimal candidates | r_x>0 fraction | Mean Δ_x | Mean lower bound | Max DP states |
|---|---:|---:|---:|---:|---:|---:|
| 8 | 100 | 615 | 0.15935 | 0.31670 | 0.09075 | 256 |
| 12 | 80 | 682 | 0.24047 | 0.79090 | 0.14082 | 4,096 |
| 16 | 50 | 527 | 0.25427 | 1.22294 | 0.21195 | 65,536 |

Candidate-weighted means are **not** birth-probability-weighted expectations. Finite observations do not imply any N→∞ behavior. The bound is nontrivial but weak in these tested instances.

## Genuine open boundary

Obtain a quantitative asymptotic law for barrier vectors c_j or their size-biased completion weights W, conditioned on a minimal x at geometric location (u,w) in an N-event 4D Minkowski sprinkling. The low-order statistic r_x alone misses much of Δ_x at the tested scales. No limit for the first-birth density, no uniform-tail Minkowski-profile theorem, and no gravitational dynamics have been proved.

Related established frameworks: Brightwell–Łuczak, *Order-Invariant Measures on Fixed Causal Sets* (2012); and the lattice-path formulation of width-two linear extensions in standard linear-extension surveys. No claim of research priority.