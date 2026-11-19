import sympy as s
u,v=s.symbols('u v'); Q=s.Rational
# integrate polynomial over triangular null coordinates
def E(f):
 p=s.Poly(s.expand(f*12*(v-u)**2),u,v)
 return sum(c/Q((i+1)*(i+j+2)) for (i,j),c in p.terms())
t=(u+v)/2;r=(v-u)/2;A=u*v; a=A**2;b=((1-u)*(1-v))**2
G2=20*(a+b)-2;G3=2100*(Q(1,20)*(a*a+b*b)+a*b)-3
# E past x b(y) = a * E over unit rest-frame interval of (1-2*t*T + A*(T²-R²))²+4*r²*R²/3
# calculate moments with fresh formal symbols
z,w=s.symbols('z w'); T=(u+v)/2; R=(v-u)/2; L=u*v
expr=(1-2*z*T+w*L)**2+Q(4,3)*(z*z-w)*R*R
# integrate coefficients separately
p=s.Poly(s.expand(expr),z,w); I=sum(E(c)*z**i*w**j for (i,j),c in p.terms())
I=s.expand(a*I.subs({z:t,w:A})); rev=lambda f:f.subs({u:1-v,v:1-u}, simultaneous=True)
# symmetrized out/in fork probability; rooted probability mean E b²
m=E(b*b); G=s.expand((a*a+b*b+2*I+2*rev(I))/(2*m)-3)
print('m',m,'I',s.factor(I),'means',[E(g) for g in [G2,G3,G]])
Gs=[G2,G3,G]; S=s.Matrix(3,3,lambda i,j:E(Gs[i]*Gs[j])); print('Sigma',S)
# phi temporal and spatial, at fixed coordinate endpoints, normalized density
P=[(t-Q(1,2))**2,r*r]; response=s.Matrix(3,2,lambda i,j:4*E(Gs[i]*P[j])); J=response*s.Matrix([[12,-36],[-6,6]]).inv();print('J',J)
for k in [2,3]:
 B=J[:k,:]; C=S[:k,:k]; V=(B.T*C.inv()*B).inv(); W=V*B.T*C.inv(); print(k,'V',V,'float',V.evalf(),'weights',W)
assert m == Q(1,105)
assert all(E(g)==0 for g in Gs)
assert S == s.Matrix([[4,9,Q(185,28)],[9,Q(527,22),Q(2111,132)],[Q(185,28),Q(2111,132),Q(59597,5280)]])
assert J == s.Matrix([[Q(2,315),-Q(2,105)],[Q(4,315),-Q(2,45)],[Q(1,105),-Q(1,30)]])
assert all(S[:i,:i].det()>0 for i in (1,2,3))
assert W*J==s.eye(2)
assert W*S*W.T==V
assert V[0,0] < Q(73327275,88)/10
print('EXACT_ASSERTIONS := PASS')
print('SCALAR_VARIANCE_REDUCTION_PERCENT', (100*(1-V[0,0]/Q(73327275,88))).evalf(12))
