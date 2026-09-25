import math, cmath, json, time
INF=math.inf
BITS=96
S=1<<BITS
def up(x): return math.nextafter(float(x), INF)
def dn(x): return math.nextafter(float(x), -INF)
def au_complex(z): return up(abs(z.real)+abs(z.imag))
def lo_complex(z): return dn(max(abs(z.real),abs(z.imag)))
def ulp_guard(x):
    x=float(x)
    return max(abs(math.nextafter(x,INF)-x),abs(x-math.nextafter(x,-INF)),2.0**-1074)
def rnd_div(num,den):
    return (2*num+den)//(2*den) if num>=0 else -((2*(-num)+den)//(2*den))
def ceil_div(num,den): return (num+den-1)//den

class A2:
    __slots__=("cr","ci","l1r","l1i","l2r","l2i","r")
    def __init__(self,c=0j,l1=0j,l2=0j,r=0.0):
        if isinstance(c,A2):
            for k in self.__slots__: setattr(self,k,getattr(c,k))
            return
        c=complex(c); l1=complex(l1); l2=complex(l2)
        vals=[]; err=0.0
        for x in (c.real,c.imag,l1.real,l1.imag,l2.real,l2.imag):
            k=round(x*S); vals.append(int(k))
            err=up(err+abs(x-k/S)+2*ulp_guard(x))
        rr=up(float(r)+err)
        rad=max(0,math.ceil(up(rr*S)))+6
        self.cr,self.ci,self.l1r,self.l1i,self.l2r,self.l2i,self.r=(*vals,rad)
    @classmethod
    def raw(cls,*args):
        o=object.__new__(cls)
        for k,v in zip(cls.__slots__,args): setattr(o,k,int(v))
        return o
    @staticmethod
    def co(x): return x if isinstance(x,A2) else A2(x)
    def center(self): return complex(self.cr/S,self.ci/S)
    def l1(self): return complex(self.l1r/S,self.l1i/S)
    def l2(self): return complex(self.l2r/S,self.l2i/S)
    def rem(self): return up(self.r/S)
    def lin1_upper(self): return up((abs(self.l1r)+abs(self.l1i))/S)
    def lin2_upper(self): return up((abs(self.l2r)+abs(self.l2i))/S)
    def dev(self): return up((abs(self.l1r)+abs(self.l1i)+abs(self.l2r)+abs(self.l2i)+self.r)/S)
    def au(self): return up((abs(self.cr)+abs(self.ci)+abs(self.l1r)+abs(self.l1i)+abs(self.l2r)+abs(self.l2i)+self.r)/S)
    def center_lower(self): return dn(max(abs(self.cr),abs(self.ci))/S)
    def l1_lower(self): return dn(max(abs(self.l1r),abs(self.l1i))/S)
    def __add__(self,o):
        o=A2.co(o)
        return A2.raw(self.cr+o.cr,self.ci+o.ci,self.l1r+o.l1r,self.l1i+o.l1i,self.l2r+o.l2r,self.l2i+o.l2i,self.r+o.r)
    __radd__=__add__
    def __neg__(self): return A2.raw(-self.cr,-self.ci,-self.l1r,-self.l1i,-self.l2r,-self.l2i,self.r)
    def __sub__(self,o): return self+(-A2.co(o))
    def __rsub__(self,o): return A2.co(o)-self
    def __mul__(self,o):
        o=A2.co(o)
        # center
        rn=self.cr*o.cr-self.ci*o.ci; inn=self.cr*o.ci+self.ci*o.cr
        cr=rnd_div(rn,S); ci=rnd_div(inn,S)
        ec=abs(rn-cr*S)+abs(inn-ci*S)
        # linear1
        lrn=self.cr*o.l1r-self.ci*o.l1i+o.cr*self.l1r-o.ci*self.l1i
        lin=self.cr*o.l1i+self.ci*o.l1r+o.cr*self.l1i+o.ci*self.l1r
        l1r=rnd_div(lrn,S); l1i=rnd_div(lin,S); e1=abs(lrn-l1r*S)+abs(lin-l1i*S)
        # linear2
        lrn2=self.cr*o.l2r-self.ci*o.l2i+o.cr*self.l2r-o.ci*self.l2i
        lin2=self.cr*o.l2i+self.ci*o.l2r+o.cr*self.l2i+o.ci*self.l2r
        l2r=rnd_div(lrn2,S); l2i=rnd_div(lin2,S); e2=abs(lrn2-l2r*S)+abs(lin2-l2i*S)
        ca=abs(self.cr)+abs(self.ci); oa=abs(o.cr)+abs(o.ci)
        l1a=abs(self.l1r)+abs(self.l1i); ol1a=abs(o.l1r)+abs(o.l1i)
        l2a=abs(self.l2r)+abs(self.l2i); ol2a=abs(o.l2r)+abs(o.l2i)
        # all products of linear deviations contribute remainder
        cross=(ca*o.r+oa*self.r+
               l1a*ol1a+l1a*ol2a+l2a*ol1a+l2a*ol2a+
               (l1a+l2a)*o.r+(ol1a+ol2a)*self.r+self.r*o.r)
        rad=ceil_div(cross+ec+e1+e2,S)+8
        return A2.raw(cr,ci,l1r,l1i,l2r,l2i,rad)
    __rmul__=__mul__
    def inv(self):
        c=self.center(); low=lo_complex(c); dev=self.dev()
        if not low>dev: raise AssertionError(("inv",low,dev,c,self.rem()))
        ic=1/c; l1=-(self.l1())/(c*c); l2=-(self.l2())/(c*c)
        rem=up(self.rem()/(low*low)+dev*dev/(low*low*dn(low-dev)))
        rem=up(rem+64*max(ulp_guard(ic.real),ulp_guard(ic.imag),ulp_guard(l1.real),ulp_guard(l1.imag),ulp_guard(l2.real),ulp_guard(l2.imag)))
        return A2(ic,l1,l2,rem)
    def __truediv__(self,o): return self*A2.co(o).inv()
    def __rtruediv__(self,o): return A2.co(o)/self
    def __pow__(self,n):
        if n<0: return self.inv()**(-n)
        out=A2(1); b=self
        while n:
            if n&1: out=out*b
            b=b*b; n//=2
        return out
    def scale(self,q):
        q=complex(q)
        return self*A2(q,0j,0j,32*max(ulp_guard(q.real),ulp_guard(q.imag)))

# parameters
OMEGA0=complex(0.34671099687810465,-0.27391487535351058)
SLOPE=complex(0.0196971854,-0.0671226649)
EC=5e-5; DE=5e-5
RROOT=5e-6
OMID=OMEGA0+SLOPE*EC
O=A2(OMID, RROOT+0j, SLOPE*DE, 0)
E=A2(EC,0j,DE+0j,0)
OABS=O.au()


# Precomputed exact polynomial terms for the shifted-horizon cleared recurrence.
# Each term is [Omega_power, epsilon_power, rational_coefficient].
POLYDATA = {"A":[[[0,0,"0"]],[[0,0,"0"]],[[0,1,"-736/9"],[0,0,"256"]],[[0,1,"-3536/9"],[0,0,"1024"]],[[0,1,"-5384/9"],[0,0,"1792"]],[[0,1,"-1400/3"],[0,0,"1792"]],[[0,1,"-1960/9"],[0,0,"1120"]],[[0,1,"-560/9"],[0,0,"448"]],[[0,1,"-10"],[0,0,"112"]],[[0,1,"-25/36"],[0,0,"16"]],[[0,0,"1"]]],"B":[[[0,0,"0"]],[[0,1,"-736/9"],[0,0,"256"]],[[0,1,"-3664/9"],[0,0,"896"]],[[0,1,"-3448/9"],[0,0,"1344"]],[[0,1,"-1750/9"],[0,0,"1120"]],[[0,1,"-70"],[0,0,"560"]],[[0,1,"-245/18"],[0,0,"168"]],[[0,1,"-10/9"],[0,0,"28"]],[[0,0,"2"]],[[0,0,"0"]],[[0,0,"0"]]],"C":[[[2,1,"-3200/9"],[2,0,"1024"]],[[2,1,"-1088"],[2,0,"5120"],[0,1,"2312/3"],[0,0,"-384"]],[[2,1,"-2176"],[2,0,"11520"],[0,1,"-1852"],[0,0,"-1536"]],[[2,1,"-8896/3"],[2,0,"15360"],[0,1,"2000/3"],[0,0,"-2592"]],[[2,1,"-2544"],[2,0,"13440"],[0,1,"1375/3"],[0,0,"-2400"]],[[2,1,"-1368"],[2,0,"8064"],[0,1,"180"],[0,0,"-1320"]],[[2,1,"-1400/3"],[2,0,"3360"],[0,1,"455/12"],[0,0,"-432"]],[[2,1,"-100"],[2,0,"960"],[0,1,"10/3"],[0,0,"-78"]],[[2,1,"-25/2"],[2,0,"180"],[0,0,"-6"]],[[2,1,"-25/36"],[2,0,"20"]],[[2,0,"1"]]]}

def rat(s):
    if "/" in s:
        a,b=s.split("/",1)
        return float(int(a)/int(b))
    return float(int(s))

def eval_terms(terms):
    out=A2(0)
    for po,pe,coef in terms:
        out += (O**po)*(E**pe)*rat(coef)
    return out

AcA=[eval_terms(t) for t in POLYDATA["A"]]
BcA=[eval_terms(t) for t in POLYDATA["B"]]
CcA=[eval_terms(t) for t in POLYDATA["C"]]
alpha=O.scale(-2j)+E*O.scale(1j/36)
RMAJ=1/8
aa=[A2(1)]
finite=[1.0]
for n in range(1,40):
    an=alpha+A2(n)
    den=AcA[2]*an*(an-A2(1))+BcA[1]*an+CcA[0]
    low=A2(0)
    for lag in range(1,min(10,n)+1):
        k=n-lag
        ak=alpha+A2(k)
        tr=A2(0)
        if lag+2<=10: tr += AcA[lag+2]*ak*(ak-A2(1))
        if lag+1<=10: tr += BcA[lag+1]*ak
        tr += CcA[lag]
        low += tr*aa[k]
    nxt=-low/den
    aa.append(nxt)
    finite.append(up(nxt.au()*RMAJ**n))

def poly_abs_bound_terms(terms,ob,eb):
    res=0.0
    for po,pe,coef in terms:
        res += abs(rat(coef))*(ob**po)*(eb**pe)
    return up(res)

OB=up(OABS)
IMB=up(abs(OMID.imag)+RROOT+abs(SLOPE.imag)*DE)
EB=1e-4
AB=[poly_abs_bound_terms(t,OB,EB) for t in POLYDATA["A"]]
BB=[poly_abs_bound_terms(t,OB,EB) for t in POLYDATA["B"]]
CB=[poly_abs_bound_terms(t,OB,EB) for t in POLYDATA["C"]]
ab=up(OB*(2+EB/36))
zmin=dn(2-5*EB/72)
n0=40
num=0.0
for lag in range(1,11):
    av=AB[lag+2] if lag+2<=10 else 0
    bv=BB[lag+1] if lag+1<=10 else 0
    cv=CB[lag]
    term=av*(1+ab/n0)*(1+(1+ab)/n0)+bv*(1+ab/n0)/n0+cv/n0**2
    num=up(num+RMAJ**lag*term)
den=dn(zmin**10/144*(36-(144+2*EB)*IMB/n0))
qmaj=up(num/den)

# series utilities for A2
def zero_series(n): return [A2(0) for _ in range(n)]
def conv(a,b,n):
    out=zero_series(n)
    for i in range(min(n,len(a))):
        for j in range(min(n-i,len(b))):
            out[i+j]=out[i+j]+a[i]*b[j]
    return out
def addser(a,b,n): return [(a[i] if i<len(a) else A2(0))+(b[i] if i<len(b) else A2(0)) for i in range(n)]
def negser(a): return [-x for x in a]
def subser(a,b,n): return addser(a,negser(b),n)
def scaleser(a,q,n):
    return [(a[i] if i<len(a) else A2(0)).scale(q) for i in range(n)]
def invlin(c,n):
    c=float(c); return [A2(((-1.)**k)/c**(k+1)) for k in range(n)]
def polyz(c,n,k=1):
    # series (c+t)^k
    return [A2(math.comb(k,j)*c**(k-j) if j<=k else 0) for j in range(n)]

# horizon endpoint from aa first 32
N_H=32; X0=1/16; RATIO=X0/RMAJ
tail=up(RATIO**(N_H+1)/(1-RATIO))
dtail=up((1/RMAJ)*RATIO**N_H*((N_H+1)-N_H*RATIO)/(1-RATIO)**2)
sv=A2(0); sd=A2(0)
for n,co in enumerate(aa[:N_H+1]):
    sv += co.scale(X0**n)
    if n: sd += co.scale(n*X0**(n-1))
sv.r += math.ceil(up(tail*S))+8
sd.r += math.ceil(up(dtail*S))+8
L=sd/sv

def h_de_series_eps(c,n):
    xi=invlin(c,n); xi2=conv(xi,xi,n); xi3=conv(xi2,xi,n); z0=c+2
    zm={k:invlin(z0,n) for k in [1]} # not powers
    # get z^-k via conv
    zinv=invlin(z0,n)
    zpow={1:zinv}
    for k in range(2,10): zpow[k]=conv(zpow[k-1],zinv,n)
    zpos={k:polyz(z0,n,k) for k in [1,2,3,4]}
    one=[A2(1)]+[A2(0)]*(n-1)
    f=subser(one,scaleser(zpow[1],2,n),n)
    fp=scaleser(zpow[2],2,n)
    invf=conv(zpos[1],xi,n); invf2=conv(zpos[2],xi2,n); invf3=conv(zpos[3],xi3,n)
    P1=addser(addser(scaleser(zpow[6],12,n),scaleser(zpow[7],-176/9,n),n),scaleser(zpow[2],-5/36,n),n)
    P1p=addser(addser(scaleser(zpow[7],-72,n),scaleser(zpow[8],1232/9,n),n),scaleser(zpow[3],5/18,n),n)
    F1=addser(addser(scaleser(zpow[6],24,n),scaleser(zpow[7],-392/9,n),n),scaleser(zpow[2],-5/36,n),n)
    V0=subser(scaleser(zpow[2],6,n),scaleser(zpow[3],6,n),n)
    V0p=addser(scaleser(zpow[3],-12,n),scaleser(zpow[4],18,n),n)
    num=addser(subser(scaleser(one,653,n),scaleser(zpos[1],281,n),n),scaleser(zpos[4],4,n),n)
    # multiply 4 z^4 by O^2
    num = addser(subser(scaleser(one,653,n),scaleser(zpos[1],281,n),n), scaleser(zpos[4], O*O*4, n),n)
    dV=scaleser(conv(num,zpow[9],n),-8,n)
    V1=subser(dV,scaleser(V0p,5/72,n),n)
    C0=subser([O*O]+[A2(0)]*(n-1),conv(f,V0,n),n)
    C1=negser(addser(conv(F1,V0,n),conv(f,V1,n),n))
    a0=O.scale(-2j); a1=O.scale(1j/36); g0=a0*(a0-A2(1)); g1=a1*(a0.scale(2)-A2(1))
    common=subser(conv(P1p,invf,n),conv(conv(P1,fp,n),invf2,n),n)
    dd=addser(addser(scaleser(xi,a0.scale(2),n),conv(fp,invf,n),n),scaleser(addser(scaleser(xi,a1.scale(2),n),common,n),E,n),n)
    e0=addser(scaleser(xi2,g0,n),scaleser(conv(conv(fp,invf,n),xi,n),a0,n),n)
    e0=addser(e0,conv(C0,invf2,n),n)
    e1=addser(scaleser(xi2,g1,n),scaleser(conv(common,xi,n),a0,n),n)
    e1=addser(e1,scaleser(conv(conv(fp,invf,n),xi,n),a1,n),n)
    e1=addser(e1,conv(C1,invf2,n),n)
    e1=subser(e1,scaleser(conv(conv(P1,C0,n),invf3,n),2,n),n)
    return dd,addser(e0,scaleser(e1,E,n),n)

def h_bounds_eps(c,R):
    xlo=dn(c-R); xup=up(c+R); zlo=dn(c+2-R); zup=up(c+2+R)
    assert xlo>0
    invx=up(1/xlo); invz=up(1/zlo)
    f_lo=dn(xlo/zup)
    fpb=up(2*invz**2)
    a0b=up(2*OABS); a1b=up(OABS/36)
    g0b=up(a0b*(a0b+1)); g1b=up(a1b*(2*a0b+1))
    P1b=up(12*invz**6+(176/9)*invz**7+(5/36)*invz**2)
    P1pb=up(72*invz**7+(1232/9)*invz**8+(5/18)*invz**3)
    commonb=up(P1pb/f_lo+P1b*fpb/(f_lo*f_lo))
    F1b=up(24*invz**6+(392/9)*invz**7+(5/36)*invz**2)
    V0b=up(6*invz**2+6*invz**3)
    V0pb=up(12*invz**3+18*invz**4)
    dVb=up(8*(653+281*zup+4*OABS**2*zup**4)*invz**9)
    V1b=up(dVb+(5/72)*V0pb)
    C0b=up(OABS**2+up(xup/zlo)*V0b)
    C1b=up(F1b*V0b+up(xup/zlo)*V1b)
    db=up(2*a0b*invx+fpb/f_lo+EB*(2*a1b*invx+commonb))
    eb=up(g0b*invx**2+a0b*fpb*invx/f_lo+C0b/(f_lo*f_lo)+EB*(
        g1b*invx**2+a0b*commonb*invx+a1b*fpb*invx/f_lo+C1b/(f_lo*f_lo)+2*P1b*C0b/(f_lo**3)))
    return db,eb

def find_bound(y,R,d,e):
    b=up(max(1.,2*y))
    for _ in range(100):
        rhs=up(y+R*up(b*b+d*b+e)); lip=up(R*(2*b+d))
        if rhs<=b and lip<1: return b
        b=up(max(1.25*b,1.05*rhs))
    raise AssertionError(("bound",y,R,b,lip))
def h_step_eps(cur,c,h,order,R):
    ds,es=h_de_series_eps(c,order+1); coeff=[cur]
    for n in range(order):
        src=A2(0)
        for k in range(n+1): src += coeff[k]*coeff[n-k]+ds[k]*coeff[n-k]
        src += es[n]
        coeff.append(src.scale(-1/(n+1)))
    out=A2(0); hp=1.
    for co in coeff: out += co.scale(hp); hp*=h
    db,eb=h_bounds_eps(c,R); b=find_bound(cur.au(),R,db,eb)
    rho=abs(h)/R; trunc=up(b*rho**(order+1)/(1-rho)); local=up(out.rem()+trunc)
    clean=A2.raw(out.cr,out.ci,out.l1r,out.l1i,out.l2r,out.l2i,0)
    return clean,local,b,db,eb

def scaleser(a,q,n):
    out=[]
    for i in range(n):
        v=a[i] if i<len(a) else A2(0)
        out.append(v*q if isinstance(q,A2) else v.scale(q))
    return out


def coeff_h_point(x):
    z=x+2
    f=x/z; fp=2/z**2
    P1=12/z**6-(176/9)/z**7-(5/36)/z**2
    P1p=-72/z**7+(1232/9)/z**8+(5/18)/z**3
    F1=24/z**6-(392/9)/z**7-(5/36)/z**2
    V0=6/z**2-6/z**3; V0p=-12/z**3+18/z**4
    dV=(A2(653-281*z)+ (O*O).scale(4*z**4)).scale(-8/z**9)
    V1=dV-A2((5/72)*V0p)
    C0=O*O-A2(f*V0)
    C1=-(A2(F1*V0)+A2(f)*V1)
    a0=O.scale(-2j); a1=O.scale(1j/36)
    g0=a0*(a0-A2(1)); g1=a1*(a0.scale(2)-A2(1))
    common=A2(P1p/f-P1*fp/f**2)
    d=a0.scale(2/x)+A2(fp/f)+E*(a1.scale(2/x)+common)
    e=g0.scale(1/x**2)+a0.scale(fp/(x*f))+C0.scale(1/f**2)+E*(
        g1.scale(1/x**2)+a0*common.scale(1/x)+a1.scale(fp/(x*f))+C1.scale(1/f**2)-(A2(P1)*C0).scale(2/f**3)
    )
    return d,e



class Ball:
    __slots__=("c","r")
    def __init__(self,c=0,r=0): self.c=complex(c); self.r=float(r)
    @staticmethod
    def co(x): return x if isinstance(x,Ball) else Ball(x)
    def au(self): return abs(self.c)+self.r  # Euclidean
    def __add__(self,o): o=Ball.co(o); return Ball(self.c+o.c,self.r+o.r)
    __radd__=__add__
    def __neg__(self): return Ball(-self.c,self.r)
    def __sub__(self,o): return self+(-Ball.co(o))
    def __rsub__(self,o): return Ball.co(o)-self
    def __mul__(self,o):
        o=Ball.co(o); return Ball(self.c*o.c, abs(self.c)*o.r+abs(o.c)*self.r+self.r*o.r)
    __rmul__=__mul__
    def inv(self):
        lo=abs(self.c)-self.r
        if lo<=0: raise AssertionError(("ballinv",self.c,self.r))
        return Ball(1/self.c, self.r/(abs(self.c)*lo))
    def __truediv__(self,o): return self*Ball.co(o).inv()
    def __rtruediv__(self,o): return Ball.co(o)/self
    def __pow__(self,n):
        if n<0:return self.inv()**(-n)
        out=Ball(1);b=self
        while n:
            if n&1: out=out*b
            b=b*b;n//=2
        return out

ORAD=RROOT+au_complex(SLOPE*DE)
def coeff_h_ball(c,h):
    x=Ball(c+h/2,h/2)
    z=x+2
    ob=Ball(OMID,ORAD); eb=Ball(EC,DE)
    f=x/z; fp=2/(z*z)
    P1=12/z**6-(176/9)/z**7-(5/36)/z**2
    P1p=-72/z**7+(1232/9)/z**8+(5/18)/z**3
    F1=24/z**6-(392/9)/z**7-(5/36)/z**2
    V0=6/z**2-6/z**3
    V0p=-12/z**3+18/z**4
    dV=-8*(653-281*z+4*(ob*ob)*z**4)/z**9
    V1=dV-(5/72)*V0p
    C0=ob*ob-f*V0
    C1=-(F1*V0+f*V1)
    a0=-2j*ob; a1=(1j/36)*ob
    g0=a0*(a0-1); g1=a1*(2*a0-1)
    common=P1p/f-P1*fp/(f*f)
    d=2*a0/x+fp/f+eb*(2*a1/x+common)
    e=g0/(x*x)+a0*fp/(x*f)+C0/(f*f)+eb*(g1/(x*x)+a0*common/x+a1*fp/(x*f)+C1/(f*f)-2*P1*C0/(f**3))
    return d,e

def h_growth(cur,Rtot,c,h,bound):
    # center evolution magnitude
    db,_=coeff_h_ball(c,h)
    # center derivative bound using local B bound already
    fbound=up(bound*bound+h_bounds_eps(c,min(4*h,c/16))[0]*bound+h_bounds_eps(c,min(4*h,c/16))[1])
    cdelta=up(h*fbound)
    lin=up(cur.lin1_upper()+cur.lin2_upper())
    growth=up((-2*cur.center()-db.c).real + 2*(lin+Rtot+cdelta)+db.r)
    return growth



def run_h(factor=1,order=14):
    cur=A2.raw(L.cr,L.ci,L.l1r,L.l1i,L.l2r,L.l2i,0); Rtot=L.rem(); xv=X0;steps=0
    maxlocal=0; maxg=-1e9
    while xv<1-1e-15:
        if xv<1/8: h=1/(1024*factor)
        elif xv<1/4: h=1/(512*factor)
        elif xv<1/2: h=1/(256*factor)
        elif xv<7/8: h=1/(512*factor)
        else: h=1/(1024*factor)
        if xv+h>1: h=1-xv
        R=min(4*h,xv/16)
        nxt,local,b,db0,eb0=h_step_eps(cur,xv,h,order,R)
        g=h_growth(cur,Rtot,xv,h,b); maxg=max(maxg,g); maxlocal=max(maxlocal,local)
        Be=up(max(2*Rtot,1e-8))
        for _ in range(64):
            rhs=up(Rtot+h*(max(g,0)*Be+Be*Be))
            if rhs<=Be:break
            Be=up(max(1.25*Be,1.05*rhs))
        else: return None,("boot",xv)
        den=dn(1-g*h)
        if den<=0:return None,("den",xv)
        Rtot=up((Rtot+h*Be*Be)/den+local)
        cur=nxt;xv+=h;steps+=1
    return (cur,Rtot,steps,maxlocal,maxg),None


def qcoef(n):
    base=A2(6 if n==2 else -18 if n==3 else 12 if n==4 else 0)
    if n==5: base += E*(O*O).scale(-32)
    if n==6: base += E*(O*O).scale(64)
    if n==8: base += E.scale(2392)
    if n==9: base += E.scale(-30376/3)
    if n==10: base += E.scale(32128/3)
    return base
def laurent_eps(N):
    c=[A2(0) for _ in range(N+1)]
    for n in range(2,N+1):
        rhs=qcoef(n)
        if n-1>=2: rhs += c[n-1].scale(n-1)
        if n-2>=2: rhs -= c[n-2].scale(2*(n-2))
        if n-7>=2: rhs += E*c[n-7].scale(12*(n-7))
        if n-8>=2: rhs += E*c[n-8].scale(-(176/9)*(n-8))
        sq=A2(0)
        for j in range(2,n-1): sq += c[j]*c[n-j]
        c[n]=(rhs-sq)/O.scale(2j)
    return c
N_J=14
jc=laurent_eps(N_J)
zstart=3+32j; iz=1/zstart
qinf=A2(0); power=1+0j
for n in range(1,N_J+1):
    power*=iz
    if n>=2:qinf += jc[n].scale(power)
rho=1/32
qbound=0.0
for n in range(2,N_J+1):qbound=up(qbound+jc[n].au()*rho**n)
resbound=0.0
for n in range(2,2*N_J+9):
    v=A2(0)
    if n<=N_J: v += O*jc[n].scale(2j)
    if 2<=n-1<=N_J:v -= jc[n-1].scale(n-1)
    if 2<=n-2<=N_J:v += jc[n-2].scale(2*(n-2))
    if 2<=n-7<=N_J:v -= E*jc[n-7].scale(12*(n-7))
    if 2<=n-8<=N_J:v += E*jc[n-8].scale((176/9)*(n-8))
    for j in range(2,N_J+1):
        k=n-j
        if 2<=k<=N_J:v += jc[j]*jc[k]
    v -= qcoef(n)
    resbound=up(resbound+v.au()*rho**n)
pdelta=up(2*rho+EB*(12*rho**6+(176/9)*rho**7))
pinv=up(1/(1-pdelta))
remin=dn(OMID.real-RROOT-abs(SLOPE.real)*DE)
damping=dn(2*remin-2*OABS*pdelta*pinv-2*qbound*pinv)
forcing=up(resbound*pinv)
nonlin=pinv

JOST_TAIL = 1e-9
assert damping > 0.0
assert dn(damping*JOST_TAIL) >= up(forcing+nonlin*JOST_TAIL*JOST_TAIL)
assert up(2*nonlin*JOST_TAIL) < damping


def invz_series_eps(zc,n):
    iz=1/zc
    out=[]
    power=iz
    phase=1+0j
    # coefficient for h^k: i^k / zc^(k+1)
    for k in range(n):
        if k==0: phase=1+0j
        elif k%4==1: phase=1j
        elif k%4==2: phase=-1+0j
        else: phase=-1j
        out.append(A2(phase*power))
        power*=iz
    return out

def inf_series_eps(s0,n):
    zc=3+1j*(32-s0)
    zi=invz_series_eps(zc,n)
    zp={1:zi}
    for k in range(2,11): zp[k]=conv(zp[k-1],zi,n)
    one=[A2(1)]+[A2(0)]*(n-1)
    Pser=addser(one,scaleser(zi,-2,n),n)
    P1=addser(scaleser(zp[6],12,n),scaleser(zp[7],-176/9,n),n)
    Pser=addser(Pser,scaleser(P1,E,n),n)
    Qser=addser(addser(scaleser(zp[2],6,n),scaleser(zp[3],-18,n),n),scaleser(zp[4],12,n),n)
    qe=addser(scaleser(zp[5],O*O*-32,n),scaleser(zp[6],O*O*64,n),n)
    qe=addser(qe,scaleser(zp[8],2392,n),n)
    qe=addser(qe,scaleser(zp[9],-30376/3,n),n)
    qe=addser(qe,scaleser(zp[10],32128/3,n),n)
    Qser=addser(Qser,scaleser(qe,E,n),n)
    return Pser,Qser

def inf_bounds_eps(s0,R):
    T=abs(32-s0); zlo=dn(max(3.0,T)-R); zup=up(3+T+R); zm2=dn(max(1.0,T)-R)
    assert zlo>0 and zm2>0
    inv={k:up(1/zlo**k) for k in range(1,12)}
    P1=up(12*inv[6]+(176/9)*inv[7])
    plo=dn(zm2/zup-EB*P1)
    Q0=up(6*inv[2]+18*inv[3]+12*inv[4])
    Q1=up(32*OABS**2*inv[5]+64*OABS**2*inv[6]+2392*inv[8]+(30376/3)*inv[9]+(32128/3)*inv[10])
    qb=up(Q0+EB*Q1)
    return plo,qb

def find_inf_bound(y,R,plo,qb):
    b=up(max(2*y,.01))
    for _ in range(100):
        rhs=up(y+R*up(qb+2*OABS*b+b*b)/plo)
        lip=up(R*(2*OABS+2*b)/plo)
        if rhs<=b and lip<1:return b
        b=up(max(1.25*b,1.05*rhs))
    raise AssertionError(("ibound",y,R,b,lip))

def inf_step_eps(cur,s0,h,order,R):
    ps,qs=inf_series_eps(s0,order+1); a=[cur]
    for n in range(order):
        sq=A2(0)
        for k in range(n+1):sq += a[k]*a[n-k]
        rhs=sq.scale(1j)-O*a[n].scale(2)-qs[n].scale(1j)
        corr=A2(0)
        for k in range(1,n+1):corr += ps[k]*a[n-k+1].scale(n-k+1)
        a.append((rhs-corr)/ps[0].scale(n+1))
    out=A2(0);hp=1.
    for co in a: out+=co.scale(hp);hp*=h
    plo,qb=inf_bounds_eps(s0,R);b=find_inf_bound(cur.au(),R,plo,qb)
    rho=abs(h)/R;tr=up(b*rho**(order+1)/(1-rho));local=up(out.rem()+tr)
    clean=A2.raw(out.cr,out.ci,out.l1r,out.l1i,out.l2r,out.l2i,0)
    return clean,local,b,plo,qb

def inf_growth(cur,Rtot,s0,h,bound,plo,qb):
    lin=up(cur.lin1_upper()+cur.lin2_upper())
    fbound=up((bound*bound+2*OABS*bound+qb)/plo)
    cdelta=up(h*fbound)
    # ball coefficient on segment
    sm=s0+h/2
    z=Ball(3+1j*(32-sm),h/2)
    ob=Ball(OMID,ORAD); eb=Ball(EC,DE)
    P=1-2/z+eb*(12/z**6-(176/9)/z**7)
    # q center plus parameter variation and existing remainder and center motion
    qball=Ball(cur.center(),up(lin+Rtot+cdelta))
    num=2j*qball-2*ob
    A=num/P
    growth=up(A.c.real+A.r)
    quad=up(1/(abs(P.c)-P.r))
    return growth,quad



def run_inf(order=14):
    cur=A2.raw(qinf.cr,qinf.ci,qinf.l1r,qinf.l1i,qinf.l2r,qinf.l2i,0)
    Rtot=up(qinf.rem()+1e-9)
    s0=0.0;steps=0;maxR=Rtot;maxlocal=0;maxg=-1e9
    while s0<32-1e-15:
        t=32-s0
        if t>16:R=1/4
        elif t>8:R=1/8
        elif t>4:R=1/16
        elif t>2:R=1/32
        elif t>1:R=1/64
        else:R=1/128
        h=R/3
        if s0+h>32:h=32-s0
        nxt,local,b,plo,qb=inf_step_eps(cur,s0,h,order,R)
        g,quad=inf_growth(cur,Rtot,s0,h,b,plo,qb)
        maxg=max(maxg,g);maxlocal=max(maxlocal,local)
        Be=up(max(2*Rtot,1e-8))
        for _ in range(64):
            rhs=up(Rtot+h*(max(g,0)*Be+quad*Be*Be))
            if rhs<=Be:break
            Be=up(max(1.25*Be,1.05*rhs))
        else: return None,("boot",s0,Rtot,g,quad)
        den=dn(1-g*h)
        if den<=0:return None,("den",s0,g,h)
        Rtot=up((Rtot+h*quad*Be*Be)/den+local)
        cur=nxt;s0+=h;steps+=1;maxR=max(maxR,Rtot)
    return (cur,Rtot,steps,maxR,maxlocal,maxg),None



assert qmaj < 1.0, qmaj
assert max(finite) <= 1.0000000001, max(finite)
assert sv.center_lower() > sv.dev()

res_h, err_h = run_h(1, 14)
assert err_h is None, err_h
cur_h, R_h, steps_h, maxlocal_h, maxg_h = res_h

res_i, err_i = run_inf(18)
assert err_i is None, err_i
cur_i, R_i, steps_i, maxRi, maxloc_i, maxg_i = res_i


# Take horizon center shift delta0
delta0=5*EC/72
deltaeta=5*DE/72
cur=cur_h; Rtot=R_h; xbase=1.0
Rloc=1/256
nxt,local,b,db0,eb0=h_step_eps(cur,xbase,delta0,14,Rloc)
g=h_growth(cur,Rtot,xbase,delta0,b)
Be=up(max(2*Rtot,1e-8))
for _ in range(64):
    rhs=up(Rtot+delta0*(max(g,0)*Be+Be*Be))
    if rhs<=Be:break
    Be=up(max(1.25*Be,1.05*rhs))
den=dn(1-g*delta0)
Rshift=up((Rtot+delta0*Be*Be)/den+local)
cur_shift=nxt
xmid=1+delta0

# pointwise derivative F at xmid
dpt,ept=coeff_h_point(xmid)
F=-(cur_shift*cur_shift+dpt*cur_shift+ept)
# Add displacement eta correction to l2 only
corr_l2=F.center()*deltaeta
cur_phys=A2(cur_shift.center(),cur_shift.l1(),cur_shift.l2()+corr_l2,0)
# bound shift nonlinear: parameter variation of F times deltaeta + existing F rem + x-Taylor second order
Fvar=up(F.lin1_upper()+F.lin2_upper()+F.rem()+2*Rshift) # include L error influence crudely
shift_cross=up(deltaeta*Fvar)
# second derivative / Taylor tail crude using local bound around xmid
Rd=1/256
dbd,ebd=h_bounds_eps(xmid,Rd); Bfull=find_bound(cur_shift.au()+Rshift,Rd,dbd,ebd)
rho=deltaeta/Rd
shift_tail=up(Bfull*rho*rho/(1-rho))
Rphys=up(Rshift+shift_cross+shift_tail)


xphys=A2(1+delta0,0,deltaeta,0)
P3=A2(1/3)+E.scale(12/3**6-(176/9)/3**7)
alpha=O.scale(-2j)+E*O.scale(1j/36)
qh_full=P3*(alpha/xphys+cur_phys)-O.scale(1j)
qh_internal=qh_full.rem()
qh_err=up(qh_internal+P3.au()*Rphys)
qh=A2.raw(qh_full.cr,qh_full.ci,qh_full.l1r,qh_full.l1i,qh_full.l2r,qh_full.l2i,0)
qi=cur_i
# mismatch clean coefficients
mm=qh-qi
err=up(abs(mm.center().real)+abs(mm.center().imag)+
       abs(mm.l2().real)+abs(mm.l2().imag)+qh_err+R_i)
linlower=dn(max(abs(mm.l1().real),abs(mm.l1().imag)))
margin=dn(linlower-err)



assert margin > 0.0, ("rouche", linlower, err, margin)
assert 0.0 <= EC-DE and EC+DE <= 1.0e-4 + 1e-18

record = {
    "schema": "chronos.gfe_axial_221_epsilon_continuation_certificate.v1",
    "scope": {
        "branch": "projected massless order-reduced EFT",
        "parity": "axial",
        "ell": 2,
        "m": 2,
        "overtone": 1,
        "parameter": "epsilon=beta^2/M^4",
        "epsilon_interval": [0.0, 1.0e-4],
        "unreduced_trace_log_spectrum": False,
    },
    "root_tube": {
        "predictor_origin": [OMEGA0.real, OMEGA0.imag],
        "predictor_slope": [SLOPE.real, SLOPE.imag],
        "uniform_disk_radius": RROOT,
        "unique_zero_counting_multiplicity_for_each_epsilon": 1,
        "simple_root_for_each_epsilon": True,
    },
    "gates": {
        "horizon_majorant_q_upper": qmaj,
        "horizon_majorant_lt_one": qmaj < 1.0,
        "horizon_remainder_upper": R_h,
        "horizon_steps": steps_h,
        "infinity_damping_lower": damping,
        "infinity_damping_positive": damping > 0.0,
        "infinity_remainder_upper": R_i,
        "infinity_steps": steps_i,
        "mismatch_center": [mm.center().real, mm.center().imag],
        "mismatch_root_linear": [mm.l1().real, mm.l1().imag],
        "mismatch_epsilon_linear": [mm.l2().real, mm.l2().imag],
        "rouche_linear_lower": linlower,
        "rouche_error_upper": err,
        "rouche_margin_lower": margin,
        "rouche_margin_positive": margin > 0.0,
    },
    "claim_boundary": [
        "This certificate proves a uniform axial (2,2,1) root tube only for epsilon in [0,1e-4] in the projected massless order-reduced EFT branch.",
        "It does not certify dOmega_221/depsilon at epsilon=0 as an independently enclosed derivative.",
        "It does not certify the polar sector, axial-polar splitting, or the full unreduced trace-log spectrum.",
        "It does not establish full gravity closure or observational detectability."
    ],
}
print("GFE_AXIAL_221_EPSILON_CONTINUATION_FAST_AFFINE")
print("OMEGA0 :=", OMEGA0.real, OMEGA0.imag)
print("PREDICTOR_SLOPE :=", SLOPE.real, SLOPE.imag)
print("EPSILON_INTERVAL := [0,1e-4]")
print("OMEGA_RADIUS :=", RROOT)
print("HORIZON_MAJORANT_Q :=", qmaj)
print("HORIZON_REMAINDER_UPPER :=", R_h)
print("HORIZON_STEPS :=", steps_h)
print("INFINITY_DAMPING_LOWER :=", damping)
print("INFINITY_REMAINDER_UPPER :=", R_i)
print("INFINITY_STEPS :=", steps_i)
print("MISMATCH_CENTER :=", mm.center().real, mm.center().imag)
print("MISMATCH_ROOT_LINEAR :=", mm.l1().real, mm.l1().imag)
print("MISMATCH_EPSILON_LINEAR :=", mm.l2().real, mm.l2().imag)
print("ROUCHE_LINEAR_LOWER :=", linlower)
print("ROUCHE_ERROR_UPPER :=", err)
print("ROUCHE_MARGIN :=", margin)
print("RESULT := CERTIFIED_UNIFORM_UNIQUE_SIMPLE_ROOT_TUBE")
print("CERTIFICATE_JSON :=", json.dumps(record, sort_keys=True, separators=(",", ":")))
