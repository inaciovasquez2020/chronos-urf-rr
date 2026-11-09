"""Held-out finite mathematical problems with independently executable certificates.

Standard-library only. This module is an *evaluation oracle*, never included
in a model prompt. TRUE means scoped finite result, not a global theorem.
"""
from __future__ import annotations
import hashlib, json, random, math, heapq

FAMILIES=('graph_threshold','gf2_system','cnf_sat','modular_identity','shortest_path')

def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=True)
def sha(x):return hashlib.sha256(canonical(x).encode()).hexdigest()

def _pairs(n):return [(i,j) for i in range(n) for j in range(i+1,n)]
def _matvec(a,x):return [sum(u*v for u,v in zip(row,x))%2 for row in a]
def _dot(x,y):return sum(a*b for a,b in zip(x,y))%2

def _satisfies(clause,assignment):
    return any((assignment[abs(lit)-1]==1) if lit>0 else (assignment[abs(lit)-1]==0) for lit in clause)

def _vectors(n):
    for mask in range(1<<n):yield [(mask>>i)&1 for i in range(n)]

def _edges_to_adj(n,edges,undirected=False):
    adj=[[] for _ in range(n)]
    for e in edges:
        u,v=e[:2]; adj[u].append((v,e[2] if len(e)>2 else 1))
        if undirected:adj[v].append((u,e[2] if len(e)>2 else 1))
    return adj

def _reachable(n,edges,start):
    adj=_edges_to_adj(n,edges); todo=[start];seen={start}
    while todo:
        for v,_ in adj[todo.pop()]:
            if v not in seen:seen.add(v);todo.append(v)
    return seen

def _distances(n,edges,start):
    adj=_edges_to_adj(n,edges);dist=[math.inf]*n;prev=[None]*n;dist[start]=0;h=[(0,start)]
    while h:
        du,u=heapq.heappop(h)
        if du!=dist[u]:continue
        for v,w in adj[u]:
            if du+w<dist[v]:dist[v]=du+w;prev[v]=u;heapq.heappush(h,(dist[v],v))
    return dist,prev

def make_suite(seed_hex: str, per_family=4):
    if not (isinstance(seed_hex,str) and len(seed_hex)>=16 and all(c in '0123456789abcdef' for c in seed_hex.lower())):raise ValueError('seed_hex must have >=16 hex chars')
    if not (2<=per_family<=12 and per_family%2==0):raise ValueError('even per_family 2..12 required')
    rng=random.Random(int(seed_hex,16));out=[]
    for family in FAMILIES:
        for ix in range(per_family):
            positive=ix%2==0
            if family=='graph_threshold':
                n=rng.randint(5,9)
                k=rng.randint(n//2,n-2) if positive else rng.randint(1,(n-2)//2)
                data={'n':n,'k':k}
                task=(f'For EVERY simple undirected graph on vertices 0..{n-1} with minimum degree at least {k}, '
                    f'is it connected? Give TRUE with a component-size proof, or FALSE with an explicit graph counterexample.')
                fmt=('If TRUE, return {"verdict":"TRUE","certificate":{"method":"component_size_bound","min_component":K,'
                     '"two_component_lower_bound":L}} with K=k+1 and L=2*K. If FALSE, return '
                     '{"verdict":"FALSE","counterexample":{"edges":[[u,v],...]}} representing the entire undirected edge set.')
            elif family=='gf2_system':
                n=rng.randint(4,6)
                for attempt in range(1000):
                    a=[[rng.randrange(2) for _ in range(n)] for _ in range(n)]
                    image={tuple(_matvec(a,x)) for x in _vectors(n)}
                    if positive and len(image)>=2:break
                    if not positive and len(image)<2**n:break
                if positive:
                    x=[rng.randrange(2) for _ in range(n)];b=_matvec(a,x)
                else:
                    missing=[y for y in _vectors(n) if tuple(y) not in image];b=rng.choice(missing)
                data={'n':n,'A':a,'b':b}
                task=f'Over GF(2), decide whether A*x=b has a solution, where A={a} and b={b}. Provide a verifiable certificate.'
                fmt=('If SAT: {"verdict":"SAT","certificate":{"x":[0/1,...]}}. '
                     'If UNSAT: {"verdict":"UNSAT","certificate":{"y":[0/1,...]}} '
                     'where y^T A=0 and y^T b=1 in GF(2).')
            elif family=='cnf_sat':
                n=rng.randint(4,5); clauses=[]
                if positive:
                    planted=[rng.randrange(2) for _ in range(n)]
                    for _ in range(rng.randint(11,17)):
                        ids=rng.sample(range(1,n+1),3)
                        for retry in range(20):
                            lits=[v if rng.randrange(2) else -v for v in ids]
                            if _satisfies(lits,planted):break
                        clauses.append(lits)
                else:
                    # All eight 3-clauses over a 3-variable subset: independently UNSAT.
                    ids=rng.sample(range(1,n+1),3)
                    for mask in range(8):clauses.append([v if (mask>>k)&1 else -v for k,v in enumerate(ids)])
                    for _ in range(rng.randint(4,7)):
                        vs=rng.sample(range(1,n+1),3)
                        clauses.append([v if rng.randrange(2) else -v for v in vs])
                    rng.shuffle(clauses)
                data={'n':n,'clauses':clauses}
                task=f'Decide whether this CNF on variables x1..x{n} is satisfiable: {clauses}. A positive literal i means xi, negative means NOT xi.'
                fmt=('If SAT: {"verdict":"SAT","certificate":{"x":[0/1,...]}}. '
                     'If UNSAT: {"verdict":"UNSAT","certificate":{"falsifying_clause_per_assignment":['
                     'index,...]}} with one ZERO-BASED clause index for EACH assignment mask 0..(2^n-1), '
                     'where bit j of mask is x(j+1). Each indexed clause must be false on that assignment.')
            elif family=='modular_identity':
                true=[(6,3),(10,5),(15,5),(21,7),(30,5),(7,7)]
                false=[(8,3),(9,3),(12,5),(15,3),(25,5),(14,3)]
                m,e=rng.choice(true if positive else false)
                assert (all(pow(x,e,m)==x%m for x in range(m))==positive)
                data={'m':m,'exponent':e}
                task=f'Is the universally quantified statement x^{e} = x (mod {m}) true for every residue x=0,...,{m-1}? Give TRUE or a counterexample.'
                fmt=('If TRUE: {"verdict":"TRUE","certificate":{"method":"exhaust_all_residues","count":m}}. '
                     'If FALSE: {"verdict":"FALSE","counterexample":{"x":INTEGER}} with x in [0,m).')
            elif family=='shortest_path':
                n=rng.randint(5,8); edges={}
                if positive:
                    for u in range(n-1):edges[(u,u+1)]=rng.randint(1,8)
                else:
                    split=rng.randint(2,n-2)
                    for u in range(split-1):edges[(u,u+1)]=rng.randint(1,8)
                for _ in range(3*n):
                    u,v=rng.randrange(n),rng.randrange(n)
                    if u==v or ((not positive) and u<split<=v):continue
                    edges.setdefault((u,v),rng.randint(1,9))
                data={'n':n,'edges':[[u,v,w] for (u,v),w in sorted(edges.items())], 'source':0,'target':n-1}
                task=(f'Directed positive-weight graph on vertices 0..{n-1} with weighted edges [u,v,w]={data["edges"]}. '
                      f'Find the shortest path from 0 to {n-1}, or prove unreachable.')
                fmt=('If REACHABLE: {"verdict":"REACHABLE","certificate":{"distance":D,"path":[vertex,...],'
                     '"potentials":[integer,...]}} where potentials[0]=0, potentials[target]=D, '
                     'and potentials[v]<=potentials[u]+w for EACH edge [u,v,w]. '
                     'The path must have total weight D. '
                     'If UNREACHABLE: {"verdict":"UNREACHABLE","certificate":{"closed_set":[vertex,...]}} '
                     'containing source but not target, with no edge exiting that set.')
            else:raise AssertionError(family)
            out.append({'id':f'P{len(out)+1:03d}-{rng.getrandbits(32):08x}','family':family,'data':data,'question':task,'output_contract':fmt})
    rng.shuffle(out)
    return {'schema':'urf-ai-heldout-math/v1','seed_commitment':hashlib.sha256(seed_hex.encode()).hexdigest(),
            'cases':out,'suite_sha256':sha(out)}

def _ints(v,n,low=0,high=1):
    return (type(v)==list and len(v)==n and all(type(x)==int and low<=x<=high for x in v))

def _graph_verify(case,resp):
    n,k=case['data']['n'],case['data']['k']
    expected='TRUE' if 2*(k+1)>n else 'FALSE'
    state=resp.get('verdict')
    if state!=expected:return False, 'wrong universal graph conclusion'
    if state=='TRUE':
        c=resp.get('certificate');want={'method':'component_size_bound','min_component':k+1,'two_component_lower_bound':2*(k+1)}
        return (c==want),'component-size inequality/proof mismatch'
    c=resp.get('counterexample');edges=c.get('edges') if isinstance(c,dict) else None
    if not isinstance(edges,list):return False,'missing graph counterexample'
    adj=[set() for _ in range(n)];seen=set()
    for item in edges:
        if not _ints(item,2,0,n-1) or item[0]>=item[1] or tuple(item) in seen:return False,'invalid graph edge encoding'
        u,v=item;adj[u].add(v);adj[v].add(u);seen.add((u,v))
    if min(map(len,adj))<k:return False,'minimum-degree constraint violated'
    reached={0};q=[0]
    while q:
        for v in adj[q.pop()]:
            if v not in reached:reached.add(v);q.append(v)
    return len(reached)<n, 'graph witness must be disconnected'

def _gf2_verify(case,resp):
    a,b,n=(case['data'][x] for x in ('A','b','n'))
    possible=any(_matvec(a,x)==b for x in _vectors(n))
    expected='SAT' if possible else 'UNSAT'
    if resp.get('verdict')!=expected:return False,'wrong GF(2) consistency claim'
    c=resp.get('certificate')
    if not isinstance(c,dict):return False,'missing GF(2) certificate'
    if possible:
        x=c.get('x');return _ints(x,n) and _matvec(a,x)==b,'A*x must equal b modulo 2'
    y=c.get('y')
    if not _ints(y,n):return False,'left-nullspace witness length or bits invalid'
    return (all(sum(y[i]*a[i][j] for i in range(n))%2==0 for j in range(n)) and _dot(y,b)==1), 'left kernel and contradiction not established'

def _cnf_verify(case,resp):
    data=case['data'];n=data['n'];clauses=data['clauses']
    possible=any(all(_satisfies(c,x) for c in clauses) for x in _vectors(n))
    expected='SAT' if possible else 'UNSAT'
    if resp.get('verdict')!=expected:return False,'wrong SAT/UNSAT conclusion'
    cert=resp.get('certificate')
    if not isinstance(cert,dict):return False,'missing CNF certificate'
    if possible:
        x=cert.get('x');return _ints(x,n) and all(_satisfies(c,x) for c in clauses),'SAT assignment falsifies at least one clause'
    refs=cert.get('falsifying_clause_per_assignment')
    if not _ints(refs,1<<n,0,len(clauses)-1):return False,'UNSAT witness must cover every assignment with one clause index'
    return all(not _satisfies(clauses[refs[mask]],x) for mask,x in enumerate(_vectors(n))),'one assignment not refuted'

def _mod_verify(case,resp):
    m,e=case['data']['m'],case['data']['exponent']
    valid=all(pow(x,e,m)==x%m for x in range(m)); expected='TRUE' if valid else 'FALSE'
    if resp.get('verdict')!=expected:return False,'wrong modular universal claim'
    if valid:return resp.get('certificate')=={'method':'exhaust_all_residues','count':m},'incorrect exhaustive-domain certificate'
    c=resp.get('counterexample');x=c.get('x') if isinstance(c,dict) else None
    return type(x)==int and 0<=x<m and pow(x,e,m)!=x%m,'invalid modular counterexample'

def _path_verify(case,resp):
    d=case['data'];n=d['n'];edges=d['edges'];dist,_=_distances(n,edges,0);expected='REACHABLE' if dist[-1]<math.inf else 'UNREACHABLE'
    if resp.get('verdict')!=expected:return False,'wrong reachability conclusion'
    c=resp.get('certificate')
    if not isinstance(c,dict):return False,'missing shortest-path certificate'
    if expected=='UNREACHABLE':
        cut=c.get('closed_set')
        if not isinstance(cut,list) or not cut or len(cut)!=len(set(str(x) for x in cut)) or not all(type(x)==int and 0<=x<n for x in cut):return False,'invalid cut'
        s=set(cut)
        return 0 in s and n-1 not in s and all(u not in s or v in s for u,v,w in edges),'cut not closed'
    path=c.get('path');p=c.get('potentials');total=c.get('distance')
    if not isinstance(path,list) or not path or not all(type(x)==int and 0<=x<n for x in path) or path[0]!=0 or path[-1]!=n-1:return False,'invalid shortest path endpoints'
    if type(total)!=int or total<0 or not _ints(p,n,-10**7,10**7) or p[0]!=0 or p[-1]!=total:return False,'dual witness invalid'
    if not all(p[v]<=p[u]+w for u,v,w in edges):return False,'edge-dual inequality fails'
    lookup={(u,v):w for u,v,w in edges}
    if any((u,v) not in lookup for u,v in zip(path,path[1:])):return False,'non-edge in path'
    length=sum(lookup[u,v] for u,v in zip(path,path[1:]))
    return length==total,'primal path does not match dual distance'

CHECKS={'graph_threshold':_graph_verify,'gf2_system':_gf2_verify,'cnf_sat':_cnf_verify,
        'modular_identity':_mod_verify,'shortest_path':_path_verify}

def expected_verdict(case):
    d=case['data'];fam=case['family']
    if fam=='graph_threshold':return 'TRUE' if 2*(d['k']+1)>d['n'] else 'FALSE'
    if fam=='gf2_system':return 'SAT' if any(_matvec(d['A'],x)==d['b'] for x in _vectors(d['n'])) else 'UNSAT'
    if fam=='cnf_sat':return 'SAT' if any(all(_satisfies(c,x) for c in d['clauses']) for x in _vectors(d['n'])) else 'UNSAT'
    if fam=='modular_identity':return 'TRUE' if all(pow(x,d['exponent'],d['m'])==x%d['m'] for x in range(d['m'])) else 'FALSE'
    if fam=='shortest_path':return 'REACHABLE' if _distances(d['n'],d['edges'],0)[0][-1]<math.inf else 'UNREACHABLE'
    raise ValueError('unknown family')

# Only the declared finite certificate fields are authorized.  Mathematical
# verification of a subset of fields is not permission to assert unrelated
# theorems in the same certificate envelope.
CERTIFICATE_FIELDS = {
    'graph_threshold': {
        'TRUE': ('certificate', frozenset({'method','min_component','two_component_lower_bound'})),
        'FALSE': ('counterexample', frozenset({'edges'}))},
    'gf2_system': {
        'SAT': ('certificate', frozenset({'x'})),
        'UNSAT': ('certificate', frozenset({'y'}))},
    'cnf_sat': {
        'SAT': ('certificate', frozenset({'x'})),
        'UNSAT': ('certificate', frozenset({'falsifying_clause_per_assignment'}))},
    'modular_identity': {
        'TRUE': ('certificate', frozenset({'method','count'})),
        'FALSE': ('counterexample', frozenset({'x'}))},
    'shortest_path': {
        'REACHABLE': ('certificate', frozenset({'distance','path','potentials'})),
        'UNREACHABLE': ('certificate', frozenset({'closed_set'}))},
}

def certificate_schema_valid(case,response):
    spec = CERTIFICATE_FIELDS.get(case['family'],{}).get(response.get('verdict'))
    return (spec is not None and isinstance(response.get(spec[0]),dict)
            and set(response[spec[0]]) == spec[1])

def grade(case,response):
    start_v=('TRUE','SAT','REACHABLE')
    neg_v=('FALSE','UNSAT','UNREACHABLE')
    if not isinstance(response,dict):return {'verified':False,'conclusive':False,'unsupported_claim':False,'factual_false':False,'counterexample_detected':False,'reason':'invalid JSON object'}
    verdict=response.get('verdict'); conclusive=verdict in start_v+neg_v
    expected=expected_verdict(case)
    allowed=({'verdict','certificate'} if verdict in ('TRUE','SAT','REACHABLE','UNSAT','UNREACHABLE')
             else {'verdict','counterexample'} if verdict=='FALSE' else {'verdict'})
    if set(response)!=allowed:
        return {'verified':False,'conclusive':conclusive,'unsupported_claim':conclusive,
                'factual_false':bool(conclusive and verdict!=expected),'counterexample_detected':False,'reason':'unexpected or missing top-level fields'}
    if verdict=='UNKNOWN':return {'verified':False,'conclusive':False,'unsupported_claim':False,'factual_false':False,'counterexample_detected':False,'reason':'abstention'}
    if not conclusive:return {'verified':False,'conclusive':False,'unsupported_claim':False,'factual_false':False,'counterexample_detected':False,'reason':'invalid verdict'}
    if not certificate_schema_valid(case,response):
        return {'verified':False,'conclusive':True,'unsupported_claim':True,
                'factual_false':verdict!=expected,'counterexample_detected':False,
                'reason':'unexpected or missing nested certificate fields'}
    try:
        ok,reason=CHECKS[case['family']](case,response)
    except (ValueError,TypeError,KeyError,IndexError,OverflowError,AttributeError) as e:
        ok,reason=False,'malformed certificate: '+type(e).__name__
    # A factual false conclusion is distinct from a true conclusion with a forged/invalid certificate.
    return {'verified':bool(ok),'conclusive':conclusive,'unsupported_claim':conclusive and not ok,
            'factual_false':verdict!=expected,'counterexample_detected':bool(ok and expected in neg_v),
            'reason':('CERTIFICATE_ACCEPTED' if ok else reason), 'expected_class_hidden_in_model_input':expected}

def reference(case):
    """Independent constructive certificates for ORACLE SELF-TEST ONLY (never sent to models)."""
    d=case['data'];f=case['family']
    if f=='graph_threshold':
        n,k=d['n'],d['k']
        if 2*(k+1)>n:return {'verdict':'TRUE','certificate':{'method':'component_size_bound','min_component':k+1,'two_component_lower_bound':2*(k+1)}}
        cut=k+1;edges=[[u,v] for u,v in _pairs(cut)]+[[u+cut,v+cut] for u,v in _pairs(n-cut)]
        return {'verdict':'FALSE','counterexample':{'edges':edges}}
    if f=='gf2_system':
        n,a,b=d['n'],d['A'],d['b']
        for x in _vectors(n):
            if _matvec(a,x)==b:return {'verdict':'SAT','certificate':{'x':x}}
        for y in _vectors(n):
            if all(sum(y[i]*a[i][j] for i in range(n))%2==0 for j in range(n)) and _dot(y,b)==1:return {'verdict':'UNSAT','certificate':{'y':y}}
        raise AssertionError('Farkas GF2 witness missing')
    if f=='cnf_sat':
        n,clauses=d['n'],d['clauses']
        for x in _vectors(n):
            if all(_satisfies(c,x) for c in clauses):return {'verdict':'SAT','certificate':{'x':x}}
        refs=[next(i for i,c in enumerate(clauses) if not _satisfies(c,x)) for x in _vectors(n)]
        return {'verdict':'UNSAT','certificate':{'falsifying_clause_per_assignment':refs}}
    if f=='modular_identity':
        m,e=d['m'],d['exponent']
        for x in range(m):
            if pow(x,e,m)!=x%m:return {'verdict':'FALSE','counterexample':{'x':x}}
        return {'verdict':'TRUE','certificate':{'method':'exhaust_all_residues','count':m}}
    if f=='shortest_path':
        n,edges=d['n'],d['edges'];dist,prev=_distances(n,edges,0)
        if dist[-1]==math.inf:return {'verdict':'UNREACHABLE','certificate':{'closed_set':sorted(_reachable(n,edges,0))}}
        target=n-1; path=[];u=target
        while u is not None:path.append(u);u=prev[u]
        path.reverse();large=max(x for x in dist if x<math.inf)+max((x[2] for x in edges),default=1)*n+10
        p=[int(x) if x<math.inf else int(large) for x in dist]
        return {'verdict':'REACHABLE','certificate':{'distance':int(dist[-1]),'path':path,'potentials':p}}
    raise ValueError(f)
