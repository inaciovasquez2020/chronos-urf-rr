# Chronos: exact mixed-U,V octupole (ell=3) matrix audit

Date: 2026-11-15. Scope: conditional four-point Minkowski probability enclosure; no claim of exact p_(4,2), Lean kernel proof or infinite-growth stability.

## Exact polynomial operator action

Let 0<c<d<1 denote the target event null coordinates, and 0<a<c<b<d source coordinates. The radial probability density is 12(b-a)^2 da db and the solid harmonic factor is r^ell=((b-a)/2)^ell. Write U=(ab)^2 and V=((1-a)(1-b))^2. The angular causal-cap eigenvalue for ell=3 is

    lambda_3(f) = f(1-f)(1-5f+5f^2),
    f=(c-a)(d-b)/[(b-a)(d-c)].

Substitute a=c*u, b=c+(d-c)*v for u,v in [0,1]; then da db=c(d-c)du dv. Put E=b-a, Q_h=(1-u)^(h+1)(1-v)^(h+1). With (R_0,R_1,R_2)=(1,-5,5), the exact causal-operator action on r^3 Y_(3m) U^i V^j is r_y^3 Y_(3m) times a polynomial whose radial coefficient is

    A_(i,j)(c,d) = (12*c*(d-c)/8) * Integral_[0,1]^2
       [ v*(d-a)*(ab)^(2i)*((1-a)*(1-b))^(2j)
         * Sum_(h=0)^2 R_h*c^(h+1)*Q_h*E^(3-h) ] du dv.

This is a polynomial integral, so all coefficients are rational. The formula follows by replacing each factor f=(c-a)(d-b)/(E(d-c)), 1-f=(b-c)(d-a)/(E(d-c)) in the causal cap; all denominators cancel. The independent numerical quadrature certificate computes the original 12*c*(d-c)*E^2*(E/2)^3*lambda_3 expression, not the canceled polynomial.

The one-variable specialization j=0 agrees exactly for i=0,1,2 with the previously archived identity

    A_(i,0)(c,d) = kappa_(3,i)*((d-c)/2)^3*(cd)^(2i+2),
    kappa_(ell,i)=12/[(ell+1)(4i+ell+4)] *
       [1/(2i+1)-1/(2i+2)-1/(2i+ell+2)+1/(2i+ell+3)].

## Mixed compression matrices

Use the six monomials (i,j)=(0,0),(1,0),(0,1),(2,0),(1,1),(0,2). Define

    G_[(i,j),(k,l)] = Integral_{0<c<d<1} (3/16)*(d-c)^8 * (cd)^(2i+2k)*((1-c)(1-d))^(2j+2l) dc dd,
    B_[(i,j),(k,l)] = Integral_{0<c<d<1} 12*(d-c)^2*A_(i,j)(c,d)*A_(k,l)(c,d) dc dd.

Each is an exactly evaluated symmetric rational 6x6 matrix (21 distinct entries). Their invariant traces are

    t_3 = Tr(G^(-1) B)
        = 2174797681196964315013 / 15362186318267503574059200
        ~= 0.000141568240102052791,

    s_3 = Tr[(G^(-1) B)^2]
        = 113467177247624632542506313851682561751843 /
          12420882551429751400785696951904507678903426560000
        ~= 9.13519444192502855e-9.

These are finite-compression quantities, **not** the full ell=3 spectral trace or Hilbert-Schmidt mass.

## Two-sided interval and exact assumptions

Use previously archived assumptions: p_(4,2)=3557/42000+(6/5)E[J_+^2]; zero-mode contribution A0=513/875875; angular masses b_ell=d_ell+c_ell*pi^2 (ell=1..5); high-l tail bound R5^2/13. The trace inequality for C=K* K and an orthogonal test-space compression is

    s <= Tr(C^2) <= s+b^2-t^2.

Use exact mixed U,V degree-2 compressions for ell=1,2,3 and archived eight-dimensional U-only compressions for ell=4,5. The rational interval bounds for pi come from Machin's identity and alternating-series bounds (archived standard-library source). The standalone combined certificate asserts exact rational comparisons and prints

    0.0854114265251745 <= conditional lower endpoint,
    conditional upper endpoint <= 0.085428074195201445,

and therefore the safe decimal enclosure

    **0.085411426525 < p_(4,2) < 0.085428074196**.

The interval improves the preceding ell=1,2 enclosure (0.0854113582,0.0854281629), narrowing width from roughly 1.68047e-5 to 1.66477e-5. It remains conditional on the earlier geometric/angular normalization results. Finite rank, not exact p_(4,2).

## Verification receipts and limitations

- Exact polynomial integration SymPy: PASS (two exact 6x6 matrices; symmetric, invertible Gram; three j=0 identities).
- Independent direct (uncanceled) SciPy quadrature: 6/6 PASS for (c,d)=(1/4,3/4) and every degree-2 monomial. These float comparisons are diagnostics, **not** rigorous quadrature enclosures or proof.
- Exact rational two-sided endpoint checks: PASS. Output log included in the archive.
- Lean kernel compilation and #print axioms: NOT_RUN.
- Exact full ell=3 trace, full E[J_+^2], exact p_(4,2), and infinite-growth stability: OPEN.
- No Git writes, branch promotion or merge.

NEXT: prioritize tighter finite-dimensional approximation or mass-tail estimates; the ell=3 degree-2 improvement is small compared with ell=1,2. Preserve current checkpoint.