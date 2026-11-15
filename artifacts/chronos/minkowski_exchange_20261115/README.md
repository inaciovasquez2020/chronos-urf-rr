# Minkowski prefix exchange and endpoint certificates

**Evidence status:** FINITE COMPUTATION_PASS, stated finite identities have independent mathematical arguments; **random-ensemble collision decay OPEN**. Not Lean verified; no asymptotic numerical claims elevated to proof.

**Provenance:** Research scripts and historical execution receipts from the 2026-11-14/15 discussion. The execution receipts were produced before GitHub upload; they are archived evidence, not GitHub Actions receipts, independent mathematical review, or proof-kernel certificates. Five scripts were independently rerun in an isolated Python environment during this integration. Only these five scripts and their five receipts are included here. Earlier n<=9 certificates are already preserved under `artifacts/chronos/minkowski_prefix_20261114/`.

## Models and exact identities

Fix a finite poset P with n>=2 and let e(P) be its number of linear extensions. A uniform permutation pi encodes the 2D order i<_P j iff i<j and pi[i]<pi[j]. For each minimal a, p_a=e(P-a)/e(P), C^+(P)=sum_a p_a^2, and A(P)=Pr(L_1<_P L_2 | P), where L is a uniform linear extension. The published Fishburn/Chan-Pak minimal-element correlation inequality implies A(P)<=(n*C^+(P)-1)/(n-1)<=C^+(P).

### Exchange bijection

For distinct minimal a,y define U(a)={z:a<_P z}. Let
alpha_{ay}=Pr_{L~UnifExt(P-a)}[y occurs before every z in U(a)\\U(y)],
beta_{ay}=Pr_{L~UnifExt(P-y)}[a occurs before every z in U(y)\\U(a)].
Replacing y by a in the alpha-selected extensions of P-a gives a bijection to the beta-selected extensions of P-y. Thus p_a/p_y=beta_{ay}/alpha_{ay}. Hence
p_a <= 1/(1+S_P(a)), S_P(a)=sum_{y minimal,y!=a} alpha_{ay}.
For A=L_1 (randomly first in the uniformly chosen extension),
C(P)=E[p_A|P] <= E[1/(1+S_P(A))|P].
Therefore E[C(P_n)] <= 1/(1+T_n) + Pr(S_{P_n}(L_1)<T_n), for any T_n>0. This remains **CONDITIONAL**, because no sequence T_n -> infinity with the required probability bound is established.

### Endpoint and reverse-order identities

For distinct minimal a and maximal b, r_ab=Pr(L_1=a,L_n=b)=e(P-{a,b})/e(P). Joint collision J(P)=sum_{a,b}r_ab^2. There is no universal sign for J-C^+C^-; exact n=4 permutation witnesses occur in the script. Chain(L) ordinal-summed with Antichain(m) has C^+=1, C^-=J=1/m. Consequently J->0 is insufficient for one-ended collision decay. Reversing extensions maps uniform extension law on P to uniform extension law on the dual P*, so E[C^+(P_n)]=E[C^-(P_n)] for the time-reflection-invariant random permutation ensemble. No endpoint independence is asserted.

### Geometric inputs

For n random points in a 1+1D Alexandrov rectangle, sorted by first null coordinate, the i-th element is a record minimum in the second coordinate with probability 1/i. Conditional on that event, its second coordinate has Beta(1,i) law and the number of its successors among the following N=n-i points has beta-binomial probability
Pr(K_i=k | record at i) = binom(N,k) * i * B(i+k,N-k+1), mean N*i/(i+1).
An exact finite-poset inequality for minimal a with s=|{z:a<_P z}| is p_a <= (s+1)/n; the accompanying script exhaustively checks this for permutation orders through n=8. It is not a machine-checked general-poset proof.

The following unconditional random-permutation rank estimate is a mathematical consequence of these two ingredients:
Pr(L_1 has first-null-coordinate rank i) <= (n-i)/(n*(i+1)) + 1/(n*i).
This bounds selection of the final k ranks by k(k+1)/n^2 for 1<=k<=n/2 (a loose bound). It does **not** establish C_n->0.

Separately, since the first selected event must be minimal, for t in [0,1]:
Pr(U_* V_* >= t) <= n(1-t)^(n-1).
This is localization, not delocalization of first-position weights.

## Certificate inventory and reproduction

- `chronos_exchange_identity_audit.py`: exhaustive ordered minimal-element exchange checks n=2..6, exact Fraction/integer arithmetic, 3782 ordered-pair checks.
- `chronos_two_ended_collision_audit.py`: exact joint endpoint count, sign classification for all permutation orders n=2..7; both signs realized at n=4.
- `chronos_two_ended_ordinal_sum_counterexample.py`: exact chain-below-antichain and dual examples.
- `chronos_record_successor_law.py`: exact beta-binomial record-successor law, 35 position distributions through n=8.
- `chronos_successor_first_position_bound.py`: inequality p_a <= (s+1)/n over 46,232 permutation orders and 124,754 minimal-element cases, through n=8.

Standard-library Python, no downloads needed. Run from this directory:
```sh
for f in chronos_exchange_identity_audit.py chronos_two_ended_collision_audit.py chronos_two_ended_ordinal_sum_counterexample.py chronos_record_successor_law.py chronos_successor_first_position_bound.py; do python3 -B "$f" || exit 1; done
```

**OPEN:** Establish or refute E[C(P_n)]->0, equivalently max_a p_a->0 in probability, for uniform random 2D permutation orders; establish A(P_n)->0 separately if collision route fails. No 4D sprinkling or full emergent-spacetime theorem has been proved.

**Gate notes:** Verified remote branch provenance is not an audit of the user's authoritative Mac working tree. A CI-green certificate-only merge is maintenance/evidence preservation, not a mathematical breakthrough in the OPEN collision question.
