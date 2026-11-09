"""Exact coefficient extraction from pinned source action; not physical review."""
import hashlib,json,re
from pathlib import Path
from fractions import Fraction as Q
import sympy as s
ROOT=Path(__file__).resolve().parents[2]
SOURCE=ROOT/"artifacts/chronos/gfe_corrected_AEH_half_full_lagrangian.json"
GEN=ROOT/"artifacts/chronos/gfe_corrected_AEH_half_euler_generator.json"
SOURCE_SHA="508ba40f34719d1a9ec1943f092f28e077022369dec58d04cb0ec0407917d7a1"
GEN_SHA="c471ef35cf5ecc569e337d67f4265ba64fe8a6b999485fdff2a613e62ad63004"
M,beta,r,lam,omega=s.symbols("M beta r lam omega")
raw=SOURCE.read_bytes();graw=GEN.read_bytes()
assert hashlib.sha256(raw).hexdigest()==SOURCE_SHA,"source action SHA mismatch"
assert hashlib.sha256(graw).hexdigest()==GEN_SHA,"generator SHA mismatch"
meta=json.loads(graw)
assert meta["source_action_sha256"]==SOURCE_SHA
source=json.loads(raw)
assert source["normalization"]=="L_full=(1/2)L_EH_unit+(5 beta/6)L_Ricci2+beta^2 L_joint"
expr=source["full_lagrangian"].replace("lambda","lam")
jets=set(re.findall(r"h[01]t\d+r\d+",expr))
loc={"M":M,"beta":beta,"r":r,"lam":lam,"omega":omega}
loc.update({name:s.Symbol(name) for name in jets})
L=s.sympify(expr,locals=loc)
x,y,z=loc["h0t0r2"],loc["h1t1r1"],loc["h1t0r1"]
C=s.factor(s.diff(L,x,2)/2)
D=s.factor(s.diff(s.diff(L,x),y))
G=s.factor(s.diff(L,y,2)/2)
F=s.factor(s.diff(L,z,2)/2)
expected_C=-beta*lam*(r-2*M)*(8*M*beta+5*r**3)/(12*r**4)
expected_F=beta*lam*(r-2*M)**2*(lam-2)*(5*r**3-16*M*beta)/(12*r**7)
for actual,target,label in ((C,expected_C,"C"),(D,-2*C,"D"),(G,C,"G"),(F,expected_F,"F")):
    assert s.cancel(actual-target)==0,"source coefficient mismatch "+label
c4=2*C;a3=d3=2*s.I*omega*C;b2=-2*(F+omega**2*G)
det=s.factor(a3*(a3*d3-c4*b2))
expected=s.I*beta**3*lam**3*omega*(r-2*M)**4*(lam-2)*(5*r**3-16*M*beta)*(8*M*beta+5*r**3)**2/(216*r**15)
assert s.cancel(det-expected)==0
spec=s.factor(det.subs({r:3,lam:6,omega:s.I/4})/beta**3)
target=(2*M-3)**4*(8*M*beta+135)**2*(16*M*beta-135)/3**15
assert s.cancel(spec-target)==0
e=meta["descriptor_E"]
loc_e={"M":M,"beta":beta,"r":r,"lam":lam,"omega":omega,"I":s.I}
assert s.cancel(s.sympify(e[4][2],locals=loc_e)-a3)==0
second=s.sympify(e[5][5],locals=loc_e).subs({r:3,lam:6,omega:s.I/4})
derived=(a3*d3-c4*b2).subs({r:3,lam:6,omega:s.I/4})
assert s.cancel(second-derived)==0
Mmax=Q(101,100)
xmax=8*Mmax*Q(1,100)
K=Q(51,50)**4*(405+2*xmax)*(8*Mmax)**2/Q(3**15)
c0=Q(125,729)*Q(49,50)**4
lower=c0-K*Q(1,10000)
assert 0<K<Q(1,100) and lower>0
assert 135-xmax>0 and 135-2*xmax>0
print("SOURCE_ACTION_SHA256 :=",SOURCE_SHA)
print("COEFFICIENTS_FROM_SOURCE := PASS")
print("GENERAL_EXACT_FACTOR := PASS")
print("EXPORTED_DESCRIPTOR_PIVOTS := PASS")
print("SPECIALIZED_EXACT_FACTOR := PASS")
print("NORMALIZED_LOWER_BOUND :=",lower)
print("DOMAIN := real M,beta; |M-1|<=1/100; |beta|<=1/100; beta != 0")
print("BETA_ZERO := DESCRIPTOR_SINGULAR")
print("INDEPENDENT_PHYSICAL_REVIEW := OPEN")
