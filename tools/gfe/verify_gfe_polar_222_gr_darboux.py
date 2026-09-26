from __future__ import annotations
import hashlib, json
from pathlib import Path
import sympy as s

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "artifacts/chronos/gfe_axial_222_epsilon0_simple_root_certificate.json"
source_bytes = SOURCE.read_bytes()
source = json.loads(source_bytes)
assert source["schema"] == "chronos.gfe_axial_222_epsilon0_simple_root_certificate.v1"
assert source["scope"]["ell"] == 2 and source["scope"]["overtone"] == 2
assert source["scope"]["epsilon"] == 0
root = source["root_disk"]
assert root["unique_zero_counting_multiplicity"] == 1 and root["simple_root"] is True

x, nu = s.symbols("x nu", positive=True)
psi = s.Function("psi")(x)
f = 1 - 2/x
v_minus = s.factor(f*(2*(nu+1)/x**2 - 6/x**3))
v_plus = s.factor(2*f*(nu**2*(nu+1)*x**3 + 3*nu**2*x**2 + 9*nu*x + 9)/(x**3*(nu*x+3)**2))
sigma = nu*(nu+1)/3
W = s.factor(sigma + 3*f/(x*(nu*x+3)))
def ds(e): return s.expand(f*s.diff(e,x))
def A(e): return s.expand(ds(e)+W*e)
def Ad(e): return s.expand(-ds(e)+W*e)
def Hm(e): return s.expand(-ds(ds(e))+v_minus*e)
def Hp(e): return s.expand(-ds(ds(e))+v_plus*e)
def zero(e): return s.factor(s.cancel(s.together(e))) == 0
flags = {
    "factorization_minus": zero(v_minus-(W**2-ds(W)-sigma**2)),
    "factorization_plus": zero(v_plus-(W**2+ds(W)-sigma**2)),
    "intertwining_forward": zero(A(Hm(psi))-Hp(A(psi))),
    "intertwining_reverse": zero(Ad(Hp(psi))-Hm(Ad(psi))),
    "composition_minus": zero(Ad(A(psi))-Hm(psi)-sigma**2*psi),
    "composition_plus": zero(A(Ad(psi))-Hp(psi)-sigma**2*psi),
}
omega=s.symbols("omega")
u=s.Function("u")(x); v=s.Function("v")(x)
u2=(v_minus-omega**2)*u; v2=(v_minus-omega**2)*v
wr=lambda l,r:s.expand(l*ds(r)-ds(l)*r)
res=s.expand(wr(A(u),A(v))-(omega**2+sigma**2)*wr(u,v))
res=s.expand(res).xreplace({
    s.diff(u,x,2):s.expand(u2/f**2-s.diff(f,x)*s.diff(u,x)/f),
    s.diff(v,x,2):s.expand(v2/f**2-s.diff(f,x)*s.diff(v,x)/f),
})
flags["wronskian_multiplier"] = zero(res)
flags["endpoint_limits"] = (s.simplify(s.limit(W,x,2,dir="+")) == sigma and s.simplify(s.limit(W,x,s.oo)) == sigma)
assert all(flags.values()), flags

center_re, center_im = root["center"]
center = complex(center_re, center_im)
radius = float(root["radius"])
sig = 2.0
dp = abs(center-1j*sig)-radius
dm = abs(center+1j*sig)-radius
hf = abs(sig-1j*center)-radius
inf = abs(sig+1j*center)-radius
inv = dp*dm
assert min(dp,dm,hf,inf,inv) > 0

def canonical(e): return s.sstr(s.factor(s.cancel(s.together(e))))
def digest(x): return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(",",":")).encode()).hexdigest()
formula={"f":canonical(f),"V_minus":canonical(v_minus),"V_plus":canonical(v_plus),"sigma":canonical(sigma),"W":canonical(W)}
identity={"formula_hash":digest(formula),"identity_flags":flags,"wronskian_factor":"omega^2+sigma^2"}
transfer={"source_sha256":hashlib.sha256(source_bytes).hexdigest(),"center":[center_re,center_im],"radius":radius,"sigma_ell2":sig,"distance_to_plus_i_sigma_lower":dp,"distance_to_minus_i_sigma_lower":dm,"horizon_factor_lower":hf,"infinity_factor_lower":inf,"inverse_factor_lower":inv}
record={
  "schema":"chronos.gfe_polar_222_gr_darboux_certificate.v1",
  "date":"2026-09-25",
  "status":"certified_gr_epsilon0_polar_222_root_via_exact_darboux_transfer",
  "scope":{"parity":"polar","ell":2,"m":2,"overtone":2,"epsilon":0.0,"dimensionless_frequency":"Omega=M*omega","branch":"Schwarzschild GR baseline inherited from certified axial 222 root","beta2_polar_correction":False,"unreduced_trace_log_spectrum":False},
  "source_axial_certificate":{"path":str(SOURCE.relative_to(ROOT)),"sha256":hashlib.sha256(source_bytes).hexdigest()},
  "darboux":{"coordinate":"x=r/M","nu":"(ell-1)*(ell+2)/2","sigma":"nu*(nu+1)/3","superpotential":"sigma+3*f/(x*(nu*x+3))","wronskian_transfer":"Wr(Au,Av)=(Omega^2+sigma^2)*Wr(u,v)","identity_flags":flags,"formula_hash":identity["formula_hash"],"identity_hash":digest(identity)},
  "polar_root_at_epsilon_0":{"unique_simple_root":True,"disk_center":[center_re,center_im],"disk_radius":radius,"same_disk_as_axial":True,"multiplicity_preserved":True,"endpoint_conditions_preserved":True,"algebraically_special_points":[[0.0,sig],[0.0,-sig]],"distance_to_plus_i_sigma_lower":dp,"distance_to_minus_i_sigma_lower":dm,"horizon_map_factor_abs_lower":hf,"infinity_map_factor_abs_lower":inf,"inverse_multiplier_abs_lower":inv,"transfer_hash":digest(transfer)},
  "claim_boundary":["This certificate proves only the Schwarzschild GR polar (ell,m,n)=(2,2,2) root at epsilon=0 by exact Darboux transfer from the certified axial root.","It does not derive the relative O(beta^2) polar quadratic action, polar master potential, polar root continuation, or polar frequency derivative.","It does not certify axial-polar splitting for epsilon>0.","The unreduced trace-log spectrum and its additional massive mode remain outside this certificate."]
}
print("GFE_POLAR_222_GR_DARBOUX")
print("SOURCE_SHA256 :=",record["source_axial_certificate"]["sha256"])
print("FORMULA_HASH :=",record["darboux"]["formula_hash"])
print("IDENTITY_HASH :=",record["darboux"]["identity_hash"])
print("TRANSFER_HASH :=",record["polar_root_at_epsilon_0"]["transfer_hash"])
print("ROOT_RADIUS :=",radius)
print("DIST_PLUS_2I_LOWER :=",dp)
print("DIST_MINUS_2I_LOWER :=",dm)
print("INVERSE_MULTIPLIER_LOWER :=",inv)
print("RESULT := CERTIFIED_POLAR_222_GR_ROOT_TRANSFER")
print("CERTIFICATE_JSON :=",json.dumps(record,sort_keys=True,separators=(",",":")))
