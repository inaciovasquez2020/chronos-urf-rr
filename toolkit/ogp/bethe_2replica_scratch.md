# bethe_2replica_scratch.md
# Two-Replica Bethe Functional for Hard-Core (Independent Set) Overlap Curvature
# Status: Differentiation Target (Frozen). No claimed derivations beyond algebraic setup.

---

## 0. Scope

Goal: define explicit, differentiable objects whose second derivative in the overlap direction yields the curvature constant
\[
\kappa_{\mathrm{Bethe}}(\rho,\Delta) := -\psi''(\nu_2),
\quad
\psi(q)=\frac1n\log|\Omega(q)|.
\]
This file enumerates **all standard equivalent formulations** (“iterations”) of the two-replica overlap-constrained Bethe functional that one can attempt to differentiate, and the exact interfaces to the LIB barrier.

---

## 1. Base Model (Single Replica)

Graph: $\Delta$-regular (or locally tree-like with degree $\Delta$).

Independent sets:
\[
\Omega=\{\sigma\in\{0,1\}^V:\ \forall (i,j)\in E,\ \sigma_i\sigma_j=0\}.
\]

Hard-core activity $\lambda>0$; Gibbs weight:
\[
\mu(\sigma)=\frac1Z \lambda^{\sum_i \sigma_i}\mathbf 1_{\sigma\in\Omega},
\qquad
Z=\sum_{\sigma\in\Omega}\lambda^{|\sigma|}.
\]

Single-replica cavity message parameterization (RS):
Let $u$ denote the cavity “occupied probability” message on a directed edge.
Fixed point on $\Delta$-regular tree:
\[
u=\frac{\lambda(1-u)^{\Delta-1}}{1+\lambda(1-u)^{\Delta-1}}.
\]
Vertex marginal occupancy:
\[
\rho=\frac{\lambda(1-u)^\Delta}{1+\lambda(1-u)^\Delta}.
\]

---

## 2. Two Replicas and Overlap

Two configurations $(\sigma,\tau)\in\Omega\times\Omega$.

Vertex overlap (microcanonical):
\[
q(\sigma,\tau)=\frac1n\sum_{i=1}^n \sigma_i\tau_i.
\]

Overlap slice:
\[
\Omega(q)=\{(\sigma,\tau)\in\Omega\times\Omega:\ q(\sigma,\tau)=q\}.
\]

Target entropy density (microcanonical):
\[
\psi(q)=\frac1n\log|\Omega(q)|,
\quad\text{or}\quad
\psi_\lambda(q)=\frac1n\log\sum_{(\sigma,\tau)\in\Omega(q)}\lambda^{|\sigma|+|\tau|}.
\]

Curvature target at $q=\nu_2$:
\[
\kappa_{\mathrm{Bethe}}(\rho,\Delta)=-\psi''(\nu_2),
\]
when $\psi$ is twice differentiable there (RS regime).

---

## 3. Iteration A: Microcanonical Two-Replica Bethe via Joint Node-Type Frequencies

### 3.1 Joint type variables

At a vertex $i$, define the pair state
\[
s_i=(\sigma_i,\tau_i)\in\{00,01,10,11\}.
\]
Let frequencies
\[
p_{ab}=\Pr(s_i=ab),\quad ab\in\{00,01,10,11\},
\]
with constraints
\[
p_{00}+p_{01}+p_{10}+p_{11}=1,
\quad
q=p_{11}.
\]
Replica symmetry (optional but standard in RS):
\[
p_{10}=p_{01},
\quad
\rho=p_{10}+p_{11}=p_{01}+p_{11}.
\]

### 3.2 Vertex (site) term

Entropy + activity contribution:
\[
F_V(p;\lambda)
=
-\sum_{ab}p_{ab}\log p_{ab}
+
(p_{10}+p_{01}+2p_{11})\log\lambda.
\]

### 3.3 Edge (constraint) term: admissibility of neighbor pairs

Edge constraint per replica: forbids $(\sigma_i,\sigma_j)=(1,1)$ and similarly for $\tau$.
Equivalently, for an edge $(i,j)$, the pair states $(s_i,s_j)$ are allowed iff:
\[
(\sigma_i,\sigma_j)\neq(1,1)
\quad\text{and}\quad
(\tau_i,\tau_j)\neq(1,1).
\]
Let $P^{(2)}$ be a (to-be-chosen) Bethe-consistent edge joint distribution on $\{00,01,10,11\}^2$ with node marginals $p$.
Then the general Bethe free energy form is:
\[
\Phi_2(q)
=
\max_{p,P^{(2)}}\Big[
\sum_{v} \frac1n H(p_v) - \sum_e \frac1n H(P^{(2)}_e)
+
\frac1n \sum_v \mathbb E_p[\log w_v]
+
\frac1n \sum_e \mathbb E_{P^{(2)}}[\log w_e]
\Big],
\]
with weights encoding activity and hard constraints.
In the homogeneous RS setting, reduce to:
\[
\Phi_2
=
F_V(p;\lambda)
+
\frac{\Delta}{2}\,F_E(P^{(2)};p),
\]
where
\[
F_E
=
-\sum_{x,y}P^{(2)}(x,y)\log P^{(2)}(x,y)
+
2\sum_x p(x)\log p(x)
+
\sum_{x,y}P^{(2)}(x,y)\log \mathbf 1_{\mathrm{allowed}}(x,y).
\]
Here $\mathbf 1_{\mathrm{allowed}}(x,y)\in\{0,1\}$ is the edge feasibility indicator.

### 3.4 Simplified proxy edge term (heuristic-only; for quick differentiation tests)

A commonly used proxy (NOT a proof) replaces the full edge distribution by a scalar penalty depending on $p_{11}$:
\[
F_E^{\mathrm{proxy}}(q) = \log(1-q^2),
\]
so that
\[
\Phi_2^{\mathrm{proxy}}(q)=F_V(p(q);\lambda)+\frac{\Delta}{2}\log(1-q^2).
\]
Use only as a sandbox algebra target; not a valid closure without justification.

### 3.5 Differentiation target

Once an explicit $\Phi_2(q)$ is fixed (full or proxy), define saddle $q^\*$ by
\[
\partial_q\Phi_2(q^\*)=0,
\]
and curvature
\[
\kappa_{\mathrm{Bethe}}=\partial_q^2\Phi_2(q^\*).
\]

---

## 4. Iteration B: Canonical Coupling (Lagrange Multiplier / Field) and Legendre Transform

Define coupled partition function (canonical in overlap):
\[
Z_2(\eta)
=
\sum_{\sigma,\tau\in\Omega}
\lambda^{|\sigma|+|\tau|}
\exp\Big(\eta\sum_i \sigma_i\tau_i\Big).
\]
Define free energy density:
\[
\phi_2(\eta)=\frac1n\log Z_2(\eta).
\]
Then overlap expectation:
\[
q(\eta)=\phi_2'(\eta).
\]
Microcanonical entropy is Legendre transform:
\[
\psi_\lambda(q)=\inf_{\eta}\big(\phi_2(\eta)-\eta q\big).
\]
Curvature relation:
\[
\psi_\lambda''(q)= -\frac{1}{\phi_2''(\eta(q))},
\quad
\kappa_{\mathrm{Bethe}} = -\psi_\lambda''(\nu_2)=\frac{1}{\phi_2''(\eta(\nu_2))}.
\]
Thus the hinge reduces to computing **susceptibility**
\[
\chi_{\mathrm{ov}} := \phi_2''(\eta)=\frac1n\mathrm{Var}\Big(\sum_i\sigma_i\tau_i\Big),
\]
under the coupled measure.

Bethe task in this iteration: compute $\phi_2(\eta)$ via two-replica RS cavity equations, then differentiate twice.

---

## 5. Iteration C: Two-Replica Cavity Messages on the Tree

State space per vertex: $\{00,01,10,11\}$.
Define directed-edge cavity message $m$ over these 4 states:
\[
m = (m_{00},m_{01},m_{10},m_{11}),\quad m_{ab}\ge0,\ \sum m_{ab}=1.
\]

With canonical coupling $\eta$, vertex weight:
\[
w(ab)=\lambda^{a+b}e^{\eta ab}.
\]
Edge feasibility between states $x=(a,b)$ and $y=(c,d)$:
\[
\mathbf 1_{\mathrm{allowed}}(x,y)=\mathbf 1_{ac=0}\cdot \mathbf 1_{bd=0}.
\]

Tree recursion (Δ-regular):
Let incoming neighbor messages be i.i.d. copies of $m$; then the cavity update is:
\[
\widetilde m_{x}
\propto
w(x)\Big(\sum_{y} m_y \mathbf 1_{\mathrm{allowed}}(x,y)\Big)^{\Delta-1}.
\]
Normalize to obtain $m$ as fixed point:
\[
m=\mathsf T_{\Delta,\lambda,\eta}(m).
\]

Then Bethe free energy (canonical) at fixed point:
\[
\phi_2(\eta)
=
\log Z_v - \frac{\Delta}{2}\log Z_e,
\]
where
\[
Z_v=\sum_x w(x)\Big(\sum_y m_y\mathbf 1_{\mathrm{allowed}}(x,y)\Big)^\Delta,
\]
\[
Z_e=\sum_{x,y} m_x m_y \mathbf 1_{\mathrm{allowed}}(x,y).
\]

Overlap expectation:
\[
q(\eta)=\Pr(\sigma_i=\tau_i=1)=p_{11}(\eta),
\]
where
\[
p_x
=
\frac{w(x)\Big(\sum_y m_y\mathbf 1_{\mathrm{allowed}}(x,y)\Big)^\Delta}{Z_v},
\quad x\in\{00,01,10,11\},
\quad
q(\eta)=p_{11}.
\]

Curvature:
\[
\kappa_{\mathrm{Bethe}}(\nu_2)=\frac{1}{\phi_2''(\eta(\nu_2))}.
\]

This is the cleanest “differentiate the right object” formulation.

---

## 6. Iteration D: Linear Response / Hessian as Inverse Susceptibility

Define overlap susceptibility at the RS fixed point:
\[
\chi_{\mathrm{ov}}(\eta)=\frac{dq}{d\eta}.
\]
Then
\[
\kappa_{\mathrm{Bethe}}(q)=\frac{1}{\chi_{\mathrm{ov}}(\eta(q))}.
\]
Linear response computation routes:
- differentiate fixed-point equation $m=\mathsf T(m)$ w.r.t. $\eta$;
- solve the resulting linear system $(I-D\mathsf T)\,m'=\partial_\eta \mathsf T$;
- compute $q'(\eta)$ from $p_{11}(\eta)$.

Failure modes:
- if $I-D\mathsf T$ is singular (RS stability boundary), $\chi_{\mathrm{ov}}$ diverges and curvature vanishes / non-analyticities appear.

---

## 7. Iteration E: High-Δ Asymptotics (Calibration Only)

For large $\Delta$, any claim of “universal” coefficients must be justified by an explicit asymptotic expansion:
\[
\kappa_{\mathrm{Bethe}}(\rho,\Delta)
=
c_1(\rho)\Delta^{-1}+c_2(\rho)\Delta^{-2}+O(\Delta^{-3})
\]
or alternative scaling depending on the regime (e.g. $\lambda$ scaling with $\Delta$).

This file makes **no universality assumption**. High-Δ expansions are only for cross-checks once the exact Bethe Hessian is derived.

---

## 8. Conductance / LIB Interface (Downstream Use Only)

Given an overlap cut set $A$ (e.g. $q\ge\nu_2$ region vs $q\le\nu_1$ region), define conductance under stationary $\pi$:
\[
\Phi(A)=\frac{Q(A,A^c)}{\pi(A)},
\qquad
Q(x,y)=\pi(x)P(x,y).
\]
Barrier functional:
\[
\mathcal B(A)=-\log \Phi(A).
\]
Regularization convention (optional):
\[
\mathcal B_\epsilon(A)=-\log(\Phi(A)+\epsilon),\quad \epsilon\in(0,1).
\]

Quantitative hinge use:
If overlap entropy satisfies quadratic upper bound near $\nu_2$ with curvature $\kappa_{\mathrm{Bethe}}$,
then the measure of the “middle overlap” bottleneck controls $\mathcal B(A)$, yielding
\[
\lambda_1 \le \exp(-c n + O(\log n)),
\quad
\tau_{\mathrm{mix}}\ge \exp(c n - O(\log n)),
\]
with leading constant proportional to $\kappa_{\mathrm{Bethe}}(\nu_2-\nu_1)^2$.

---

## 9. Checklist: What Must Be Produced to Close the Hinge

### 9.1 Minimal closure deliverable (accept/reject)
Provide one of:
- explicit formula for $\kappa_{\mathrm{Bethe}}(\rho,\Delta)$ from Iteration C/D; or
- minimal missing lemma explaining why Bethe Hessian does not control $\psi''(\nu_2)$ in the targeted regime.

### 9.2 Internal consistency checks
- verify $q(\eta)$ monotone in $\eta$ in RS regime.
- compute $\phi_2''(\eta)\ge0$.
- check stability: spectral radius of $D\mathsf T$ < 1.
- confirm Legendre relation $\psi''=-1/\phi''$.

### 9.3 Sanity limits
- $\eta\to 0$ should recover two independent replicas (baseline overlap $q=\rho^2$).
- $\eta\to +\infty$ should force $\sigma=\tau$ on occupied vertices (max overlap).
- $\lambda\to 0$ yields $\rho\to 0$, overlap curvature should match sparse Bernoulli limit.

---

## 10. Optional: Numeric Recipe (Population Dynamics / Fixed Point Solve)

Canonical route (Iteration C):
1. initialize message $m^{(0)}$ on 4 states.
2. iterate $m^{(t+1)}=\mathsf T(m^{(t)})$ to tolerance.
3. compute $(\phi_2(\eta), q(\eta))$ from $Z_v,Z_e$.
4. sweep $\eta$ to hit target $q=\nu_2$.
5. finite-difference $\phi_2''(\eta)$ or solve linear response for $dq/d\eta$.
6. output $\kappa_{\mathrm{Bethe}}=1/\phi_2''(\eta(\nu_2))$.

---

## 11. Notes on Validity Regime

All differentiations assume:
- RS fixed point exists and is locally stable,
- overlap slice is smooth at $\nu_2$ (no kink / 1RSB non-analyticity),
- graph is locally tree-like enough for Bethe approximation at leading order.

If any assumption fails, the file’s role is to pinpoint the obstruction precisely, not to force a coefficient.

---
