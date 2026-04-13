# Kairos 2D Navier--Stokes Stabilization

Status: supporting-instance
Scope: non-frontier
Role: certified strong test of the Kairos stabilization tool; not a flagship closure claim.

## Problem
Prove global existence, uniqueness, and exponential stabilization for the Kairos-controlled incompressible Navier--Stokes system on the 2D torus.

\[
\partial_t u+(u\cdot\nabla)u+\nabla p=\nu \Delta u-\lambda \mathbb P u,
\qquad
\nabla\cdot u=0,
\qquad
u(0)=u_0,
\]
with
\[
\nu>0,\qquad \lambda>0,\qquad u_0\in H^1_\sigma(\mathbb T^2).
\]

## Kairos instance
\[
\Phi(u)=\frac12\|u\|_{L^2}^2,
\qquad
\mathcal K(u)=-\lambda \mathbb P u.
\]

## Closed theorem
For every
\[
u_0\in H^1_\sigma(\mathbb T^2),
\]
there exists a unique global solution
\[
u\in C([0,\infty);H^1_\sigma)\cap L^2_{\mathrm{loc}}([0,\infty);H^2_\sigma),
\]
and
\[
\|u(t)\|_{L^2}^2\le e^{-2\lambda t}\|u_0\|_{L^2}^2
\qquad
\forall t\ge 0.
\]

Moreover,
\[
\|\nabla u(t)\|_{L^2}^2\le e^{-2\lambda t}\|\nabla u_0\|_{L^2}^2
\qquad
\forall t\ge 0.
\]

## Proof skeleton
1. \(L^2\)-energy:
\[
\frac12\frac{d}{dt}\|u\|_{L^2}^2+\nu\|\nabla u\|_{L^2}^2+\lambda\|u\|_{L^2}^2=0.
\]

2. Vorticity equation in 2D:
\[
\omega=\partial_1u_2-\partial_2u_1,\qquad
\partial_t\omega+u\cdot\nabla\omega=\nu\Delta\omega-\lambda\omega.
\]

3. Vorticity energy:
\[
\frac12\frac{d}{dt}\|\omega\|_{L^2}^2+\nu\|\nabla\omega\|_{L^2}^2+\lambda\|\omega\|_{L^2}^2=0.
\]

4. On \(\mathbb T^2\), divergence-free equivalence gives
\[
\|\nabla u\|_{L^2}\simeq\|\omega\|_{L^2},
\]
hence exponential \(H^1\)-decay.

5. Standard 2D theory yields global existence and uniqueness.

## Registry label
- supporting-instance
- non-frontier
- tool-validation
- certified-test-case

## Use rule
This item validates Kairos on a hard classical PDE in an already globally well-posed regime.
It does not count as a frontier closure or flagship program completion.
