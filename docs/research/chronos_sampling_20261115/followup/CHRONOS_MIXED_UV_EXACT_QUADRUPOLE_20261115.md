# Chronos: exact mixed-(U,V) quadrupole matrices and refined four-point interval

**Date:** 2026-11-15. **Result:** exact rational polynomial integration of the ell=2 causal operator on bivariate basis of total degree ≤2, with conditional strict rational bound on p_(4,2). **Status:** PROVED for integral identity, COMPUTATION_PASS for finite matrix and bound, exact probability OPEN, infinite-growth stability OPEN, Lean NOT_RUN, Git NOT_MODIFIED. Not independently externally reviewed.

## Normalizations and formula

Unit Minkowski 4D diamond with normalized radial measure `12(b-a)^2 da db`, `0<a<b<1`. Define `r=(b-a)/2`, `U=(ab)^2`, `V=((1-a)(1-b))^2`. For target `0<c<d<1` let `r_y=(d-c)/2`, and use the radial harmonic operator whose angular eigenvalue at degree two on the partial-angle region `0<a<c<b<d` is

`lambda_2 = f (1-f) (1-2f)`, where `f=(c-a)(d-b)/((b-a)(d-c))`.

In the full-angle region, the ell=2 eigenvalue vanishes. The action on the solid-harmonic test input `F_ij=r² U^i V^j` is

`K_2 F_ij(c,d) = [3/(d-c)^3] * integral_(a=0)^c integral_(b=c)^d (b-a)(c-a)(d-b)(b-c)(d-a) * [(b-a)(d-c)-2(c-a)(d-b)] * U(a,b)^i V(a,b)^j db da`.

Substitute `a=c u`, `b=c+(d-c) v`. The denominators cancel exactly, yielding a polynomial square integral:

`K_2 F_ij(c,d) = 3 c²(d-c) integral_0^1 integral_0^1 (1-u) v (1-v) (d-cu) (b-a) [(b-a)-2c(1-u)(1-v)] U(a,b)^i V(a,b)^j du dv`.

All coefficients are rational for integer `i,j≥0`. The action is polynomial in `(c,d)`, so all Gram and energy entries are also rational through the monomial integration identity

`integral_(0<c<d<1) c^p d^q dc dd = 1/((p+1)(p+q+2))`.

For ell=2, the Gram and energy measures are respectively

`G_ij,kl = integral 3/4 (d-c)^6 U^(i+k)V^(j+l) dc dd`, 

`B_ij,kl = integral 12(d-c)^2 (K_2 F_ij)(K_2 F_kl) dc dd`.

## Exact finite-dimensional result

On the degree-one span `(r², r² U, r² V)`:

`t_2^[1]=221203/595094500`, 

`s_2^[1]=4062793239133/41434083279839250000`.

On the degree-two span `(r², r²U, r²V, r²U², r²UV, r²V²)`:

`t_2 = 2217278773590300096043/4224747009459816329490000`,

`s_2 = 2534224692359879386796822545357673466752899/17848487293939661406615903047685656243660100000000`.

Here `t_2=tr(G^-1 B)`, `s_2=tr[(G^-1 B)^2]`. The exact `U`-only action was checked for `i=0,1,2` against the separately established all-harmonic identity

`K_2(r² U^i) = kappa_(2,i) r_y² U_y^(i+1)`, 

`kappa_(ell,k)=12/((ell+1)(4k+ell+4)) * [1/(2k+1)-1/(2k+2)-1/(2k+ell+2)+1/(2k+ell+3)]`.

## Conditional global enclosure

Assume the previously independently audited four-point reduction and angular trace decomposition, the exact zero-mode contribution `A0=513/875875`, exact first-five angular masses `b_ell=d_ell+c_ell pi²`, and rigorous tail `sum_(ell>=6) A_ell ≤ R_5²/13`. For `C_ell=K_ell* K_ell` positive trace class and a projection `P`, use

`tr[(P C_ell P)^2] ≤ tr(C_ell²) ≤ tr[(P C_ell P)^2] + b_ell² - tr(P C_ell P)²`.

Use the degree-two mixed `(U,V)` subspaces for ell=1,2 and archived eight-dimensional `U`-only spaces for ell=3,4,5. The exact rational arithmetic (40-term Machin pi enclosure) proves

**`0.0854113582 < p_(4,2) < 0.0854281629`.**

Width < `1.68047e-5`, versus previous mixed-dipole-only width approximately `1.83027e-5`. These are conditional rigorous bounds, NOT an exact value of p_(4,2).

## Validation and boundary

- SymPy exact integration of all 21 independent entries of each `6x6` Gram and energy matrix: PASS.
- Exact three-dimensional preliminary matrix: PASS.
- One-variable coefficient reproduction for ell=2 at i=0,1,2: PASS.
- Mixed dipole ell=1 matrix reused and re-computed from original source; higher modes ell=3..5 imported from archived exact script: PASS.
- Strict comparison with rational bounds, no floating-point arithmetic for decision: PASS.
- Full trace and full sum: OPEN.
- Full Lean kernel verification and external independent review: NOT_RUN.
- No GitHub change, merge, or branch removal.

Sources: `chronos_mixed_uv_quadrupole_exact_20261115.py`, `chronos_mixed_uv_quadrupole_bounds_20261115.py`, the prior dipole and eight-function harmonic scripts, and original four-point reduction certificate. The `bounds` script currently expects these files in `/mnt/data`; that is a reproducibility limitation in the standalone source archive, not a mathematical assumption.