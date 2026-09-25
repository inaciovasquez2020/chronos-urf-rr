from fractions import Fraction as Q
import math
INF=math.inf
def up(x,n=8):
    x=float(x)
    for _ in range(n): x=math.nextafter(x,INF)
    return x
ORE=Q('0.34671099687810465'); OIM=Q('-0.27391487535351058')
ROOT_R=Q(11,10000000); CAUCHY_O_R=Q(1,25000); CAUCHY_E_R=Q(1,10000)
LAUNCH=Q(1,16); MAJ_R=Q(1,8); N=32
TAIL_S=Q(1,2**32); TAIL_SP=Q(17,2**27)
OMEGA0=complex(float(ORE),float(OIM))

class B:
    __slots__=('c','r')
    def __init__(self,c=0,r=0): self.c=complex(c); self.r=up(r)
    @staticmethod
    def co(x): return x if isinstance(x,B) else B(x)
    @property
    def re(self): return self.c.real
    @property
    def im(self): return self.c.imag
    @property
    def rad(self): return self.r
    def au(self): return up(abs(self.c)+self.r)
    def lo(self): return abs(self.c)-self.r
    def __add__(self,o): o=B.co(o); return B(self.c+o.c,up(self.r+o.r+1e-15))
    __radd__=__add__
    def __neg__(self): return B(-self.c,self.r)
    def __sub__(self,o): return self+(-B.co(o))
    def __rsub__(self,o): return B.co(o)-self
    def __mul__(self,o):
        o=B.co(o); z=self.c*o.c; rr=abs(self.c)*o.r+abs(o.c)*self.r+self.r*o.r+2e-15
        return B(z,up(rr))
    __rmul__=__mul__
    def inv(self):
        a=abs(self.c); lo=a-self.r; assert lo>0,(self.c,self.r)
        return B(1/self.c,up(self.r/(a*lo)+2e-15))
    def __truediv__(self,o): return self*B.co(o).inv()
    def __rtruediv__(self,o): return B.co(o)/self
    def __pow__(self,n):
        if n<0:return self.inv()**(-n)
        out=B(1);b=self
        while n:
            if n&1:out=out*b
            b=b*b;n//=2
        return out

class U:
    __slots__=('v','do','de')
    def __init__(self,v=0,do=0,de=0): self.v=B.co(v);self.do=B.co(do);self.de=B.co(de)
    @staticmethod
    def co(x): return x if isinstance(x,U) else U(x)
    def __add__(self,o): o=U.co(o); return U(self.v+o.v,self.do+o.do,self.de+o.de)
    __radd__=__add__
    def __neg__(self): return U(-self.v,-self.do,-self.de)
    def __sub__(self,o): return self+(-U.co(o))
    def __rsub__(self,o): return U.co(o)-self
    def __mul__(self,o):
        o=U.co(o); return U(self.v*o.v,self.do*o.v+self.v*o.do,self.de*o.v+self.v*o.de)
    __rmul__=__mul__
    def inv(self):
        iv=self.v.inv();iv2=iv*iv;return U(iv,-self.do*iv2,-self.de*iv2)
    def __truediv__(self,o): return self*U.co(o).inv()
    def __rtruediv__(self,o): return U.co(o)/self
    def __pow__(self,n):
        if n<0:return self.inv()**(-n)
        out=U(1);b=self
        while n:
            if n&1:out=out*b
            b=b*b;n//=2
        return out
I=U(B(1j))

def sadd(a,b,N):return [(a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0) for i in range(N)]
def sneg(a):return [-x for x in a]
def ssub(a,b,N):return sadd(a,sneg(b),N)
def smul(a,b,N):
    out=[0 for _ in range(N)]
    for i in range(min(N,len(a))):
        for j in range(min(N-i,len(b))):out[i+j]=out[i+j]+a[i]*b[j]
    return out
def sscale(a,c,N):return [a[i]*c if i<len(a) else 0 for i in range(N)]
def zneg(k,N,coerce):return [coerce(((-1)**n*math.comb(k+n-1,n))/(2**(k+n))) for n in range(N)]
def zpos(k,N,coerce):return [coerce(math.comb(k,n)*2**(k-n)) if n<=k else coerce(0) for n in range(N)]
def horizon_series(N,Omega,eps,coerce):
    one=[coerce(1)]+[coerce(0)]*(N-1);zm={k:zneg(k,N,coerce) for k in [1,2,3,4,6,7,8,9]};zp4=zpos(4,N,coerce)
    f=ssub(one,sscale(zm[1],2,N),N);fp=sscale(zm[2],2,N);fpp=sscale(zm[3],-4,N)
    p1=sadd(sscale(zm[6],12,N),sscale(zm[7],-176/9,N),N);p1s=ssub(p1,sscale(fp,5/72,N),N)
    p1p=sadd(sscale(zm[7],-72,N),sscale(zm[8],1232/9,N),N);p1sp=ssub(p1p,sscale(fpp,5/72,N),N)
    f1=sadd(sscale(zm[6],24,N),sscale(zm[7],-392/9,N),N);f1s=ssub(f1,sscale(fp,5/72,N),N)
    v0=ssub(sscale(zm[2],6,N),sscale(zm[3],6,N),N);v0p=sadd(sscale(zm[3],-12,N),sscale(zm[4],18,N),N)
    num=sadd(ssub(sscale(one,653,N),sscale(zpos(1,N,coerce),281,N),N),sscale(zp4,4*(Omega*Omega),N),N)
    v1=sscale(smul(num,zm[9],N),-8,N);v1s=ssub(v1,sscale(v0p,5/72,N),N)
    A0=smul(f,f,N);A1=sscale(smul(f,p1s,N),2,N);B0=smul(f,fp,N);B1=sadd(smul(p1s,fp,N),smul(f,p1sp,N),N)
    C0=ssub([Omega*Omega]+[coerce(0)]*(N-1),smul(f,v0,N),N);C1=sneg(sadd(smul(f1s,v0,N),smul(f,v1s,N),N))
    return sadd(A0,sscale(A1,eps,N),N),sadd(B0,sscale(B1,eps,N),N),sadd(C0,sscale(C1,eps,N),N)
def recurrence(A,Bb,C,alpha,count,coerce):
    aa=[coerce(1)]
    for n in range(1,count+1):
        den=A[2]*(alpha+n)*(alpha+n-1)+Bb[1]*(alpha+n)+C[0];low=coerce(0)
        for m in range(3,n+3):
            k=n-m+2
            if k>=0:low+=A[m]*(alpha+k)*(alpha+k-1)*aa[k]
        for m in range(2,n+2):
            k=n-m+1
            if k>=0:low+=Bb[m]*(alpha+k)*aa[k]
        for m in range(1,n+1):low+=C[m]*aa[n-m]
        aa.append(-low/den)
    return aa

Olarge=B(OMEGA0,float(CAUCHY_O_R));Elarge=B(0,float(CAUCHY_E_R));Ad,Bd,Cd=horizon_series(42,Olarge,Elarge,B.co);alphaD=-2j*Olarge+(1j/36)*Elarge*Olarge
ad=recurrence(Ad,Bd,Cd,alphaD,39,B.co);maxscaled=1.0
for n,a in enumerate(ad[1:],1):
    sc=up(a.au()*float(MAJ_R)**n);maxscaled=max(maxscaled,sc);assert sc<=1.00000001,(n,sc)

Ou=U(B(OMEGA0,float(ROOT_R)),B(1),B(0));Eu=U(B(0),B(0),B(1));Au,Bu,Cu=horizon_series(N+3,Ou,Eu,U.co);alpha=-2*I*Ou+(1/36)*I*Eu*Ou;aa=recurrence(Au,Bu,Cu,alpha,N,U.co)
xeval=U(B(float(LAUNCH)),B(0),B(5/72));Sv=U();Sp=U()
for n,a in enumerate(aa):
    Sv+=a*(xeval**n)
    if n:Sp+=n*a*(xeval**(n-1))
marginO=float(CAUCHY_O_R-ROOT_R);ce=float(CAUCHY_E_R)
Sv.v.r=up(Sv.v.r+float(TAIL_S));Sv.do.r=up(Sv.do.r+float(TAIL_S)/marginO);Sv.de.r=up(Sv.de.r+float(TAIL_S)/ce)
Sp.v.r=up(Sp.v.r+float(TAIL_SP));Sp.do.r=up(Sp.do.r+float(TAIL_SP)/marginO);Sp.de.r=up(Sp.de.r+float(TAIL_SP)/ce)
assert Sv.v.lo()>0
zfix=33/16;fz=1-2/zfix;P1z=4*(27*zfix-44)/(9*zfix**7);Pfix=U(B(fz),B(0),B(P1z));qhor=Pfix*(alpha/xeval+Sp/Sv)-I*Ou

Oc=U(B(OMEGA0),0,0);Ec=U(0,0,0);A0,B0,C0=horizon_series(N+3,Oc,Ec,U.co);alpha0=-2*I*Oc;ac=recurrence(A0,B0,C0,alpha0,N,U.co);x0=U(B(float(LAUNCH)));S0=U();SP0=U()
for n,a in enumerate(ac):
    S0+=a*(x0**n)
    if n:SP0+=n*a*(x0**(n-1))
S0.v.r=up(S0.v.r+float(TAIL_S));SP0.v.r=up(SP0.v.r+float(TAIL_SP));qhor0=U(B(fz))*(alpha0/x0+SP0/S0)-I*Oc

def qcoef(n,O,E):
    base=U(6 if n==2 else -18 if n==3 else 12 if n==4 else 0)
    if n==5:base+=E*(O*O)*(-32)
    if n==6:base+=E*(O*O)*64
    if n==8:base+=E*2392
    if n==9:base+=E*(-30376/3)
    if n==10:base+=E*(32128/3)
    return base
def lcoeff(N,O,E):
    c=[U() for _ in range(N+1)]
    for n in range(2,N+1):
        rhs=qcoef(n,O,E)
        if n-1>=2:rhs+=c[n-1]*(n-1)
        if n-2>=2:rhs-=c[n-2]*(2*(n-2))
        if n-7>=2:rhs+=E*c[n-7]*(12*(n-7))
        if n-8>=2:rhs+=E*c[n-8]*(-(176/9)*(n-8))
        sq=U()
        for j in range(2,n-1):sq+=c[j]*c[n-j]
        c[n]=(rhs-sq)/(O*(2j))
    return c
NJ=14;ci=lcoeff(NJ,Ou,Eu);zstart=3+32j;iz=1/zstart;qinf=U();power=1+0j
for n in range(1,NJ+1):
    power*=iz
    if n>=2:qinf+=ci[n]*power
Ocau=U(B(OMEGA0,float(CAUCHY_O_R)),0,0);Ecau=U(B(0,float(CAUCHY_E_R)),0,0);cc=lcoeff(NJ,Ocau,Ecau);rho=1/32
qbound=sum(cc[n].v.au()*rho**n for n in range(2,NJ+1))
resbound=0.0
for n in range(2,2*NJ+9):
    v=U()
    if n<=NJ:v+=Ocau*cc[n]*(2j)
    if 2<=n-1<=NJ:v-=cc[n-1]*(n-1)
    if 2<=n-2<=NJ:v+=cc[n-2]*(2*(n-2))
    if 2<=n-7<=NJ:v-=Ecau*cc[n-7]*(12*(n-7))
    if 2<=n-8<=NJ:v+=Ecau*cc[n-8]*((176/9)*(n-8))
    for j in range(2,NJ+1):
        k=n-j
        if 2<=k<=NJ:v+=cc[j]*cc[k]
    v-=qcoef(n,Ocau,Ecau)
    resbound=up(resbound+v.v.au()*rho**n)
pdel=up(2*rho+float(CAUCHY_E_R)*(12*rho**6+(176/9)*rho**7));pinv=up(1/(1-pdel));remin=float(ORE-CAUCHY_O_R);omegaabs=Ocau.v.au();damp=up(2*remin-2*omegaabs*pdel*pinv-2*qbound*pinv);forcing=up(resbound*pinv);nonlin=pinv;jtail=3e-6
assert damp>0 and damp*jtail>=forcing+nonlin*jtail*jtail and 2*nonlin*jtail<damp,(damp,forcing)
qinf.v.r=up(qinf.v.r+jtail);qinf.do.r=up(qinf.do.r+jtail/marginO);qinf.de.r=up(qinf.de.r+jtail/ce)
cc0=lcoeff(NJ,Oc,Ec);qinf0=U();power=1+0j
for n in range(1,NJ+1):
    power*=iz
    if n>=2:qinf0+=cc0[n]*power
qinf0.v.r=up(qinf0.v.r+jtail)

INF=math.inf
def upx(x,n=12):
    x=float(x)
    for _ in range(n): x=math.nextafter(x,INF)
    return x
def dnx(x,n=12):
    x=float(x)
    for _ in range(n): x=math.nextafter(x,-INF)
    return x

class F:
    __slots__=('c','r')
    def __init__(self,c=0j,r=0.0):
        self.c=complex(c); self.r=upx(r,8)
    @staticmethod
    def co(x): return x if isinstance(x,F) else F(x)
    def au(self): return upx(abs(self.c.real)+abs(self.c.imag)+self.r,8)
    def cu(self): return upx(abs(self.c.real)+abs(self.c.imag),8)
    def __add__(self,o):
        o=F.co(o);z=self.c+o.c;e=math.ulp(z.real)+math.ulp(z.imag)
        return F(z,upx(self.r+o.r+e,8))
    __radd__=__add__
    def __neg__(self): return F(-self.c,self.r)
    def __sub__(self,o): return self+(-F.co(o))
    def __rsub__(self,o): return F.co(o)-self
    def __mul__(self,o):
        o=F.co(o);a,b=self.c.real,self.c.imag;c,d=o.c.real,o.c.imag
        p1=a*c;p2=b*d;p3=a*d;p4=b*c;rr=p1-p2;ii=p3+p4
        e=math.ulp(p1)+math.ulp(p2)+math.ulp(rr)+math.ulp(p3)+math.ulp(p4)+math.ulp(ii)
        rad=self.cu()*o.r+o.cu()*self.r+self.r*o.r+e
        return F(complex(rr,ii),upx(rad,8))
    __rmul__=__mul__
    def inv(self):
        a=abs(self.c);lo=dnx(a-self.r,8);assert lo>0,(self.c,self.r)
        ic=1/self.c
        rnd=2*(math.ulp(ic.real)+math.ulp(ic.imag))
        return F(ic,upx(self.r/(a*lo)+rnd,8))
    def __truediv__(self,o): return self*F.co(o).inv()
    def __rtruediv__(self,o): return F.co(o)/self
    def __pow__(self,n):
        if n<0:return self.inv()**(-n)
        out=F(1);b=self
        while n:
            if n&1:out=out*b
            b=b*b;n//=2
        return out
IF=F(1j); O0=F(OMEGA0); OR=float(ROOT_R); Ob=upx(O0.au()+OR)

def coeff_series(c,d,N):
    c=F.co(c);d=F.co(d);iv=1/c;ratio=-d*iv;invp=[F(1)]
    for _ in range(10):invp.append(invp[-1]*iv)
    rp=[F(1)]
    for _ in range(N):rp.append(rp[-1]*ratio)
    zm={k:[invp[k]*rp[n]*math.comb(k+n-1,n) for n in range(N)] for k in range(1,11)}
    f=[(F(1) if n==0 else F())-2*zm[1][n] for n in range(N)]
    p1=[12*zm[6][n]-(176/9)*zm[7][n] for n in range(N)]
    q0s=[6*zm[2][n]-18*zm[3][n]+12*zm[4][n] for n in range(N)]
    OO=O0*O0
    qe=[-32*OO*zm[5][n]+64*OO*zm[6][n]+2392*zm[8][n]-(30376/3)*zm[9][n]+(32128/3)*zm[10][n] for n in range(N)]
    return f,p1,q0s,qe

def coefficient_bounds(c,R):
    z=complex(c.c if isinstance(c,F) else c);cr=z.real;ci=z.imag
    if abs(ci)<1e-30:
        zlo=dnx(cr-R);zup=upx(cr+R);xlo=dnx(cr-2-R);assert zlo>0 and xlo>0
        inv={k:upx(1/zlo**k) for k in range(1,11)};flo=dnx(xlo/zup)
    else:
        T=abs(ci);zlo=dnx(max(abs(cr),T)-R);zup=upx(abs(cr)+T+R);zm2=dnx(max(abs(cr-2),T)-R);assert zlo>0 and zm2>0
        inv={k:upx(1/zlo**k) for k in range(1,11)};flo=dnx(zm2/zup)
    Qb=upx(6*inv[2]+18*inv[3]+12*inv[4]);Qeb=upx(32*Ob*Ob*inv[5]+64*Ob*Ob*inv[6]+2392*inv[8]+(30376/3)*inv[9]+(32128/3)*inv[10])
    return flo,Qb,Qeb,upx(12*inv[6]+(176/9)*inv[7]),upx(1+2*inv[1]),inv[5]

def find_Bq(Y,R,flo,Qb,Oc):
    b=upx(max(.01,2*Y))
    for _ in range(64):
        rhs=upx(Y+R*(Qb+b*b+2*Oc*b)/flo)
        if rhs<=b and R*(2*b+2*Oc)/flo<1:return b
        b=upx(max(1.25*b,1.05*rhs))
    raise AssertionError(('Bq',Y,R,b))

def center_step(q,u,v,c,h,d,N,R):
    f,p1,Q0s,Qe=coeff_series(c,d,N+1);invf=[1/f[0]]
    for n in range(1,N+1):
        x=F()
        for k in range(1,n+1):x+=f[k]*invf[n-k]
        invf.append(-x/f[0])
    qs=[q];us=[u];vs=[v];gz=[];aa=[];bo=[];be=[]
    for n in range(N):
        q2=[]
        for m in range(n+1):
            x=F()
            for j in range(m+1):x+=qs[j]*qs[m-j]
            q2.append(x)
        x=F()
        for k in range(n+1):
            j=n-k;x+=invf[k]*(Q0s[j]-q2[j]-2*IF*O0*qs[j])
        gz.append(x);qs.append(d*x/(n+1));xa=F();xb=F()
        for k in range(n+1):
            j=n-k;xa+=invf[k]*(-2*(qs[j]+(IF*O0 if j==0 else F())));xb+=invf[k]*(-2*IF*qs[j])
        aa.append(xa);bo.append(xb);x=bo[n]
        for k in range(n+1):x+=aa[k]*us[n-k]
        us.append(d*x/(n+1));x=F()
        for k in range(n+1):
            j=n-k;pg=F()
            for a in range(j+1):pg+=p1[a]*gz[j-a]
            x+=invf[k]*(Qe[j]-pg)
        be.append(x);x=be[n]
        for k in range(n+1):x+=aa[k]*vs[n-k]
        vs.append(d*x/(n+1))
    def ev(arr):
        x=F();hp=F(1)
        for z in arr:x+=z*hp;hp*=h
        return x
    nq,nu,nv=ev(qs),ev(us),ev(vs);arq,aru,arv=nq.r,nu.r,nv.r;nq.r=nu.r=nv.r=0.0
    flo,Qb,Qeb,p1b,fup,z5=coefficient_bounds(c,R);Bq=find_Bq(q.au(),R,flo,Qb,O0.au());A=upx(2*(Bq+O0.au())/flo);assert R*A<1
    Bu=upx((u.au()+R*(2*Bq/flo))/(1-R*A));G=upx((Qb+Bq*Bq+2*O0.au()*Bq)/flo);Bv=upx((v.au()+R*(Qeb+p1b*G)/flo)/(1-R*A));rho=abs(h)/R
    tq=upx(Bq*rho**(N+1)/(1-rho)+arq);tu=upx(Bu*rho**(N+1)/(1-rho)+aru);tv=upx(Bv*rho**(N+1)/(1-rho)+arv)
    return nq,nu,nv,(tq,tu,tv),(Bq,Bu,Bv,(flo,Qb,Qeb,p1b,fup,z5))

def step_errors(q,u,v,rq,ru,rv,c,h,d,R,loc,bounds):
    tq,tu,tv=loc;Bq,Bu,Bv,bd=bounds;flo,Qb,Qeb,p1b,fup,z5=bd;G=upx((Qb+Bq*Bq+2*O0.au()*Bq)/flo);qcenter_var=upx(abs(h)*G);be=upx(max(2*rq,1e-16))
    for _ in range(64):
        zmc=F.co(c)+F.co(d)*(h/2);zm=F(zmc.c,abs(h)/2);qd=F(q.c,qcenter_var+be);fd=1-2/zm;a=F.co(d)*(-2*(qd+IF*O0)/fd);mu=upx(a.c.real+a.r);fq=upx(be*be/flo);den=dnx(1-mu*abs(h));assert den>0;rhs=upx((rq+abs(h)*fq)/den)
        if rhs<=be:break
        be=upx(max(1.25*be,1.05*rhs))
    else:raise AssertionError('center q remainder')
    rq2=upx(rhs+tq);qpar=upx((Bu+ru)*OR+be);da=upx(2*(qpar+OR)/flo);muu=upx(mu+da);den=dnx(1-muu*abs(h));assert den>0;fu=upx(da*(Bu+ru)+2*qpar/flo);ru2=upx((ru+abs(h)*fu)/den+tu);qevar=upx(32*fup*z5*(2*Ob*OR+OR*OR));gerr=upx(((2*Bq+qpar+2*Ob)*qpar+2*OR*(Bq+qpar))/flo);db=upx((qevar+p1b*gerr)/flo);fv=upx(da*(Bv+rv)+db);rv2=upx((rv+abs(h)*fv)/den+tv);return rq2,ru2,rv2

def propagate(init,kind):
    q,u,v,rq,ru,rv=init;Nstep=20 if kind=='h' else 12;steps=0
    if kind=='h':
        z=33/16
        while z<3-1e-15:
            x=z-2;h=1/1024 if x<1/8 else 1/512;h=min(h,3-z);R=2.5*h;c=F(z);d=F(1);nq,nu,nv,loc,bounds=center_step(q,u,v,c,h,d,Nstep,R);rq,ru,rv=step_errors(q,u,v,rq,ru,rv,c,h,d,R,loc,bounds);q,u,v=nq,nu,nv;z+=h;steps+=1
    else:
        s=0.0
        while s<32-1e-14:
            t=32-s;R=.25 if t>8 else .125 if t>4 else .0625 if t>2 else .015625 if t>1 else .0078125 if t>.5 else .00390625 if t>.25 else .001953125 if t>.125 else .0009765625 if t>.0625 else .00048828125;h=min(R/4,32-s);c=F(complex(3,t));d=F(-1j);nq,nu,nv,loc,bounds=center_step(q,u,v,c,h,d,Nstep,R);rq,ru,rv=step_errors(q,u,v,rq,ru,rv,c,h,d,R,loc,bounds);q,u,v=nq,nu,nv;s+=h;steps+=1
    return q,u,v,rq,ru,rv,steps

def clean_from_B(b): return F(b.c,0)
hor=(clean_from_B(qhor0.v),clean_from_B(qhor.do),clean_from_B(qhor.de),qhor0.v.r,qhor.do.r,qhor.de.r)
inf=(clean_from_B(qinf0.v),clean_from_B(qinf.do),clean_from_B(qinf.de),qinf0.v.r,qinf.do.r,qinf.de.r)
H=propagate(hor,'h');J=propagate(inf,'i')
Dc=H[1].c-J[1].c;Ec=H[2].c-J[2].c;Dr=upx(H[4]+J[4]);Er=upx(H[5]+J[5]);Dlow=dnx(abs(Dc)-Dr);assert Dlow>0
center=-Ec/Dc;rad=upx(Er/Dlow+abs(Ec)*Dr/(abs(Dc)*Dlow)+1e-14)
print('maxscaled',maxscaled,'damp',damp,'forcing',forcing,'jtail',jtail)
print('H',H[6],H[4],H[5],'J',J[6],J[4],J[5])
print('Domega',Dc,Dr,'low',Dlow)
print('Deps',Ec,Er)
print('DERIV',center,rad,'real_lower',center.real-rad,'imag_upper',center.imag+rad)
import json
real_lower=dnx(center.real-rad)
real_upper=upx(center.real+rad)
imag_lower=dnx(center.imag-rad)
imag_upper=upx(center.imag+rad)
assert real_lower>0.0,(center,rad,real_lower)
assert imag_upper<0.0,(center,rad,imag_upper)
record={
  "schema":"chronos.gfe_axial_221_epsilon0_derivative_certificate.v1",
  "scope":{"branch":"projected massless order-reduced EFT","parity":"axial","ell":2,"m":2,"overtone":1,"parameter":"epsilon=beta^2/M^4","endpoint":"epsilon=0"},
  "root_dependency":{"center":[float(ORE),float(OIM)],"radius":float(ROOT_R),"refinement_required":True},
  "implicit_derivative":{"formula":"dOmega/depsilon=-D_epsilon/D_Omega","center":[center.real,center.imag],"disk_radius":rad,"real_lower_bound":real_lower,"real_upper_bound":real_upper,"imag_lower_bound":imag_lower,"imag_upper_bound":imag_upper,"D_Omega_nonzero":True,"real_part_positive":True,"imag_part_negative":True},
  "gates":{"max_scaled_horizon_coefficient":maxscaled,"infinity_damping_lower":damp,"infinity_forcing_upper":forcing,"jost_tail_radius":jtail,"horizon_steps":H[6],"infinity_steps":J[6],"D_Omega_center":[Dc.real,Dc.imag],"D_Omega_radius":Dr,"D_Omega_lower":Dlow,"D_epsilon_center":[Ec.real,Ec.imag],"D_epsilon_radius":Er},
  "claim_boundary":["This certificate encloses only dOmega_221/depsilon at epsilon=0 in the projected massless order-reduced axial branch.","It does not certify a polar derivative or axial-polar splitting.","It does not certify the full unreduced trace-log spectrum or full gravity closure."],
}
print("GFE_AXIAL_221_EPSILON0_IMPLICIT_DERIVATIVE")
print("ROOT_RADIUS :=",float(ROOT_R))
print("D_OMEGA_CENTER :=",Dc.real,Dc.imag)
print("D_OMEGA_RADIUS :=",Dr)
print("D_OMEGA_LOWER :=",Dlow)
print("D_EPSILON_CENTER :=",Ec.real,Ec.imag)
print("D_EPSILON_RADIUS :=",Er)
print("DERIVATIVE_CENTER :=",center.real,center.imag)
print("DERIVATIVE_RADIUS :=",rad)
print("DERIVATIVE_REAL_LOWER :=",real_lower)
print("DERIVATIVE_IMAG_UPPER :=",imag_upper)
print("RESULT := CERTIFIED_EPSILON0_IMPLICIT_DERIVATIVE")
print("CERTIFICATE_JSON :=",json.dumps(record,sort_keys=True,separators=(",",":")))
