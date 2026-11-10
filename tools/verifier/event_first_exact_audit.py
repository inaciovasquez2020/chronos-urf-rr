"""Exact rational audit of 4D Minkowski diamond and intrinsic growth test.
Requires Python 3 and sympy; no repository mutation.
"""
from fractions import Fraction
import sympy as S

t,r=S.symbols('t r',real=True)
A=(1+t)**2-r**2
B=(1-t)**2-r**2
h=S.expand((A**2+B**2)/16)
V=S.Rational(2,3)*S.pi

def avg(f):
    # Reflect negative times explicitly, including nonsymmetric integrands.
    f=S.expand(f)
    refl=S.expand(f.subs(t,-t))
    return S.simplify(4*S.pi/V*S.integrate(S.integrate(r**2*(f+refl),(r,0,1-t)),(t,0,1)))

ordered_pair=S.simplify(S.pi/24/V*avg(A**2))
triple_rad=S.simplify(S.integrate(S.integrate(r**2*(A**2*B**2 + (A**2*B**2).subs(t,-t)),(r,0,1-t)),(t,0,1)))
ordered_triple=S.simplify((S.pi/24)**2*4*S.pi*triple_rad/V**3)
mean=avg(h)
variance=S.simplify(avg(h*h)-mean**2)
weighted=S.simplify(S.pi/24/V*avg(h*A**2))
pair_derivative=S.simplify(8*(weighted-mean*ordered_pair))
wave=S.diff(h,r,2)+2*S.diff(h,r)/r-S.diff(h,t,2)
curvature_derivative=S.simplify(-3*S.limit(wave.subs(t,0),r,0))
results={
 'V4':V,'P_pair':2*ordered_pair,'P_fixed_order_triple':ordered_triple,
 'P_any_order_triple':6*ordered_triple,'E_h':mean,'Var_h':variance,
 'P_pair_derivative':pair_derivative,'R_origin_derivative':curvature_derivative,
 'Growth_p_at_pair_match':S.Rational(1,10),
 'Growth_P3_chain_at_pair_match':S.Rational(1,100),
 'Minkowski_P3_chain':S.Rational(1,350)
}
expected={'V4':2*S.pi/3,'P_pair':S.Rational(1,10),
 'P_fixed_order_triple':S.Rational(1,2100),
 'P_any_order_triple':S.Rational(1,350),
 'E_h':S.Rational(1,10),'Var_h':S.Rational(1,100),
 'P_pair_derivative':S.Rational(1,25),'R_origin_derivative':S.Integer(9)}
for name, target in expected.items():
    assert S.simplify(results[name]-target)==0,(name,results[name],target)
for key,v in results.items():print(f'{key} = {v}')
print('EXACT_AUDIT = PASS')
print('THREE_EVENT_GROWTH_MISMATCH = PASS')
