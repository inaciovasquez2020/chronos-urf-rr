# Chronos: distribution-free prefix null-layer theorem

**Date:** 2026-11-15  
**Classification:** PROVED (finite probability inequality and causal geometry); COMPUTATION_PASS (exact-arithmetic regressions); Lean NOT_RUN; Minkowski first-choice localization OPEN; infinite-growth double limit OPEN.  
**Repository:** no changes made.

## 1. The precise finite theorem

Let \(X_1,\dots,X_N\) be iid random points from any probability measure \(\mu\) on a measurable strict partial order \((D,\prec)\). Let
\(w(x)=\mu\{y:y\prec x\}\). For any potentially random rule that chooses a linear extension \(L\) of the induced order, and for all \(1\le n\le N\) and \(0\le\delta\le 1\),

\[
 \Pr\!\left(\max_{1\le k\le n}w(L_k)\ge\delta\right)
 \le N\Pr\bigl(\mathrm{Bin}(N-1,\delta)\le n-1\bigr).
 \tag{1}
\]

No uniform-linear-extension assumption is required; the rule can be deterministic, adversarial, or depend on the entire point configuration.

**Proof.** A point placed among the first \(n\) positions must have at most \(n-1\) strict predecessors in the whole sample. Conditional on \(X_i=x\), its number of predecessors is \(\mathrm{Bin}(N-1,w(x))\). The binomial lower tail is decreasing in \(w(x)\). Bound the probability that point \(i\) both has \(w(X_i)\ge\delta\) and has at most \(n-1\) predecessors by the displayed binomial lower tail, and sum over \(i=1,\dots,N\).

For \(N\ge 3\), set
\[
 \delta_{N,n}=\frac{4(n+2\log N)}{N-1}.
\]
Assume \(\delta_{N,n}\le1\). With \(\mu=(N-1)\delta_{N,n}=4(n+2\log N)\), we have \(n-1\le\mu/4\). The lower-tail Chernoff inequality \(\Pr(B\le\mu/4)\le\exp(-9\mu/32)\) gives
\[
 \boxed{\Pr\bigl(\max_{k\le n}w(L_k)\ge\delta_{N,n}\bigr)
 \le N^{-5/4}\exp(-9n/8).}\tag{2}
\]
In particular, for *every* deterministic sequence \(n_N=o(N)\), \(\max_{k\le n_N}w(L_k)\xrightarrow{\Pr}0\), uniformly over all choices of valid linear extension.

## 2. Flat 4D Minkowski-diamond specialization

Let \(D=\{(t,\mathbf x):0\le t\le1,\|\mathbf x\|\le\min(t,1-t)\}\), \(r=\|\mathbf x\|\), and \(a=t-r,\ b=t+r\). The normalized past volume is exactly
\[
 w(t,r)=a^2b^2=(t^2-r^2)^2.
\]
Consequently, except on an event of probability at most the right side of (2), every one of the first \(n\) events lies in the explicit region
\[
 0\le t^2-r^2\le\sqrt{\delta_{N,n}}.
 \tag{3}
\]
For fixed \(n\), this is a shrinking neighborhood of the *past-null boundary* \(a=0\), including the bottom tip. For \(n=o(N)\), the entire growing prefix is likewise confined to a shrinking layer, even for adversarial linear-extension choices.

## 3. Angular collision necessary for comparable prefix pairs

Consider two causally comparable events \(X\prec Y\) among the first \(n\) positions and assume their radial coordinates both satisfy \(r_X,r_Y\ge\varepsilon>0\). Let \(\theta\in[0,\pi]\) be the spatial-angle separation. The exact Minkowski identity is
\[
 (t_Y-t_X)^2-\|\mathbf x_Y-\mathbf x_X\|^2
 =(b_Y-b_X)(a_Y-a_X)-2r_Xr_Y(1-\cos\theta).
 \tag{4}
\]
For a causal pair the right side is nonnegative and both null-coordinate differences are nonnegative. If both past volumes are \(\le\delta\), then \(b_X,b_Y\ge2\varepsilon\), hence \(a_X,a_Y\le\sqrt\delta/(2\varepsilon)\), giving
\[
 \boxed{1-\cos\theta\le\frac{\sqrt\delta}{4\varepsilon^3},
 \qquad
 \theta\le\frac\pi{2\sqrt2}\frac{\delta^{1/4}}{\varepsilon^{3/2}}.}\tag{5}
\]
The angle estimate follows from \(1-\cos\theta\ge2\theta^2/\pi^2\). With fixed \(n\) and fixed \(\varepsilon\), this is an angular width \(O((\log N/N)^{1/4})\).

**Interpretation / exact obstruction.** For fixed prefix length, any remaining comparable pairs must either (i) involve a point whose spatial radius approaches the bottom tip or (ii) involve spatial directions separated by a shrinking angle. Proving that neither event carries persistent linear-extension probability would yield vanishing fixed-prefix comparability. Rotational symmetry alone is insufficient: uniform one-point angular marginals do not exclude strongly correlated angular pairs. First-choice delocalization \(Q_N\to0\) is independently OPEN; it is not implied by this localization theorem.

## 4. Independent executable checks and limits

The standalone Python certificate `chronos_prefix_null_layer_confinement_20261115.py` ran successfully in the isolated environment:

- 17 rational binomial-tail / Chernoff comparisons at finite \(N,n\), all PASS;
- 2,000 exact rational Minkowski kinematic identities, all PASS;
- the angular inequality checked at every randomly sampled comparable configuration within those cases.

The mathematical claim is supported by the proof above; finite checks are not a replacement for it.

**OPEN:** distribution of the maximal first-choice extension weight \(Q_N\); joint angle and bottom-tip selection laws of the first \(n\) events; \(\lim_{n\to\infty}\lim_{N\to\infty}\mathbb E p(P_N,n)\); exact \(p_{4,2}\).
