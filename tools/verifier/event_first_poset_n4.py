"""Exhaustive naturally labeled posets on four elements; no dependencies."""
from itertools import permutations, combinations
from collections import defaultdict, Counter
from hashlib import sha256
N=4
edges=[(i,j) for i in range(N) for j in range(i+1,N)]
perms=list(permutations(range(N)))

def closure(adj):
    adj=list(adj)
    for k in range(N):
        for i in range(N):
            if adj[i]>>k&1:adj[i]|=adj[k]
    return tuple(adj)

def encode(adj,perm):
    ans=0
    for i in range(N):
        for j in range(N):
            if adj[perm[i]]>>perm[j]&1:ans|=1<<(i*N+j)
    return ans

def canonical(adj):return min(encode(adj,p) for p in perms)

def chains(adj):
    f=[1]*N; counts=[]
    for k in range(1,N+1):
        counts.append(sum(f))
        f=[sum(f[i] for i in range(N) if adj[i]>>j&1) for j in range(N)]
    return tuple(counts)

def interval_hist(adj):
    return tuple(sorted(sum(bool(adj[i]>>k&1) and bool(adj[k]>>j&1) for k in range(N)) for i in range(N) for j in range(N) if adj[i]>>j&1))

classes={}
for mask in range(1<<len(edges)):
    raw=[0]*N
    for bit,(i,j) in enumerate(edges):
        if mask>>bit&1:raw[i]|=1<<j
    adj=closure(raw)
    classes.setdefault(canonical(adj),adj)

by_sig=defaultdict(list)
for key,adj in sorted(classes.items()):
    c=chains(adj)
    by_sig[c[1:4]].append((key,adj,c,interval_hist(adj)))

candidates=[]
for signature,items in by_sig.items():
    for i in range(len(items)):
        for j in range(i+1,len(items)):
            if items[i][3]!=items[j][3]: candidates.append((signature,items[i],items[j]))

print('N :=',N)
print('UPPER_TRIANGULAR_EDGE_MASKS :=',1<<len(edges))
print('ISOMORPHISM_CLASSES :=',len(classes))
print('SIGNATURE_COLLISIONS_DIFFERENT_INTERVAL_HISTOGRAM :=',len(candidates))
if candidates:
    # Prefer comparable connected candidates with meaningful C3 and small simple edge count
    candidates.sort(key=lambda v:(v[0][1]==0,-v[0][1],v[0][0],v[1][0],v[2][0]))
    sig,a,b=candidates[0]
    for tag,entry in (('A',a),('B',b)):
        key,adj,counts,hist=entry
        rel=[(i,j) for i in range(N) for j in range(N) if adj[i]>>j&1]
        print(tag+'_RELATIONS :=',rel)
        print(tag+'_CHAINS_C1_TO_C5 :=',counts)
        print(tag+'_INTERVAL_INTERIOR_SIZES :=',hist)
        print(tag+'_CANONICAL_CODE :=',key)
    print('SHARED_C2_C3_C4 :=',sig)
    for tag,entry in (('A',a),('B',b)):
        _,adj,dp,_=entry
        brute=tuple(sum(all((adj[u]>>v)&1 for u,v in combinations(sub,2)) for sub in combinations(range(N),k)) for k in range(1,N+1))
        assert dp==brute,(tag,dp,brute)
        maxima=sum(1 for i in range(N) if adj[i]==0)
        print(tag+'_BRUTE_COUNTS :=',brute)
        print(tag+'_MAXIMAL_ELEMENTS :=',maxima)
    assert sum(x==0 for x in a[1]) != sum(x==0 for x in b[1])
    assert a[2][1:4]==b[2][1:4] and a[3]!=b[3]
    print('WITNESS_VERIFIED := PASS')
else: print('WITNESS_VERIFIED := NO_WITNESS_AT_N5')
print('SCRIPT_SHA256 :=',sha256(open(__file__,'rb').read()).hexdigest())
