# Four-dimensional causal-chain local identifiability — analytical checkpoint (2026-11-10)

**Scope:** Two-parameter conformal deformation of one prescribed 4D Minkowski causal diamond. This is **not** an intrinsic generation law, arbitrary curvature reconstruction, a spacetime emergence theorem, or Einstein dynamics.

**Status:** Exact SymPy rational-integration check on 2026-11-10, run outside the Mac; **not Lean-verified**, no local repository build or independent review. Novelty **NOT ESTABLISHED**.

## Model and conventions

Let
[
D=\{(t,\mathbf x): |t|+\|\mathbf x\|<1\},\quad
\eta=-dt^2+dx^2+dy^2+dz^2,\quad r=\|\mathbf x\|.
]
The flat diamond volume is (V_0=2\pi/3). Define
[
A=((1+t)^2-r^2)^2,\quad B=((1-t)^2-r^2)^2,\quad
h=(A+B)/16,\quad \phi=t^2+5r^2/9.
]
For small (a,b), use
[
g_{a,b}=c(a,b)(1+ah+b\phi)\eta
]
where (c(a,b)>0) enforces (V_{g_{a,b}}(D)=V_0). Because the volume form scales by ( [c(1+ah+b\phi)]^2), the normalized sprinkling density is proportional to ((1+ah+b\phi)^2). Causal order stays that of (eta).

Write (P_k) for the probability that (k) i.i.d. volume-uniform events in (D) form one chain (with unspecified chronological labeling). Baselines: (P_2(0,0)=1/10), (P_3(0,0)=1/350).

For an even polynomial (F(t,r)), normalized flat expectation is
[
\mathbb E_0 F=12\int_0^1\int_0^{1-t} F(t,r)r^2\,dr\,dt.
]

## Rational integration receipts

| Moment | Exact value |
| --- | ---: |
| E[h] | 1/10 |
| E[h²] | 1/50 |
| E[phi] | 13/45 |
| E[h phi]-E[h] E[phi] | 0 |
| E[A B] | 64/525 |
| E[phi A B] | 1856/99225 |
| E[A²+B²] | 512/105 |
| E[phi (A²+B²)] | 11776/6615 |
| E[h A B] | 32/2205 |
| E[h (A²+B²)] | 3392/2205 |

The pair response for a perturbation \(\psi\) is
[
\partial_\psi P_2(0,0)=4\operatorname{Cov}_0(\psi,h).
]
Thus \(\partial_aP_2=1/25\) and \(\partial_bP_2=0\).

The chronological three-chain roles (earliest, middle, latest) yield
[
\partial_\psi P_3(0,0)
=2 P_3(0,0)
\left[
\frac{\mathbb E_0[\psi K]}{\mathbb E_0[AB]}
-3\mathbb E_0[\psi]
\right],
\quad K=AB+(A^2+B^2)/20.
]
Here flat past and future diamond volumes are \((\pi/24)A\) and \((\pi/24)B\). For the earliest or latest role the conditional *specified orientation* of the other two points contributes the factor \(P_2/2=1/20\). Substitution gives
[
\partial_a P_3=9/3500,\qquad \partial_b P_3=16/165375.
]

The resulting Jacobian and determinant are
[
J=\begin{pmatrix}1/25&0\\9/3500&16/165375\end{pmatrix},
\qquad \det J=16/4134375\ne0.
]
By the inverse function theorem, the mapping \((a,b)\mapsto(P_2,P_3)\) is locally invertible near \((0,0)\), **within this fixed family and sampling model**.

First-order recovery:
[
a=25\Delta P_2+O(\|\Delta P\|^2),\quad
b=\frac{165375}{16}\left(\Delta P_3-\frac9{140}\Delta P_2\right)+O(\|\Delta P\|^2).
]
The small \(\partial_bP_3\) implies potentially poor statistical conditioning. No sample-size certification has been performed.

## Reproduce with exact arithmetic (SymPy)

Run with an **already installed** SymPy; no dependency installation or repository mutation required:

```python
import sympy as S

t, u = S.symbols("t u", nonnegative=True)
r = (1-t)*u
A = ((1+t)**2-r**2)**2
B = ((1-t)**2-r**2)**2
h = (A+B)/16
phi = t**2+S.Rational(5,9)*r**2

def E(z):
    z = S.expand(z * 12 * (1-t)**3 * u**2)
    return S.factor(S.integrate(S.integrate(z, (u,0,1)), (t,0,1)))

checks = {
    "Eh": (E(h), S.Rational(1,10)),
    "Eh2": (E(h*h), S.Rational(1,50)),
    "Ephi": (E(phi), S.Rational(13,45)),
    "cov_phi_h": (E(h*phi)-E(h)*E(phi), S.Integer(0)),
    "EAB": (E(A*B), S.Rational(64,525)),
    "EphiAB": (E(phi*A*B), S.Rational(1856,99225)),
    "EA2B2": (E(A*A+B*B), S.Rational(512,105)),
    "EphiA2B2": (E(phi*(A*A+B*B)), S.Rational(11776,6615)),
    "EhAB": (E(h*A*B), S.Rational(32,2205)),
    "EhA2B2": (E(h*(A*A+B*B)), S.Rational(3392,2205)),
}
for name,(actual,expected) in checks.items():
    assert S.simplify(actual-expected) == 0, (name,actual,expected)
def dP3(psi):
    return S.factor(2*S.Rational(1,350) *
       ((E(psi*A*B)+E(psi*(A*A+B*B))/20)/E(A*B) - 3*E(psi)))
assert dP3(h) == S.Rational(9,3500)
assert dP3(phi) == S.Rational(16,165375)
assert S.det(S.Matrix([[S.Rational(1,25),0],
 [dP3(h),dP3(phi)]])) == S.Rational(16,4134375)
print("EXACT_CHAIN_JACOBIAN := PASS")
```

## Audit boundary and open obligations

- The **full metric is presupposed** to define the volume measure. No intrinsic event-generation dynamics is established.
- Dimension is fixed at 4. This calculation does not identify dimension jointly with curvature, nor reconstruct arbitrary metric tensors.
- The two parameters \(a,b\) do not span arbitrary scalar-curvature perturbations. Invertibility is local within the stated conformal family.
- Sampling uncertainty, numerical conditioning, finite-(N) confidence intervals, independent mathematical review, Mac reproducibility, and Lean axiom audit remain **OPEN/NOT_RUN**.
- Next decisive task: calculate a rigorous finite-(N) covariance matrix and estimator condition number for \((P_2,P_3)\); then investigate a third independent observable and separately specified dimension/curvature family.
- Do not merge or elevate this checkpoint to a global spacetime/gravity claim.

**Literature context:** Myrheim–Meyer dimension estimator; Roy, Sinha & Surya, *The Discrete Geometry of a Small Causal Diamond* (arXiv:1212.0631); Rideout–Sorkin classical sequential growth. Novelty has not been established.
