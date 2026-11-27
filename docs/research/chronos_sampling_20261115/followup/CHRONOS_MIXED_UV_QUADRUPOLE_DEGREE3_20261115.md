# Chronos: degree-three exact mixed U,V quadrupole compression

Date: 2026-11-15. Evidence: exact symbolic computation (SymPy) + rational-arithmetic enclosure; **conditional** on archived four-point geometric reduction, angular decomposition, zero-mode value and harmonic Hilbert–Schmidt masses. No Lean verification. Minkowski infinite-growth stability and exact p_(4,2) remain OPEN.

## Computation

Work in the ell=2 radial angular sector with `U=(ab)^2`, `V=((1-a)(1-b))^2`, and the ten monomials `r^2 U^i V^j` for `i+j<=3`, ordered
`[(0,0),(1,0),(0,1),(2,0),(1,1),(0,2),(3,0),(2,1),(1,2),(0,3)]`.

The imported causal-cap integral is evaluated as an exact polynomial integral, producing `G` and `B` as 10x10 rational symmetric matrices. The operator compression invariants `t=tr(G^-1 B)` and `s=tr((G^-1 B)^2)` are

```
t = 211705308462723587738252837621548789701227 / 342094974046218133616335235209633511456344200
s = 327340973508093362321536910843963394504784831202485995379938343305601072729841381 / 2035286456829263625004409954845640668334833280982757286910358236892020781725607458672000
```

Approximate `t=0.000618849514094648810`, `s=1.60832875593370779e-7`. The exact one-variable harmonic action was cross-checked at `(i,j)=(0,0),(1,0),(2,0),(3,0)` (four checks), and the archived degree-two 6x6 quadrupole invariants were independently recomputed and matched byte-for-byte.

The trace inequality for positive trace-class `C_l=K_l* K_l` and orthogonal polynomial compression is

` s_l <= tr(C_l^2) <= s_l + b_l^2 - t_l^2 `,

where `b_l=tr(C_l)` is the independently archived Hilbert–Schmidt mass. The full angular tail at `l>=6` remains bounded as in the archived certificate. With ell=1 degree-three, ell=2 degree-three, ell=3 mixed degree-two, ell=4,5 archived one-variable degree-eight, the conditional exact rational tests establish

`0.08541223417 < p_(4,2) < 0.08542295380`.

The displayed float approximations are `0.085412234178565402` and `0.085422953792163789`. These are not closed-form evaluations; the strict decimal claims are exact Fraction comparisons.

## Marginal benefit for adding four functions

Compared with degree-two mixed compression in each sector, the degree-three ell=1 expansion changes the lower endpoint by `+6.9456856575e-7` and the upper endpoint by `-4.5883258661e-6` (total width saving `~5.28289443e-6`). Degree-three ell=2 changes the lower endpoint by `+1.1308482514e-7`, the upper endpoint by `-5.32077171596e-7` (total width saving `~6.45161997e-7`). Hence ell=1 degree-three was ~8.19x more effective per added basis function, in this comparison.

Relative to the earlier mixed l=1,2,3 degree-two bounds, the joint update reduces interval width to `1.0719613598390265e-5`, or 64.39% of the old width. Relative to the preceding degree-three dipole-only checkpoint, ell=2 reduces width by ~`6.4516e-7`.

## Independent boundary

Exact matrix entries and rational trace comparisons were executed and passed. These scripts do **not** independently rederive the 4D geometry, `A_0`, or `b_l` constants; the final interval remains conditional on those previously audited values. No independent reviewer or Lean kernel has checked these theorems. Nothing was committed, pushed, or merged.

## Reproduction

Run from the directory of the enclosed files, with SymPy available:

`python3 chronos_mixed_uv_quadrupole_degree3_20261115.py`

`python3 chronos_mixed_uv_quadrupole_degree3_bounds_20261115.py`

The second script uses pinned exact rational values for ell=1 degree-three and the archived exact ell=1..5 baseline receipt (`chronos_mixed_uv_octupole_bounds.log`). Resource-guarded failure is INCOMPLETE, never PASS.