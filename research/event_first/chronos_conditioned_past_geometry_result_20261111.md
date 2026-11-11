# Conditional ancestral geometry of shallow-past events

Date 2026-11-11. Scope: fixed-N conditional law in 4D Minkowski Alexandrov intervals. PROVED analytically; bounded independent numeric validation PASS. Lean NOT_RUN; independent novelty NOT_ESTABLISHED. Linear-extension selection and Minkowski prefix limit OPEN.

## Theorem 1: exact conditional predecessor law

Let P_N be the causal order induced by N independent uniform four-volume points in a 4D Minkowski Alexandrov interval D=I(p,q). Fix a distinguished event Z=z, and let D_N(z) be the number of other sampled events in I(p,z). For 0<=j<=N-1, conditional on Z=z and D_N(z)=j, the j predecessors are independent volume-uniform random points of I(p,z); the remaining N-1-j points are independent uniform points of D\I(p,z), independently of those predecessors (up to an arbitrary ordering of iid labels).

Proof: conditional independent sampling under a fixed multinomial count partitions the iid observations into conditionally independent samples from the cells. Minkowski dilation and Lorentz covariance identify I(p,z) with a rescaled standard 4D interval. Hence, for every unlabeled j-event poset type H,

Pr(induced order on predecessors = H | Z=z,D_N(z)=j) = Q_j^(4)(H),

independent of z and N. Example: for j=2, comparability probability is 1/10. More generally the expected number of j-predecessor events whose ancestor suborder has type H equals E[# {z:D_N(z)=j}] Q_j^(4)(H), exactly for every N.

This law is conditional on predecessor COUNT, not on being selected into an early prefix by a uniform random linear extension. The latter reweights entire configurations and remains OPEN.

## Theorem 2: exact null-coordinate ratio of one predecessor

For j=1, let X be the unique predecessor of Z=z. Take the null coordinate u=t+x_parallel, with x_parallel aligned with the spatial vector z-p, and define H=[u(X)-u(p)]/[u(z)-u(p)]. Then

H ~ Beta(2,2): density 6h(1-h), 0<h<1;
E[H]=1/2; E[H²]=3/10; CDF=3h²-2h³.

Proof: Lorentz boost and common scaling map I(p,z) to I((0,0),(1,0)) and leave the normalized aligned null-coordinate ratio invariant. Write v=t-x_parallel and rho²=y²+z². Standard interval constraints are 0<=u,v<=1 and rho²<=min(uv,(1-u)(1-v)). Integrate the transverse 2-disc and the coordinate v. The section integral is
int_0^1 min(uv,(1-u)(1-v)) dv = u(1-u)/2.
The normalized u-density is therefore 6u(1-u).

As the interval endpoint z approaches the past null cone, v(z)->0. Every point X in I(p,z) has 0<=v(X)<=v(z) and transverse displacement squared <= u(z)v(z); hence X approaches the same null generator. The nondegenerate fraction H remains Beta(2,2).

## Bounded reproducible check

The companion Python file chronos_conditioned_past_geometry_20261111.py uses seed 20261111 and 120,000 independent pairs. Its exact rational section identity PASS; empirical H mean 0.499783 (target 1/2), second moment 0.2999023 (target 3/10); CDF at 0.1/0.25/0.5: 0.02745/0.156275/0.5008833 vs 0.028/0.15625/0.5; causal comparability 0.0987167 vs 0.1. PASS to predefined tolerances. This is evidence, not proof.

## Precise OPEN boundary

These are laws of geometrically conditioned ancestors, NOT linear-extension-weighted selected events. To determine the first birth law and the iterated Minkowski sampling limit, control the whole-poset completion weights (equivalently the successor-barrier distribution) after conditioning on the shallow-past marked geometry. Neither the exact ancestor law nor the Beta null ratio is enough.

Repo staging only; no Mac build, no Lean formalization, no independent review, no merge.