# GfE axial 221 epsilon-zero simple-root certificate — 2026-09-24

Status: **certified within the stated epsilon-zero projected branch**.

## Result

For the projected, massless, odd-parity GfE operator at the Schwarzschild point

[
arepsilon=eta^2/M^4=0,
]

the first axial overtone ((ell,m,n)=(2,2,1)) has exactly one quasinormal-mode root, counting multiplicity, in

[
left|
Omega-
left(0.34671099687810464-0.27391487535351056iight)
ight|
le 5	imes10^{-6}.
]

Because the zero count is one, the enclosed root is simple.

## Certified chain

The standalone verifier checks:

- an ingoing horizon Frobenius series and an all-orders weighted coefficient majorant;
- nonvanishing of the regular horizon factor at the launch point;
- 96-bit fixed-point affine center/sensitivity propagation to the real matching point (z=3);
- an outgoing Laurent-Jost endpoint with a positive vertical-ray Volterra damping margin;
- independent affine propagation from the outgoing endpoint to (z=3);
- separate nonlinear-remainder transport on both sides to prevent interval wrapping; and
- a Rouché boundary inequality on the stated frequency disk.

The decisive numerical bounds are

[
q_{m hor}le 0.7141139467515436<1,
qquad
delta_{infty}ge0.5893870317770651>0,
]

and

[
	ext{linear lower}=1.033708584346826	imes10^{-4},
]

[
	ext{total error upper}=7.88238175259142	imes10^{-5},
]

so the certified Rouché margin is

[
2.45470409087684	imes10^{-5}>0.
]

## Exact claim boundary

This certificate is **epsilon-zero only**. It does not certify an (arepsilon>0) continuation tube, the derivative

[
left.rac{dOmega_{221}}{darepsilon}ight|_0,
]

the polar sector, axial-polar splitting, or the full unreduced trace-log spectrum. It also does not establish full gravity closure or observational detectability.

## Repository anchors

- verifier: `tools/gfe/verify_gfe_axial_221_epsilon0_simple_root.py`
- machine-readable certificate: `artifacts/chronos/gfe_axial_221_epsilon0_simple_root_certificate.json`
- regression test: `tests/test_gfe_axial_221_epsilon0_simple_root.py`
