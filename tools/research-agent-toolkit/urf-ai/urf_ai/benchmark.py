"""Structured semantic benchmarks; math facts checked by finite graph algorithms.

This is NOT general natural-language semantic understanding. Unstructured text fails closed.
"""
from __future__ import annotations
import re
from collections import deque
from .evidence import validated_receipt
from .bridge_cases import BRIDGE_CASES, evaluate_bridge_response
from .sat_query_boundary import SAT_QUERY_CASES, evaluate_sat_query_response


def cycle_graph(n: int):
    if not isinstance(n,int) or n < 4: raise ValueError("cycle length at least 4")
    return {i:{(i-1)%n,(i+1)%n} for i in range(n)}

def disjoint_cycles(n: int):
    if n<4: raise ValueError("cycle length at least 4")
    return {i:{((i-1)%n),(i+1)%n} if i<n else {n+((i-n-1)%n), n+((i-n+1)%n)} for i in range(2*n)}

def component_count(g):
    seen=set(); components=0
    for start in g:
        if start in seen: continue
        components+=1; stack=[start]; seen.add(start)
        while stack:
            for y in g[stack.pop()]:
                if y not in seen: seen.add(y);stack.append(y)
    return components

def ball_signature(g,root:int,r:int):
    if root not in g or r<0: raise ValueError("invalid rooted ball")
    dist={root:0};queue=deque([root])
    while queue:
        v=queue.popleft()
        if dist[v] == r: continue
        for w in g[v]:
            if w not in dist: dist[w]=dist[v]+1;queue.append(w)
    ball=set(dist)
    edges=sum(len(g[v]&ball) for v in ball)//2
    deg=sorted(len(g[v]&ball) for v in ball)
    layers=tuple(sorted([d for d in dist.values()]).count(i) for i in range(r+1))
    return len(ball),edges,tuple(deg),layers

def cycle_witness(radius:int,m:int):
    if (type(radius) is not int or type(m) is not int or radius<1 or m<=2*radius+1):
        return False,"radius/length inadmissible"
    if m>40 or radius>16: return False,"resource bound exceeded"
    a=cycle_graph(2*m); b=disjoint_cycles(m)
    if len(a)!=len(b) or component_count(a)!=1 or component_count(b)!=2:
        return False,"global witness invalid"
    sigs_a={ball_signature(a,x,radius) for x in a}
    sigs_b={ball_signature(b,x,radius) for x in b}
    return (len(sigs_a)==1 and sigs_a==sigs_b),"exact finite local signature vs connectivity"

VALID_CASES = {"cycle_locality", "colap_counterexample", "entropy_bridge", "dashboard_not_proof", "conditional_axiom"} | BRIDGE_CASES | SAT_QUERY_CASES

def evaluate_response(response: object, case_id: str) -> dict:
    """Evaluates JSON decisions, not prose token frequency."""
    def fail(reason): return {"case":case_id,"pass":False,"reason":reason}
    if case_id in BRIDGE_CASES: return evaluate_bridge_response(response,case_id)
    if case_id in SAT_QUERY_CASES: return evaluate_sat_query_response(response,case_id)
    if case_id not in VALID_CASES or not isinstance(response,dict): return fail("unknown case or non-structured answer")
    allowed={
        "cycle_locality":{"case_id","status","unproved","witness"},
        "colap_counterexample":{"case_id","status","witness","missing_lemma"},
        "entropy_bridge":{"case_id","status","missing_lemma","evidence_level"},
        "dashboard_not_proof":{"case_id","status","evidence_level"},
        "conditional_axiom":{"case_id","status","evidence_level"},
    }
    if response.get("case_id")!=case_id or set(response)!=allowed[case_id]:
        return fail("schema/identity mismatch")
    if case_id=="cycle_locality":
        if response.get("status")!="REFUTED_AS_STATED" or response.get("unproved") != "GLOBAL_FROM_LOCAL": return fail("invalid global claim status")
        w=response.get("witness")
        if not isinstance(w,dict) or set(w)!={"family","radius","m"} or w.get("family")!="cycle_pair": return fail("missing mathematical witness")
        ok,reason=cycle_witness(w.get("radius"),w.get("m"))
        return {"case":case_id,"pass":ok,"reason":reason}
    if case_id=="colap_counterexample":
        w=response.get("witness")
        if response.get("status")!="REFUTED_AS_STATED" or not isinstance(w,dict): return fail("unrestricted counterexample not classified")
        if set(w)!={"colap_rank","overlap_rank","origin"} or w.get("origin")!="chronos_pr279_record": return fail("counterexample provenance mismatch")
        if w.get("colap_rank")!=0 or w.get("overlap_rank")!=1 or response.get("missing_lemma")!="forall admissible X, overlap(X) <= colap(X)": return fail("false or irrelevant repair")
        return {"case":case_id,"pass":True,"reason":"numeric contradiction + source-bound witness; graph-semantic formal proof NOT checked"}
    if case_id=="entropy_bridge":
        ok = response.get("status")=="OPEN" and response.get("missing_lemma")=="SemanticRankRateToFiberEntropySoundness" and response.get("evidence_level")=="NO_FORMAL_PROOF"
        return {"case":case_id,"pass":ok,"reason":"explicit unresolved proof bridge"}
    if case_id=="dashboard_not_proof":
        ok = response.get("status")=="NOT_THEOREM" and response.get("evidence_level")=="CI_STATUS_ONLY"
        return {"case":case_id,"pass":ok,"reason":"CI scoped to status, not mathematics"}
    if case_id=="conditional_axiom":
        ok = response.get("status")=="CONDITIONAL" and response.get("evidence_level")=="PROJECT_AXIOMS_ACTIVE"
        return {"case":case_id,"pass":ok,"reason":"axiom-dependent proof cannot be unconditional"}

def baseline_keyword_score(candidate: str) -> int:
    """Faithful relevant branch of original 2026-05-14 PR280 rubric, for contrast.
    Only first canonical case, not a substitute for executing original runner.
    """
    normalized=" ".join(candidate.lower().split())
    def has(s):return " ".join(s.lower().split()) in normalized
    forbidden=["P vs NP is solved","Clay problem is solved","Chronos-RR is closed","H4.1/FGL is closed","unconditional graph-theoretic cycle-overlap-rank bound","rigidity closure is proved"]
    if any(has(x) for x in forbidden):return 0
    required=["OPEN_PROBLEM_REQUIRED","restricted","cycleOverlap_le_colap","cycleOverlapRank","colapRank","weakest","open"]
    level=1
    if has("OPEN_PROBLEM_REQUIRED"):level=max(level,2)
    if has("Unrestricted graph-semantic cycle-overlap domination remains open.") or has("remains open"):level=max(level,3)
    if has("For every admissible graph-semantic input X, cycleOverlapRank X <= colapRank X.") or (has("weakest") and has("cycleOverlapRank") and has("colapRank")):level=max(level,4)
    if all(has(x) for x in required):level=max(level,5)
    if level>=5 and all(has(x) for x in ["counterexample","colapRank = 0","cycleOverlapRank = 1"]):level=6
    return level
