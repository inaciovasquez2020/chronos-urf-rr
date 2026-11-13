# Quantitative local inverse and finite-sample confidence theorem (2026-11-12)

**Status:** PROVED on paper (standard probability and differentiable-map arguments) with a standalone exact-rational constants verifier and bounded discrete-change oracle. No Lean verification or nonlinear numerical response calculation. Novelty NOT ESTABLISHED. This result is independent of whether Chronos #1355's full fixed-N covariance PR has merged.

## Hypotheses, not hidden claims

Use exactly the normalized 4D Minkowski diamond D, base measure \(\mu_0\), and conformal family from the already merged local-identifiability checkpoint:
\[
  u_\theta(x)=1+a h(x)+b\phi(x),\quad
  p_\theta(x)=\frac{u_\theta(x)^2}{\mathbb E_0 u_\theta^2},\quad
  \theta=(a,b).
\]
Here \(h=\{[((1+t)^2-r^2)^2+((1-t)^2-r^2)^2]\}/16\), \(\phi=t^2+(5/9)r^2\) and \(|t|+r\le1\). Positivity and smoothness hold if \(\rho=|a|+|b|<1\). Indeed \(0\le h\le1\) and \(0\le\phi\le1\): writing \(s=|t|\), the convex radial inequalities give \(h\le[(1+s)^4+(1-s)^4]/16\le1\), while \(\phi\le s^2+5(1-s)^2/9\le1\). No unknown dimension, arbitrary metric, intrinsic event law, or gravitational field equation is inferred.

Let \(F(\theta)=(P_2(\theta),P_3(\theta))\) be the probabilities that two, respectively three, iid events sampled from \(p_\theta\) form a causal chain. The causal relation is held fixed (conformal invariance). The already verified exact flat derivative is
\[
J=DF(0)=\begin{pmatrix}1/25&0\\9/3500&16/165375\end{pmatrix}.
\]
Its inverse matrix has entries \(25,0,-42525/64,165375/16\); hence the induced infinity norm is exactly \(M=\|J^{-1}\|_\infty=704025/64\).

## Rigorous uniform Hessian estimate

Fix a parameter vector with \(\rho<1\) and let \(L=1-\rho\). For \(f_1=h,f_2=\phi\), set \(g_i(x)=f_i(x)/u_\theta(x)\in[0,1/L]\). The normalized log density has score
\[
s_i(x)=\partial_i\log p_\theta(x)
      =2\big(g_i(x)-\mathbb E_\theta g_i\big),
\]
so \(|s_i|\le2/L\). Differentiate the score, using \(\partial_j\mathbb E_\theta g_i=\mathbb E_\theta[-g_i g_j]+2\operatorname{Cov}_\theta(g_i,g_j)\), to obtain
\[
\partial_j s_i
=-2\big(g_i g_j-\mathbb E_\theta[g_i g_j]\big)
-4\operatorname{Cov}_\theta(g_i,g_j).
\]
The first difference has absolute value at most \(1/L^2\). The bounded-variable covariance inequality \(|\operatorname{Cov}(g_i,g_j)|\le1/(4L^2)\) follows by Cauchy–Schwarz and Popoviciu's variance bound. Therefore
\[
|\partial_j s_i|\le3/L^2.
\]

The log-density score of a k-point independent product sample is a sum of k such scores. For any parameter-independent measurable indicator \(H_k\in[0,1]\) (in particular chain formation), differentiation under the integral is legitimate on every compact subcube \(\rho<1\); the second derivative is the expectation of \(H_k\big(S_i S_j+\partial_j S_i\big)\). Consequently
\[
|\partial_{ij}P_k(\theta)|\le\frac{4k^2+3k}{(1-\rho)^2}.
\]
For both k=2 and 3 the common bound is \(45/(1-\rho)^2\).

## A certified explicit inverse neighborhood

Take the closed cube \(Q=[-r_0,r_0]^2\), with \(r_0=1/4{,}000{,}000\). Every \(\theta\in Q\) has \(\rho\le2r_0\). Apply the mean-value theorem to each Jacobian entry and sum two columns:
\[
\sup_{\theta\in Q}\|DF(\theta)-J\|_\infty
\le\frac{180r_0}{(1-2r_0)^2}.
\]
Let
\[
\kappa=M\frac{180r_0}{(1-2r_0)^2}
=\frac{1980070312500}{3999996000001}<\frac12.
\]
For \(\theta,\eta\in Q\), the integral mean-value formula along the segment contained in Q gives
\[
\|J^{-1}(F(\theta)-F(\eta))-(\theta-\eta)\|_\infty
\le\kappa\|\theta-\eta\|_\infty.
\]
It follows that F is **injective on Q** and, precisely,
\[
\|\theta-\eta\|_\infty\le
\frac{M}{1-\kappa}\|F(\theta)-F(\eta)\|_\infty
<\frac{704025}{32}\|F(\theta)-F(\eta)\|_\infty.
\]

This cube radius is 6.25 times the previously established \(1/25{,}000{,}000\). The proof requires neither numerical inversion nor a global one-to-one assumption.

## Nonasymptotic confidence-set coverage and diameter

For exactly N independent events drawn under any fixed \(\theta_0\in Q\), define \(U_k\) as the fraction of unordered k-subsets that form chains, k=2,3. Replacing one input event can affect at most \(\binom{N-1}{k-1}\) of the \(\binom Nk\) kernel terms; thus its bounded-difference coefficient is \(k/N\). For N≥3, McDiarmid's inequality and a union bound yield
\[
\Pr_{\theta_0}\left(
\bigcap_{k=2,3}\{|U_k-P_k(\theta_0)|\le\epsilon_k\}
\right)\ge1-\alpha,
\quad
\epsilon_k=k\sqrt{\frac{\log(4/\alpha)}{2N}},
\quad 0<\alpha<1.
\]
The **inverse-image confidence set**
\[
C(U)=\{\theta\in Q:\ |F_k(\theta)-U_k|\le\epsilon_k,\ k=2,3\}
\]
therefore contains the true \(\theta_0\) with probability at least \(1-\alpha\). Every realization, whether or not C is empty, satisfies
\[
\operatorname{diam}_\infty C\le
\min\left(2r_0,\frac{2M}{1-\kappa}\max_k\epsilon_k\right)
\le\min\left(2r_0,4M\epsilon_3\right).
\]
An empty set does not cover the truth; the coverage claim is probabilistic, not a promise that the set is nonempty for all random datasets.

### A sharper U-statistic concentration option

The full U-statistic \(U_k\), k=2,3, is the average over all k-subsets, with 0/1 kernels. Let \(m_k=\lfloor N/k\rfloor\). Under a uniform random permutation of the N iid inputs, partition its first \(k m_k\) positions into \(m_k\) **disjoint** k-blocks. Conditioned on the input sample, the average block indicator has expectation \(U_k\), by symmetry. Jensen's inequality for the exponential moment followed by the independent-block Hoeffding inequality therefore gives the **distribution-free U-statistic tail bound**
\[
 \Pr_\theta(|U_k-P_k(\theta)|>e)\le2\exp(-2m_k e^2).
\]
Thus the same confidence-set proof works with the sharper radii
\[
\epsilon_k^{(U)}=\sqrt{\frac{\log(4/\alpha)}{2\lfloor N/k\rfloor}},
\quad k\in\{2,3\},
\]
for any N≥3. In particular \(\epsilon_3^{(U)}\ge\epsilon_2^{(U)}\). The deterministic confidence-set diameter bound remains \(\operatorname{diam}_\infty C\le\min(2r_0,4M\epsilon_3^{(U)})\).

For \(\alpha=1/20\) and the sufficient target \(4M\epsilon_3^{(U)}\le r_0\), the exact arithmetic threshold using \(\log80<5\) is
\[
N\ge 232336500292968750000000
\]
(about \(2.32\times10^{23}\) observations), versus \(697009500878906250000000\) (about \(6.97\times10^{23}\)) using McDiarmid's bound. These astronomically large **sufficient** thresholds emphasize that the result is mathematically certified but not practically useful; no lower bound on the information-theoretic sample requirement is implied.

This is a *valid finite-N theorem* but the upper bound is extremely conservative. As an explicit illustration, for confidence \(95\%\), \(\log(80)<5\). Enforcing the stronger sufficient target \(4M\epsilon_3\le r_0\) requires \(N\ge 697009500878906250000000\) (approximately \(6.97\times10^{23}\)). The tightness and practical usefulness of this bound have NOT been established. The exact rational verifier records one sufficient integer N without using floating-point logarithms.

## Verification and open boundary

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -B tools/verifier/causal_chain_local_inverse_certificate.py
```

The standard-library verifier tests the exact Jacobian inverse, norm, Hessian coefficient, cube contraction factor, confidence diameter algebra, a conservative rational sample threshold and an exhaustive independent three-atom discrete bounded-differences oracle. Each fraction is computed exactly. This is a certificate of numerical constants and bounded finite examples, **not a Lean formalization or an exhaustive search over real parameters**. The proof of the analytic hypotheses is supplied above.

**OPEN:** nonlinear response evaluation/parameter-efficient confidence sets; substantially improved nonasymptotic and practical sample bounds; intrinsic geometry and dimension inference; Einstein/gravity dynamics. These remain independent scientific obligations, not implied by the local inverse.
