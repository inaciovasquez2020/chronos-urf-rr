# Chronos: exact dipole operator compression improves the 4D four-event lower bound

**Date:** 2026-11-15. **Status:** PROVED conditional on the previously audited four-event reduction and angular trace decomposition; accompanying standard-library exact-rational test **COMPUTATION_PASS**. Full common-future second moment, exact p_(4,2), Minkowski growing-prefix limit **OPEN**. Lean **NOT_RUN**. Git unchanged.

## 1. Geometry and the angular operator

Let `D={0<t<1, |x|<min(t,1-t)}` be the 4D Minkowski causal diamond with normalized volume measure μ. Write `r=|x|`, `a=t-r`, `b=t+r`, and `W_-(x)=(ab)^2=(t²-r²)²`. Its radial/null-coordinate measure is `12(b-a)^2 da db`; spatial directions are independent and uniform on `S²`.

Set `T f(y)=∫_{x≺y}f(x) dμ(x)`. This is an SO(3)-equivariant Hilbert–Schmidt operator, hence decomposes as `⊕_{ell≥0} (K_ell⊗I_(2ell+1))`. The exact angular harmonic decomposition of the four-point common-future overlap gives

`E[J_+(X,Y)^2]=Σ_{ell≥0}(2ell+1) Tr[(K_ell* K_ell)^2]`.

In particular, `A_0=513/875875` was previously obtained by exact ordered-simplex evaluation. Each `A_ell≥0`. The four-point relation audited in PR #1364 is

`p_(4,2)=3557/42000+(6/5)E[J_+²]`.

## 2. Exact l=1 operator action: Lorentz covariance

For each nonnegative integer m, take the dipole test vector field `F_m(x)=x_spatial,z W_-(x)^m=r_x cos(theta_x) W_-(x)^m`, a pure l=1 harmonic. The causal integral is

`T F_m(y)=∫_{J(0,y)} x_spatial,z (x_μ x^μ)^(2m) dμ(x)`.

Because the integrand is a Lorentz four-vector times a scalar, and the Alexandrov interval is Lorentz covariant, this vector integral must be proportional to `y^μ (y_μ y^μ)^(2m+2)` for timelike y. For `y=(1,0,0,0)`, its time component fixes the constant

`κ_m=E_D[t W_-(x)^m]`.

Consequently the *spatial component* satisfies the exact identity

`T F_m(y)=κ_m y_spatial,z W_-(y)^(m+1)`.

Under the radial/null-coordinate measure,

`κ_m = [6/(4m+5)] [B(2m+1,3)+B(2m+2,3)]`, with `κ_0=1/2`.

Similarly, let

`G_k=E_D[r² W_-^k]=[3/(4k+6)] B(2k+1,5)`, where `G_0=1/10` and `G_2=1/2940`.

The ordinary `cos(theta)` factor contributes the same `1/3` to both quadratic forms and cancels under Gram normalization. Thus the radial l=1 Gram matrix and energy matrix for `m=0,...,d−1` are exactly

`G^(d)_(i,j)=G_(i+j)` and `B^(d)_(i,j)=κ_i κ_j G_(i+j+2)`.

## 3. Rigorous compression of the squared trace

Let `H=K_1* K_1`, a positive trace-class operator on the radial l=1 space, and let `P_d` orthogonally project onto the span of `r W_-^i` (`i=0,...,d−1`). Then the Hilbert–Schmidt compression inequality gives

`Tr(H²)≥Tr((P_d H P_d)²)=Tr([(G^(d))^(-1) B^(d)]²)`.

Therefore

`A_1=3 Tr(H²)≥3 Tr([(G^(d))^(-1)B^(d)]²)`.

The Gram matrix is positive definite because `r W_-^i` are independent in L²(D). All entries are rational: the inequality is a rigorous rational lower bound, not an estimate from sampling.

For one test function (`d=1`),

`A_1≥3[(κ_0² G_2)/G_0]²=3(1/1176)²=1/460992`.

For `d=4`, exact rational elimination yields

`A_1≥2479143939321795794973747723735274570412067/920845740985452604132438573733852461791394000000`

`≈ 0.000002692246734690562`.

Combining with the previously established zero mode and the exact four-point reduction gives the improved **rigorous lower bound**

`p_(4,2) ≥ 3557/42000 + (6/5)[513/875875+A_1_lower]`

`=589777848833410780299619386910909253874295188103/6906343057390894530993289303003893463435455000000`

`≈ 0.08539654690368355`.

In particular `p_(4,2)>0.08539654`, improving the previous lower bound `0.0853933162076...`. The earlier independent certified upper bound `p_(4,2)<0.08543935` remains unchanged. Therefore

**`0.08539654 < p_(4,2) < 0.08543935`.**

For `d=5,6`, exact calculations yield slightly stronger lower bounds `0.08539656971146002` and `0.08539658203065797`, respectively. The quoted d=4 inequality is the smaller auditable rational certificate, not the numerically strongest available.

## 4. Verification and scope

The companion script `chronos_l1_operator_compression_certificate_20261115.py` uses only Python's standard-library `fractions` and `math.factorial`; it independently constructs beta moments, inverts rational matrices, checks the d=1 closed form, and computes monotone bounds through d=6. Execution succeeded. It does not recompute the previously established A0 or four-point reduction from scratch; these are explicit prerequisites.

**What remains OPEN:** the full spectral trace `A_1` (as opposed to a rational lower bound), all higher nonzero traces, the exact `E[J_+²]`, exact `p_(4,2)`, and growing-prefix sampling stability. No Lean kernel verification or repository update was performed.