# Chronos: rigorous two-sided harmonic trace compression (2026-11-15)

**Result:** A rational-arithmetic improvement of the bounds on the uniform-linear-extension four-event comparable-first-pair probability, conditional on the archived four-point reduction, spherical-harmonic decomposition, zero-mode trace and first five Hilbert-Schmidt mode masses. **Exact p_(4,2) OPEN. Lean NOT_RUN. Git NOT_MODIFIED.**

## The missing upper-bound lemma

Fix a spherical-harmonic degree `ell>=1`, and let `K_ell` denote the causal integral operator restricted to the radial/time Hilbert space. Set `C=K_ell^* K_ell`, a positive trace-class operator. Its Hilbert-Schmidt mode mass is `b_ell=tr(C)`. Choose a finite-dimensional orthogonal projection `P` onto the span of `r^ell W_-^m` for `m=0,...,d-1` in a fixed spherical-harmonic component. Set `t=tr(PCP)` and `s=tr((PCP)^2)`. The exact rational Gram and energy matrices are

`G_ij = E[r^(2ell) W_-^(i+j)]`,
`B_ij = kappa_(ell,i) kappa_(ell,j) E[r^(2ell) W_-^(i+j+2)]`,

where `kappa` is the all-harmonic action coefficient in the earlier certificate. Hence `t=tr(G^-1 B)` and `s=tr((G^-1 B)^2)`.

In the decomposition `H=PH ⊕ (1-P)H`, write `C=[A, X; X*, D]`. Positivity implies the Hilbert-Schmidt bound `||X||_HS^2 <= tr(A) tr(D)`. For example, writing `C=Y*Y`, with Y_P=YP and Y_Q=Y(1-P), gives `||Y_P*Y_Q||_HS^2 <= ||Y_P||_HS^2 ||Y_Q||_HS^2`. Also `tr(D^2) <= (tr D)^2`. Therefore

`tr(C^2) = s + 2||X||_HS^2 + tr(D^2)`

obeys the **two-sided trace compression bound**

`s <= tr(C^2) <= s + 2t(b_ell-t)+(b_ell-t)^2 = s + b_ell^2 - t^2`.

Both inequalities are valid even when `K_ell` is not self-adjoint; positivity is used only for `C=K_ell^*K_ell`. The upper bound improves on the simpler inequality `tr(C^2)<=b_ell^2` when the compressed operator has rank greater than one, because `s<=t^2`.

## Rational certification

The archived decomposition is `E[J_+^2]=A_0+sum_(ell>=1) (2ell+1) tr(C_ell^2)`, `A_0=513/875875` and `p_(4,2)=3557/42000+(6/5) E[J_+^2]`. For `ell=1,...,5` the archived exact mode masses `b_ell=d_ell+c_ell*pi^2` are inserted with rigorous rational bounds on pi from Machin's formula and alternating arctangent remainders. Their error is tiny compared with the finite projection residual. The remaining `ell>=6` tail obeys

`sum_(ell>=6) (2ell+1) tr(C_ell^2) <= R^2/13`,

where `R=3/140 - sum_(ell=1)^5 (2ell+1)b_ell`. The script bounds `R` above by subtracting the lower rational bounds for the known `b_ell`. It checks all needed positivity assumptions exactly.

Using degrees 1..5 and `d=8` polynomial test functions per degree, the exact rational certificate proves

**0.085396726 < p_(4,2) < 0.085438735.**

The computed rational endpoints, displayed numerically (not serving as the proof), are `0.08539672610066572...` and `0.08543873484919789...`.

Earlier d=6 all-harmonic reporting had displayed `p>0.085396713989`; the exact rational recomputation gives `0.08539671395879227...` for degrees 1..5 and dimension 6. That previous displayed decimal is *not certified by this calculation* and must not be reused. The new d=8 bound is stronger and checked in exact arithmetic.

The certificate also checks strict monotonicity of the lower and upper endpoints through dimensions 1..8 and the source-mode positivity inequalities `b_ell > t`.

## Boundaries

- This is an independently derived **operator trace residual inequality** coupled to previously archived mathematical inputs, not a standalone fresh derivation of the four-event geometric reduction or the angular HS masses.
- This proves a narrower interval, **not an exact value** for the common-future moment.
- No proof that polynomial test spaces are dense in the relevant operator domain is provided here; thus a fully quantified d→∞ convergence theorem is not claimed.
- The uniform-linear-extension infinite-growth stability conjecture is separate and **OPEN**.
- Git PR #1364 is unchanged, Lean kernel verification NOT_RUN, external mathematical review OPEN.

Reproduce with `python3 -E -B chronos_two_sided_harmonic_trace_certificate_20261115.py` (Python 3 standard library, no external dependencies). A nonzero exit or timeout is not PASS.