#!/usr/bin/env python3
"""Read-only exact audit of PR #1347's flat 4D causal diamond.
Requires existing sympy; no repository access or file writes.
No Lean verification is implied.
"""
import sympy as S
from functools import lru_cache

t, r = S.symbols('t r')
A = ((1+t)**2-r**2)**2
B = ((1-t)**2-r**2)**2
h = (A+B)/16
phi = t**2 + S.Rational(5, 9)*r**2

@lru_cache(None)
def moment(i, j):
    return 12*S.factorial(i)*S.factorial(j+3)/(
        (j+3)*S.factorial(i+j+4))

def E(f):
    # The t >= 0 reduction is valid only after explicitly symmetrizing.
    z = S.Poly(S.expand((f+f.subs(t, -t))/2), t, r)
    return S.factor(sum(c*moment(i,j) for (i,j),c in z.terms()))

def E_independent(f):
    # Different exact algorithm: integrate each r monomial and then t polynomial.
    z = S.Poly(S.expand((f+f.subs(t, -t))/2), t, r)
    result = S.Integer(0)
    for (i,j),coeff in z.terms():
        primitive = S.Poly(S.expand(t**i*(1-t)**(j+3)), t).integrate()
        result += 12*coeff*(primitive.eval(1)-primitive.eval(0))/(j+3)
    return S.factor(result)

assert E(S.Integer(1)) == E_independent(S.Integer(1)) == 1
assert E(h) == S.Rational(1,10)
assert E(phi) == S.Rational(13,45)
assert E(A*B) == E_independent(A*B) == S.Rational(64,525)
assert E(A*A+B*B) == S.Rational(512,105)
assert E(A*A*B) == E_independent(A*A*B) == S.Rational(256,2205)
assert E(B**3) == E_independent(B**3) == S.Rational(256,21)

# Ordered-pair shared-overlap integral; dimensionless conditional interval ratios:
# E[v] = E[w] = 1/20; E[v^2] = E[w^2] = 1/105; E[v*w] = 1/2100.
shared_pair_T = S.factor((S.Rational(6,5)*E(A*A*B)+E(B**3)/50)/2048)
assert shared_pair_T == S.Rational(11,58800)

# Minkowski diamond centered fourth moment and quadratic form identity.
c4 = E((t*t-r*r)**2)/16
assert c4 == S.Rational(1,80)
def squared_interval_mean(U2, UdotD, tau2):
    return S.expand(U2**2 - S.Rational(3,10)*tau2*U2
                    + UdotD**2/5+c4*tau2**2)

# x is an upper vertex of a fork: integrate future-volume B(y)/16 over past(x).
mean_B_past = squared_interval_mean(
    ((3-t)**2-r**2)/4, ((3-t)*(1+t)+r**2)/2,
    (1+t)**2-r**2)
qfork = S.factor((B*B + 2*A*mean_B_past)/256)
q3 = (A*B+(A*A+B*B)/20)/128
q2 = h
assert E(qfork) == S.Rational(1,35)
assert E(q3) == S.Rational(1,350)

# Future conditional expectations of h and phi.
mean_A_future = squared_interval_mean(
    ((3+t)**2-r**2)/4, ((3+t)*(1-t)+r**2)/2,
    (1-t)**2-r**2)
future_h = (mean_A_future+B/20)/16
future_phi = ((t+1)/2)**2 + S.Rational(5,9)*r*r/4 + \
    ((1-t)**2-r*r)*S.Rational(2,90) + \
    ((1-t)**2+S.Rational(5,9)*r*r)/20
assert S.simplify(future_phi-(13*r*r+29*t*t+32*t+29)/90) == 0

def fork_derivative(psi, future_psi):
    return S.factor(S.Rational(6,256)*E(B*B*(psi+2*future_psi-3*E(psi))))

D = S.Matrix([[S.Rational(1,25), 0],
              [S.Rational(9,3500), S.Rational(16,165375)],
              [fork_derivative(h, future_h), fork_derivative(phi, future_phi)]])
assert list(D[2,:]) == [S.Rational(37,1960), S.Rational(8,11025)]

q = [q2, q3, qfork]
means = [E(z) for z in q]
C = S.Matrix(3, 3, lambda i,j: S.factor(E(q[i]*q[j])-means[i]*means[j]))
assert E(qfork*qfork) == E_independent(qfork*qfork)
assert E(qfork*q3) == E_independent(qfork*q3)
Gamma = S.diag(2,3,3)*C*S.diag(2,3,3)
assert Gamma == S.Matrix([
    [S.Rational(1,25),S.Rational(9,3500),S.Rational(37,1960)],
    [S.Rational(9,3500),S.Rational(527,2695000),S.Rational(2111,1617000)],
    [S.Rational(37,1960),S.Rational(2111,1617000),S.Rational(564,48125)]])
J = D[:2,:]
V2 = S.simplify(J.inv()*Gamma[:2,:2]*J.inv().T)
Info3 = S.simplify(D.T*Gamma.inv()*D)
V3 = S.simplify(Info3.inv())
assert V2 == S.diag(S.Integer(25),S.Rational(145563075,45056))
assert V3 == S.diag(S.Integer(25),S.Rational(64865640298725,24848969728))
assert V2[1,1] > V3[1,1]

n = S.symbols('n',integer=True,positive=True)
var3 = S.factor(9*(n-3)*(n-4)/(n*(n-1)*(n-2))*C[1,1]
        +18*(n-3)/(n*(n-1)*(n-2))*(shared_pair_T-S.Rational(1,350)**2)
        +6/(n*(n-1)*(n-2))*S.Rational(1,350)*(1-S.Rational(1,350)))
assert var3 == (527*n*n+4990*n+26355)/(2695000*n*(n-1)*(n-2))

print('PR_HEAD_EXPECTED := abef2b3e61dcb24a3ebb65ad0df7a76f63d4869f')
print('T_EXACT :=',shared_pair_T)
print('FORK_DERIVATIVES :=',D[2,0],D[2,1])
print('GAMMA_EXACT :=',Gamma)
print('INFORMATION_3 :=',Info3)
print('VARIANCE_2 :=',V2)
print('VARIANCE_3 :=',V3)
print('B_VARIANCE_REDUCTION :=',S.factor(1-V3[1,1]/V2[1,1]))
print('FINITE_N_VAR_P3 :=',var3)
print('INDEPENDENT_RATIONAL_INTEGRATIONS := PASS')
print('LEAN_VERIFICATION := NOT_RUN')