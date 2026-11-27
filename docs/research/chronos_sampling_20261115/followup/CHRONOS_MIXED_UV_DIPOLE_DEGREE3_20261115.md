# Chronos — mixed U,V degree-three dipole compression (2026-11-15)

**Status:** COMPUTATION_PASS exact-rational calculation; mathematical enclosure CONDITIONAL on previously audited four-point reduction, angular harmonic decomposition, zero-mode trace, and rigorous higher-mode bounds. Exact p_(4,2) OPEN. Lean NOT_RUN. No Git modification.

## Model and basis

4D Minkowski Alexandrov diamond D, null variables 0<a<b<1, radial normalized measure 12(b-a)^2 da db, r=(b-a)/2, U=(ab)^2, V=((1-a)(1-b))^2. In the dipole sector ell=1, use F_{ij}=r Y_{1m} U^i V^j. The 10 monomials (i,j) with i+j<=3 form the complete bivariate polynomial degree-three basis.

The causal-cap eigenvalue is lambda_1=f(1-f), with f=(c-a)(d-b)/((b-a)(d-c)) on a<c<b<d. Both denominator factors cancel against the radial volume and solid-harmonic terms. Mapping a=cu, b=c+(d-c)v makes action(i,j) an integral of a polynomial on [0,1]^2; remaining radial Gram and energy entries use 0<c<d<1. All entries are rational. See source certificate for exact formulas and checks.

Define Gram G and energy B by G_ij=<F_i,F_j>, B_ij=<T F_i,T F_j>. The ten-dimensional compression of positive C=K_1^*K_1 gives t=tr(G^-1 B), s=tr((G^-1 B)^2). Independent exact rational computation yields:

- t = 989610632475598595359290706541/327664864777456922359616458200000
- s = 444071837107849960272625367952385147509253975084225833789945773/89434431586821065345047836938559580574587847734324185250920000000000

For any projection P onto this test space and positive trace-class C, the two-sided inequality s <= tr(C²) <= s+b²-t² holds with b=tr(C). Replacing only ell=1 in the prior ell=1,2,3 mixed/ell=4,5 U-only enclosure, and retaining zero-mode and ell>=6 spectral remainder, gives the **conditional strict rational interval**

    0.08541212109 < p_(4,2) < 0.08542348587.

The rational endpoints are derived from exact previous endpoints (stored in `chronos_mixed_uv_octupole_bounds.log`) by adding (18/5)*(s_new-s_old) to the lower endpoint, and (18/5)*[(s_new-s_old)-(t_new²-t_old²)] to the upper endpoint. (18/5)=(6/5)*(2*ell+1) for ell=1.

## Verified execution and limitations

- Dipole degree-three ten-function basis: exact polynomial action, symmetric G/B, invertible G, positive t,s with s<=t²; PASS.
- Exact rational updated interval comparison: PASS. Previous upper/lower endpoints are *inputs* from an archived exact certificate; their full provenance is not independently re-derived here.
- Degree-three incremental 7 and 8-function computations also passed but are not required.
- Exact full common-future second moment: OPEN. Unrestricted convergence of bounds requires increasing mixed polynomial degree and angular cutoff with certified tail.
- Infinite-growth sampling stability: OPEN. No Lean axioms audit; NOT_RUN.

**HEAD:** not inspected locally; PR #1364 untouched. No commits, pushes, merges or deletions.