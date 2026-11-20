# Chronos — all-harmonic Lorentz-covariant compression, 2026-11-15

**RESULT:** A new analytic identity for every spherical-harmonic degree and a rational, finite-dimensional lower certificate for the four-event prefix-comparability probability. This is conditional on the previously audited four-point reduction and harmonic decomposition. **PROVED** at the level of the following paper argument; **COMPUTATION_PASS** for the accompanying exact-rational script. **NOT Lean verified**. The exact four-point value and the infinite-growth sampling-stability limit remain **OPEN**. No Git changes.

## 1. Definitions and normalization

Let `D={ (t,v):0<t<1, |v|<min(t,1-t) }` be the unit 4D Minkowski Alexandrov diamond, and let `mu` be its uniform probability measure. Define `W(x)=(t_x^2-|v_x|^2)^2`. For the causal averaging operator `Tf(y)=integral_(x prec y) f(x) dmu(x)`, the SO(3)-isotypic decomposition reads `T=direct_sum_(ell>=0) K_ell tensor I_(2ell+1)`.

Use solid spatial spherical harmonics `r^ell Y_(ell,m)(omega)` and test functions `F_(ell,m,k)(x)=r_x^ell Y_(ell,m)(omega_x) W(x)^k` for `k>=0`.

## 2. New all-harmonic action identity

**Theorem.** For all nonnegative integers `ell,k` and all spherical harmonics of degree `ell`,

`T F_(ell,m,k)(y)=kappa_(ell,k) r_y^ell Y_(ell,m)(omega_y) W(y)^(k+1)`

with the following exact rational constant:

`kappa_(ell,k) = [12 / ((ell+1)(4k+ell+4))] * [1/(2k+1)-1/(2k+2)-1/(2k+ell+2)+1/(2k+ell+3)]`.

**Proof.** Put `s(y)=t_y^2-|v_y|^2`, so `W(y)=s(y)^2`. For fixed integer `ell`, consider the Lorentz-covariant polynomial moment tensor

`M^(mu_1...mu_ell)(y) = integral_(x prec y) x^(mu_1)...x^(mu_ell) W(x)^k dmu(x)`.

Its symmetric tensor structure, by Lorentz invariance and homogeneity under the map from the unit interval to the interval `J(0,y)`, is a linear combination of symmetrized products of `y` and the Minkowski metric. Contract with `ell` copies of any complex spatial vector `u` satisfying `u·u=0`. Its associated spacetime covector `q=(0,u)` is Minkowski-null; every metric contraction vanishes. The remaining term is proportional to `(u·v_y)^ell s(y)^(2k+2)`, i.e. `(u·v_y)^ell W(y)^(k+1)`. Powers `(u·v)^ell` with `u·u=0` span the complexification of all degree-`ell` solid spherical harmonics, yielding the claimed identity for every real harmonic by linearity.

To determine the coefficient, instead contract the same tensor with a *real* null covector `q=(1,n)`, with `|n|=1`, at the endpoint `y=(1,0)`. Then `q·y=1` (choose either metric sign convention consistently), and `kappa_(ell,k)=E_D[(t+r cos(theta))^ell W^k]`, because spatial angles are uniform and `cos(theta)` is uniform on `[-1,1]`. With `a=t-r`, `b=t+r`, the normalized radial measure is `12(b-a)^2 da db` on `0<a<b<1`. Averaging over `cos(theta)` gives `(b^(ell+1)-a^(ell+1))/((ell+1)(b-a))`. Therefore

`kappa_(ell,k)= 12/(ell+1) * integral_(0<a<b<1) (b-a)(b^(ell+1)-a^(ell+1))a^(2k)b^(2k) da db`,

and substitution `a=bs` yields the stated rational expression. It recovers the old dipole coefficient `kappa_(1,0)=1/2`, and additionally gives `kappa_(2,0)=3/10`.

The normalized radial Gram moments are exactly

`G_(ell,j)=E_D[r^(2ell) W^j] = [12/(4^ell(4j+2ell+4))] B(2j+1,2ell+3)`.

## 3. Rigorous spectral lower certificate

Let `H_ell=K_ell* K_ell`, a positive trace-class operator. For `d>=1`, define `d x d` matrices

`Gram^(ell,d)_(ij)=G_(ell,i+j)`, `Energy^(ell,d)_(ij)=kappa_(ell,i)kappa_(ell,j)G_(ell,i+j+2)` for `0<=i,j<d`.

The Gram matrix is invertible (nonzero polynomials in `W` are linearly independent under the radial measure). If `P_(ell,d)` is the orthogonal projection onto the first `d` test functions, then

`Tr(H_ell^2) >= Tr((P H_ell P)^2) = Tr((Gram^(-1) Energy)^2)`.

Consequently the `ell`-mode common-future overlap contribution obeys

`A_ell := (2ell+1)Tr(H_ell^2) >= (2ell+1)Tr((Gram^(-1) Energy)^2)`.

Apply this with `ell=1,...,8`, `d=6`, and retain the previously certified exact zero-mode value `A_0=513/875875`. The 4-point relation `p_(4,2)=3557/42000+(6/5)sum_(ell>=0) A_ell` yields the strict **rational-arithmetic certificate**

`0.085396713989 < p_(4,2) < 0.08543935`.

The upper bound is the previously audited 5-mode spectral residual bound; the new work improves only the lower bound. Full `A_ell`, the infinite sum, and the exact `p_(4,2)` remain OPEN. The denominator/numerator of the exact 6x8 rational lower certificate are large; the source computes them directly and checks the stated decimal inequality with exact Fractions. Printed SHA-256 of that exact `Fraction` string: `2d118407632ab39b3446ea79d1c722be0c3e957bb0c538d2dc9eaa4eb0bb3cc0`.

### Exact contributions to the d=6 lower bound

| ell | Lower bound on A_ell (decimal display only) |
|---:|---:|
| 1 | 2.721519213374668e-6 |
| 2 | 1.02019763e-7 |
| 3 | 7.05943453e-9 |
| 4 | 7.514988e-10 |
| 5 | 1.09415597e-10 |
| 6 | 2.01838136e-11 |
| 7 | 4.47903283e-12 |
| 8 | 1.15275203e-12 |

## 4. Independent exact checks and boundaries

`chronos_all_harmonic_compression_certificate_20261115.py` executes on Python's standard library. Its independent beta-moment and monomial ordered-simplex expansions match `kappa_(ell,k)` in 50 combinations (ell=0..9, k=0..4). It verifies previous dipole moments exactly, computes all `ell=1..8`, `d=1..6` Gram inversions and positive trace lower bounds, asserts strict monotonic improvement across d, and checks the new decimal lower bound by exact rational comparison. All tests **COMPUTATION_PASS** in the working container.

**Dependencies assumed, not reproved by this new script:** previously audited exact `A_0`, four-point reduction, and representation of overlap as angular trace sum. **Lean:** NOT_RUN. **External mathematical review:** NOT_ESTABLISHED. **Git commit/merge:** NOT_PERFORMED.