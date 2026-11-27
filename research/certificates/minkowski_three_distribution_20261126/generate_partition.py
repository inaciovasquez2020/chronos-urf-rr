from itertools import product, permutations
from fractions import Fraction
from collections import Counter, deque
from pathlib import Path
import sys

out = Path(sys.argv[1])
edges = [(i,j) for i in range(3)
         for j in range(3) if i != j]
points = ["z.1", "z.2.1", "z.2.2"]

def relation(m):
    return {e for k,e in enumerate(edges)
            if (m >> k) & 1}

def mask(R):
    return sum(1 << edges.index(e) for e in R)

def valid(R):
    return (
        not any((j,i) in R for i,j in R)
        and not any(
            (i,k) not in R
            for i,j in R for l,k in R if j == l
        )
    )

patterns = [m for m in range(64)
            if valid(relation(m))]

def classify(m):
    R = relation(m)
    if len(R) == 0:
        return "A"
    if len(R) == 1:
        return "E"
    if len(R) == 3:
        return "C"
    if any(sum(a == i for a,b in R) == 2
           for i in range(3)):
        return "V"
    return "W"

classes = {
    c: [m for m in patterns if classify(m) == c]
    for c in "AEVWC"
}

assert len(patterns) == 19
assert [len(classes[c]) for c in "AEVWC"] == [
    1,6,3,3,6
]

def pred(m,kind):
    R = relation(m)
    if kind == "rot":
        p = (1,2,0)
        return mask({(p[i],p[j]) for i,j in R})
    return mask({(j,i) for i,j in R})

groups = [
    classes["A"],
    classes["E"],
    classes["V"]+classes["W"],
    classes["C"]
]

rep = {}
links = []

for group in groups:
    root = group[0]
    rep[root] = root
    q = deque([root])
    while q:
        m = q.popleft()
        for kind in ("rot","rev"):
            n = pred(m,kind)
            assert n in group
            if n not in rep:
                rep[n] = root
                links.append((n,m,kind))
                q.append(n)

assert len(rep) == 19
assert len(links) == 15

def edge(i,j):
    return f"edge{i}{j}"

def pat(m):
    return f"pattern{m}"

def expr(ms):
    names = [pat(m) for m in ms]
    assert names
    s = names[-1]
    for name in reversed(names[:-1]):
        s = f"({name} ∪ {s})"
    return s

def meas(ms):
    names = [f"hm{m}" for m in ms]
    s = names[-1]
    for name in reversed(names[:-1]):
        s = f"({name}.union {s})"
    return s

def sumexpr(ms):
    return " + ".join(
        f"mass {pat(m)}" for m in ms
    )

events = {
    "all": patterns,
    "pair": [m for m in patterns
             if {(1,2),(2,1)} & relation(m)],
    "fork": [m for m in patterns
             if {(0,1),(0,2)} <= relation(m)],
    "earliest": [
        m for m in patterns
        if {(0,1),(0,2)} <= relation(m)
        and {(1,2),(2,1)} & relation(m)
    ]
}

weights = {
    "A": Fraction(53,70),
    "E": Fraction(11,350),
    "V": Fraction(3,350),
    "W": Fraction(3,350),
    "C": Fraction(1,2100)
}

targets = {
    "all": Fraction(1),
    "pair": Fraction(1,10),
    "fork": Fraction(1,105),
    "earliest": Fraction(1,1050)
}

for k,ms in events.items():
    assert sum(weights[classify(m)] for m in ms) == \
        targets[k]
    print("EXACT_EVENT_CHECK",k,Counter(
        classify(m) for m in ms))

names = {
    "A": "antichainEvent",
    "E": "singlePairEvent",
    "V": "vEvent",
    "W": "invertedVEvent",
    "C": "chainEvent"
}

lines = []

def emit(s=""):
    lines.append(s)

for i,j in edges:
    emit(f"def {edge(i,j)} : Set (Triple E) :=")
    emit(f"  (fun z : Triple E => "
         f"({points[i]},{points[j]})) ⁻¹' causalPair")

for m in patterns:
    terms = []
    for k,(i,j) in enumerate(edges):
        n = edge(i,j)
        terms.append(n if (m >> k)&1
                     else f"{n}ᶜ")
    emit(f"def {pat(m)} : Set (Triple E) :=")
    emit("  "+" ∩ ".join(terms))

for c in "AEVWC":
    emit(f"def {names[c]} : Set (Triple E) :=")
    emit("  "+expr(classes[c]))


# Abstract the finite partition from geometric terms.
logic_names = {
    (i,j): f"p{i}{j}" for i,j in edges
}

def logic_pattern(m):
    terms = [
        logic_names[e] if (m >> k)&1
        else "¬ " + logic_names[e]
        for k,e in enumerate(edges)
    ]
    result = terms[0]
    for term in terms[1:]:
        result = f"({result} ∧ {term})"
    return result

def logic_union(ms):
    terms = [logic_pattern(m) for m in ms]
    result = terms[-1]
    for term in reversed(terms[:-1]):
        result = f"({term} ∨ {result})"
    return result

emit("theorem finite_partition_logic")
emit("    ("+" ".join(logic_names.values())+
     " : Prop)")
for i in range(3):
    for j in range(i+1,3):
        emit(f"    (ha{i}{j} : "
             f"{logic_names[i,j]} → "
             f"¬ {logic_names[j,i]})")
for i,j,k in permutations(range(3)):
    emit(f"    (ht{i}{j}{k} : "
         f"{logic_names[i,j]} → "
         f"{logic_names[j,k]} → "
         f"{logic_names[i,k]})")
emit("    : True ↔ "+logic_union(patterns)+
     " := by")
emit("  classical")
emit("  "+" <;> ".join(
    [f"by_cases h_{n} : {n}" for n in
     logic_names.values()]+["simp_all"]
))
emit()

emit("""
section Final

variable [InnerProductSpace ℝ E]
variable [FiniteDimensional ℝ E]
variable [ProperSpace E]
variable [MeasurableSpace E]
variable [BorelSpace E]

set_option maxHeartbeats 4000000 in
theorem distribution
    (μ : Measure E)
    [μ.IsAddHaarMeasure]
    (hdim : Module.finrank ℝ E = 3) :
""")

for c in "AEVWC":
    prob = weights[c]*len(classes[c])
    tail = " ∧" if c != "C" else " := by"
    emit(f"    ((tripleLaw μ) {names[c]}).toReal"
         f" = {prob.numerator}/{prob.denominator}{tail}")

emit("""
  let ρ := law μ
  let M := tripleLaw μ
  letI : IsProbabilityMeasure ρ :=
    law_probability μ
  letI : IsProbabilityMeasure M := by
    dsimp [M,tripleLaw]
    infer_instance
  let mass : Set (Triple E) → ℝ :=
    fun s => (M s).toReal
  have hrot : Measurable
      (rotate : Triple E → Triple E) := by
    unfold rotate
    fun_prop
  have hrev : Measurable
      (reverseTriple : Triple E → Triple E) := by
    unfold reverseTriple reversePoint
    fun_prop
  have hrotmap : M.map rotate = M :=
    rotate_law μ
  have hrevmap : M.map reverseTriple = M :=
    reverse_triple_law μ hdim
  have hperm
      (f : Triple E → Triple E)
      (hf : Measurable f)
      (hmap : M.map f = M)
      (s t : Set (Triple E))
      (hs : MeasurableSet s)
      (he : f ⁻¹' s = t) :
      mass t = mass s := by
    dsimp [mass]
    rw [← he,← Measure.map_apply hf hs,hmap]
  have hadd
      (s t : Set (Triple E))
      (hd : Disjoint s t)
      (ht : MeasurableSet t) :
      mass (s ∪ t) = mass s + mass t := by
    dsimp [mass]
    rw [measure_union hd ht,
      ENNReal.toReal_add
        (measure_ne_top M s)
        (measure_ne_top M t)]
""")

for i,j in edges:
    e = edge(i,j)
    emit(f"  have hm{e} : MeasurableSet "
         f"({e} (E := E)) := by")
    emit(f"    unfold {e}")
    emit(f"    exact (show Measurable "
         f"(fun z : Triple E => "
         f"({points[i]},{points[j]})) "
         f"by fun_prop) "
         f"causalPair_open.measurableSet")

for m in patterns:
    terms = []
    for k,(i,j) in enumerate(edges):
        h = f"hm{edge(i,j)}"
        terms.append(h if (m>>k)&1
                     else h+".compl")
    proof = terms[0]
    for h in terms[1:]:
        proof = f"({proof}.inter {h})"
    emit(f"  have hm{m} : MeasurableSet "
         f"({pat(m)} (E := E)) := by")
    emit(f"    unfold {pat(m)}")
    emit("    exact "+proof)

base = ", ".join(
    [edge(i,j) for i,j in edges]+[
        "causalPair","Set.mem_preimage",
        "Set.mem_inter_iff","Set.mem_union",
        "Set.mem_compl_iff","Set.mem_setOf_eq"
    ]
)

def simps(ms,extra=""):
    return ", ".join(
        [pat(m) for m in sorted(set(ms))]
        + [base] + ([extra] if extra else [])
    )

for n,m,kind in links:
    fn = "rotate" if kind == "rot" else "reverseTriple"
    hf = "hrot" if kind == "rot" else "hrev"
    mp = "hrotmap" if kind == "rot" else "hrevmap"
    emit(f"  have hs{n} : mass {pat(n)} "
         f"= mass {pat(rep[n])} := by")
    emit(f"    have he : ({fn} : Triple E → Triple E) ⁻¹' "
         f"{pat(m)} = {pat(n)} := by")
    emit("      ext z")
    emit("      simp only ["+
         simps([n,m],
               "rotate, reverseTriple, reverse_precedes")
         +"]")
    emit("      all_goals tauto")
    emit(f"    have h := hperm {fn} {hf} {mp} "
         f"{pat(m)} {pat(n)} hm{m} he")
    if m == rep[m]:
        emit("    exact h")
    else:
        emit(f"    exact h.trans hs{m}")

def order_facts():
    for i in range(3):
        for j in range(i+1,3):
            emit(f"    have ha{i}{j} : "
                 f"precedes {points[i]} {points[j]} → "
                 f"¬ precedes {points[j]} {points[i]} :="
                 f" fun h => precedes_asymmetric h")
    for i,j,k in permutations(range(3)):
        emit(f"    have ht{i}{j}{k} : "
             f"precedes {points[i]} {points[j]} → "
             f"precedes {points[j]} {points[k]} → "
             f"precedes {points[i]} {points[k]} :="
             f" fun h k => precedes_transitive h k")

actual = {
    "all": "(Set.univ : Set (Triple E))",
    "pair": "(edge12 ∪ edge21 : Set (Triple E))",
    "fork": "forkEvent",
    "earliest": "earliestComparable"
}

for k,ms in events.items():
    emit(f"  have hset_{k} : {actual[k]} "
         f"= {expr(ms)} := by")
    emit("    ext z")
    order_facts()
    emit("    simp only ["+
         simps(ms,
          "Set.mem_univ, forkEvent, "
          "earliestComparable, comparable")
         +"]")
    if k == "all":
        args = [
            f"(precedes {points[i]} {points[j]})"
            for i,j in edges
        ]
        args += [
            f"ha{i}{j}"
            for i in range(3)
            for j in range(i+1,3)
        ]
        args += [
            f"ht{i}{j}{k}"
            for i,j,k in permutations(range(3))
        ]
        emit("    exact finite_partition_logic "+
             " ".join(args))
    else:
        emit("    all_goals tauto")

emit("""
  have hactual_all :
      mass (Set.univ : Set (Triple E)) = 1 := by
    dsimp [mass]
    simp
  have hpairset :
      (edge12 ∪ edge21 : Set (Triple E)) =
        Set.univ ×ˢ comparable := by
    ext z
    simp only [edge12,edge21,causalPair,
      comparable,Set.mem_union,Set.mem_preimage,
      Set.mem_setOf_eq,Set.mem_prod,
      Set.mem_univ,true_and]
  have hactual_pair :
      mass (edge12 ∪ edge21) = 1/10 := by
    change
      ((ρ.prod (ρ.prod ρ))
        (edge12 ∪ edge21)).toReal = _
    rw [hpairset,Measure.prod_prod,
      measure_univ,one_mul]
    change
      ((law μ).prod (law μ)
        comparable).toReal = _
    rw [comparable_pair_mass μ hdim,
      ENNReal.toReal_ofReal (by norm_num)]
  have hactual_fork :
      mass forkEvent = 1/105 := by
    change (tripleLaw μ forkEvent).toReal = _
    unfold tripleLaw
    rw [fork_mass μ hdim,
      ENNReal.toReal_ofReal (by norm_num)]
  have hactual_earliest :
      mass earliestComparable = 1/1050 := by
    change
      (tripleLaw μ earliestComparable).toReal = _
    unfold tripleLaw
    rw [earliest_comparable_mass μ hdim,
      ENNReal.toReal_ofReal (by norm_num)]
""")

def union_sum(k,ms):
    emit(f"  have hsum_{k} : mass {expr(ms)} "
         f"= {sumexpr(ms)} := by")
    if len(ms) == 1:
        emit("    rfl")
        return
    for i,m in enumerate(ms[:-1]):
        rest = ms[i+1:]
        emit(f"    rw [hadd {pat(m)} {expr(rest)} (by")
        emit("      rw [Set.disjoint_left]")
        emit("      intro z hz hw")
        emit("      simp only ["+
             simps([m]+rest)+"] at hz hw")
        emit("      all_goals tauto) "+meas(rest)+"]")
    emit("    all_goals ring")

for k,ms in events.items():
    union_sum(k,ms)
    emit(f"  rw [← hset_{k},hactual_{k}] at hsum_{k}")
    hs = [f"hs{m}" for m in ms if rep[m]!=m]
    if hs:
        emit("  simp only ["+", ".join(hs)+
             f"] at hsum_{k}")

equations = ", ".join(
    "hsum_"+k for k in events
)

for c in "AEVWC":
    ms = classes[c]
    union_sum(c,ms)
    prob = weights[c]*len(ms)
    emit(f"  have hresult{c} : mass {names[c]} "
         f"= {prob.numerator}/{prob.denominator} := by")
    emit(f"    change mass {expr(ms)} = _")
    if len(ms)>1:
        emit(f"    rw [hsum_{c}]")
        hs = [f"hs{m}" for m in ms if rep[m]!=m]
        if hs:
            emit("    simp only ["+", ".join(hs)+"]")
    emit(f"    linarith only [{equations}]")

emit("  exact ⟨hresultA,hresultE,hresultV,"
     "hresultW,hresultC⟩")

emit("""
noncomputable def physicalPrefix
    (μ : Measure E) : ℝ :=
  ((tripleLaw μ) singlePairEvent).toReal / 3 +
  ((tripleLaw μ) vEvent).toReal +
  ((tripleLaw μ) chainEvent).toReal

theorem physical_prefix_gap
    (μ : Measure E)
    [μ.IsAddHaarMeasure]
    (hdim : Module.finrank ℝ E = 3) :
    ((law μ).prod (law μ)
      comparable).toReal = 1/10 ∧
    physicalPrefix μ = 16/175 ∧
    ((law μ).prod (law μ)
      comparable).toReal -
      physicalPrefix μ = 3/350 := by
  obtain ⟨_,hE,hV,_,hC⟩ :=
    distribution μ hdim
  have hp :
      ((law μ).prod (law μ)
        comparable).toReal = 1/10 := by
    rw [comparable_pair_mass μ hdim,
      ENNReal.toReal_ofReal (by norm_num)]
  have hq :
      physicalPrefix μ = 16/175 := by
    unfold physicalPrefix
    rw [hE,hV,hC]
    norm_num
  exact ⟨hp,hq,by rw [hp,hq]; norm_num⟩

theorem coherent_prefix_obstruction
    (μ : Measure E)
    [μ.IsAddHaarMeasure]
    (hdim : Module.finrank ℝ E = 3)
    (r : ℝ) :
    (3:ℝ)/350 ≤
      |((law μ).prod (law μ)
        comparable).toReal-r| +
      |r-physicalPrefix μ| := by
  obtain ⟨hp,hq,_⟩ :=
    physical_prefix_gap μ hdim
  rw [hp,hq]
  linarith [le_abs_self ((1:ℝ)/10-r),
    le_abs_self (r-(16:ℝ)/175)]

end Final

#print axioms reverse_precedes
#print axioms precedes_asymmetric
#print axioms reverse_law
#print axioms rotate_law
#print axioms reverse_triple_law
#print axioms distribution
#print axioms physical_prefix_gap
#print axioms coherent_prefix_obstruction

end Chronos.ThreeDistribution
""")


def refactor_partition(src):
    import re
    from itertools import permutations

    keys = ("all","pair","fork","earliest")

    edges = [
        (i,j) for i in range(3)
        for j in range(3) if i != j
    ]

    points = ["z.1","z.2.1","z.2.2"]

    atoms = [f"p{i}{j}" for i,j in edges]

    lhs = {
        "pair": "(p12 ∨ p21)",
        "fork": "(p01 ∧ p02)",
        "earliest":
            "((p01 ∧ p02) ∧ (p12 ∨ p21))"
    }

    def pattern(mask):
        terms = [
            a if (mask >> k)&1 else "¬ " + a
            for k,a in enumerate(atoms)
        ]
        result = terms[0]
        for term in terms[1:]:
            result = f"({result} ∧ {term})"
        return result

    def union(masks):
        terms = [pattern(m) for m in masks]
        result = terms[-1]
        for term in reversed(terms[:-1]):
            result = f"({term} ∨ {result})"
        return result

    start = src.index("  have hset_all :")
    end = src.index("  have hactual_all :",start)

    region = src[start:end]

    blocks = re.split(
        r"(?=^  have hset_)",
        region,
        flags=re.M
    )

    blocks = [b for b in blocks if b.strip()]
    assert len(blocks) == 4

    abstract = []
    geometric = []
    replacements = []
    audits = []

    for key,block in zip(keys,blocks):

        header,*body = block.rstrip().splitlines()

        assert header.startswith(
            f"  have hset_{key} :"
        )

        masks = [
            int(x) for x in
            re.findall(r"\bpattern(\d+)\b",header)
        ]

        assert masks

        if key != "all":
            name = f"finite_partition_logic_{key}"

            proof = [
                "set_option maxHeartbeats 4000000 in",
                f"theorem {name}",
                "    ("+" ".join(atoms)+" : Prop)"
            ]

            for i in range(3):
                for j in range(i+1,3):
                    proof.append(
                        f"    (ha{i}{j} : "
                        f"p{i}{j} → ¬ p{j}{i})"
                    )

            for i,j,k in permutations(range(3)):
                proof.append(
                    f"    (ht{i}{j}{k} : "
                    f"p{i}{j} → p{j}{k} → p{i}{k})"
                )

            proof += [
                f"    : {lhs[key]} ↔ "
                +union(masks)+" := by",
                "  classical",
                "  "+" <;> ".join(
                    [f"by_cases h_{a} : {a}"
                     for a in atoms]+["simp_all"]
                )
            ]

            abstract.append("\n".join(proof))
            audits.append(f"#print axioms {name}")

            args = [
                f"(precedes {points[i]} {points[j]})"
                for i,j in edges
            ]

            args += [
                f"ha{i}{j}"
                for i in range(3)
                for j in range(i+1,3)
            ]

            args += [
                f"ht{i}{j}{k}"
                for i,j,k in permutations(range(3))
            ]

            assert body[-1].strip() == "all_goals tauto"

            body[-1] = (
                "    exact "+name+" "+" ".join(args)
            )

        statement = header.split(" : ",1)[1]

        if key == "fork":
            statement = statement.replace(
                "forkEvent =",
                "(forkEvent : Set (Triple E)) =",
                1
            )

        if key == "earliest":
            statement = statement.replace(
                "earliestComparable =",
                "(earliestComparable : Set (Triple E)) =",
                1
            )

        name = f"partition_set_{key}"

        geometric.append(
            "set_option maxHeartbeats 4000000 in\n"
            +f"theorem {name} : "+statement+"\n"
            +"\n".join(line[2:] for line in body)
        )

        replacements.append(
            f"  have hset_{key} := "
            f"{name} (E := E)"
        )

        audits.append(f"#print axioms {name}")

    src = (
        src[:start]
        +"\n".join(replacements)+"\n"
        +src[end:]
    )

    marker = "\nsection Final\n"

    assert src.count(marker)==1

    src = src.replace(
        marker,
        "\n"+"\n\n".join(abstract)+"\n"+marker,
        1
    )

    marker = (
        "set_option maxHeartbeats 4000000 in\n"
        "theorem distribution"
    )

    assert src.count(marker)==1

    src = src.replace(
        marker,
        "\n\n".join(geometric)+"\n\n"+marker,
        1
    )

    marker = "#print axioms distribution"

    assert src.count(marker)==1

    src = src.replace(
        marker,
        "#print axioms finite_partition_logic\n"
        +"\n".join(audits)+"\n"+marker,
        1
    )

    return src

with out.open("a") as f:
    f.write(refactor_partition("\n".join(lines)+"\n"))

print("DIRECTED_CONFIGURATIONS := 64")
print("STRICT_PARTIAL_ORDERS := 19")
print("SYMMETRY_CLASSES := 4")
print("SYMMETRY_LINKS := 15")
print("EXACT_FINITE_ENUMERATION := PASS")
print("LEAN_SOURCE_GENERATION := PASS")


LINTER_CLEANUP_EDITS = {3360: ('  simp only [pattern0, pattern1, pattern2, pattern3, pattern4, pattern8, pattern10, pattern11, pattern12, pattern14, pattern16, pattern20, pattern28, pattern32, pattern33, pattern35, pattern48, pattern49, pattern52, edge01, edge02, edge10, edge12, edge20, edge21, causalPair, Set.mem_preimage, Set.mem_inter_iff, Set.mem_union, Set.mem_compl_iff, Set.mem_setOf_eq, Set.mem_univ, forkEvent, earliestComparable, comparable]', '  simp only [pattern0, pattern1, pattern2, pattern3, pattern4, pattern8, pattern10, pattern11, pattern12, pattern14, pattern16, pattern20, pattern28, pattern32, pattern33, pattern35, pattern48, pattern49, pattern52, edge01, edge02, edge10, edge12, edge20, edge21, causalPair, Set.mem_preimage, Set.mem_inter_iff, Set.mem_union, Set.mem_compl_iff, Set.mem_setOf_eq, Set.mem_univ]'), 3375: ('  simp only [pattern8, pattern10, pattern11, pattern12, pattern14, pattern28, pattern32, pattern33, pattern35, pattern48, pattern49, pattern52, edge01, edge02, edge10, edge12, edge20, edge21, causalPair, Set.mem_preimage, Set.mem_inter_iff, Set.mem_union, Set.mem_compl_iff, Set.mem_setOf_eq, Set.mem_univ, forkEvent, earliestComparable, comparable]', '  simp only [pattern8, pattern10, pattern11, pattern12, pattern14, pattern28, pattern32, pattern33, pattern35, pattern48, pattern49, pattern52, edge01, edge02, edge10, edge12, edge20, edge21, causalPair, Set.mem_preimage, Set.mem_inter_iff, Set.mem_union, Set.mem_compl_iff, Set.mem_setOf_eq]'), 3390: ('  simp only [pattern3, pattern11, pattern35, edge01, edge02, edge10, edge12, edge20, edge21, causalPair, Set.mem_preimage, Set.mem_inter_iff, Set.mem_union, Set.mem_compl_iff, Set.mem_setOf_eq, Set.mem_univ, forkEvent, earliestComparable, comparable]', '  simp only [pattern3, pattern11, pattern35, edge01, edge02, edge10, edge12, edge20, edge21, causalPair, Set.mem_preimage, Set.mem_inter_iff, Set.mem_union, Set.mem_compl_iff, Set.mem_setOf_eq, forkEvent]'), 3405: ('  simp only [pattern11, pattern35, edge01, edge02, edge10, edge12, edge20, edge21, causalPair, Set.mem_preimage, Set.mem_inter_iff, Set.mem_union, Set.mem_compl_iff, Set.mem_setOf_eq, Set.mem_univ, forkEvent, earliestComparable, comparable]', '  simp only [pattern11, pattern35, edge01, edge02, edge10, edge12, edge20, edge21, causalPair, Set.mem_preimage, Set.mem_inter_iff, Set.mem_union, Set.mem_compl_iff, Set.mem_setOf_eq, forkEvent, earliestComparable, comparable]'), 3540: ('      simp only [pattern1, pattern8, edge01, edge02, edge10, edge12, edge20, edge21, causalPair, Set.mem_preimage, Set.mem_inter_iff, Set.mem_union, Set.mem_compl_iff, Set.mem_setOf_eq, rotate, reverseTriple, reverse_precedes]', '      simp only [pattern1, pattern8, edge01, edge02, edge10, edge12, edge20, edge21, causalPair, Set.mem_preimage, Set.mem_inter_iff, Set.mem_compl_iff, Set.mem_setOf_eq, rotate]'), 3547: ('      simp only [pattern1, pattern4, edge01, edge02, edge10, edge12, edge20, edge21, causalPair, Set.mem_preimage, Set.mem_inter_iff, Set.mem_union, Set.mem_compl_iff, Set.mem_setOf_eq, rotate, reverseTriple, reverse_precedes]', '      simp only [pattern1, pattern4, edge01, edge02, edge10, edge12, edge20, edge21, causalPair, Set.mem_preimage, Set.mem_inter_iff, Set.mem_compl_iff, Set.mem_setOf_eq, reverseTriple, reverse_precedes]'), 3554: ('      simp only [pattern8, pattern16, edge01, edge02, edge10, edge12, edge20, edge21, causalPair, Set.mem_preimage, Set.mem_inter_iff, Set.mem_union, Set.mem_compl_iff, Set.mem_setOf_eq, rotate, reverseTriple, reverse_precedes]', '      simp only [pattern8, pattern16, edge01, edge02, edge10, edge12, edge20, edge21, causalPair, Set.mem_preimage, Set.mem_inter_iff, Set.mem_compl_iff, Set.mem_setOf_eq, rotate]'), 3561: ('      simp only [pattern8, pattern32, edge01, edge02, edge10, edge12, edge20, edge21, causalPair, Set.mem_preimage, Set.mem_inter_iff, Set.mem_union, Set.mem_compl_iff, Set.mem_setOf_eq, rotate, reverseTriple, reverse_precedes]', '      simp only [pattern8, pattern32, edge01, edge02, edge10, edge12, edge20, edge21, causalPair, Set.mem_preimage, Set.mem_inter_iff, Set.mem_compl_iff, Set.mem_setOf_eq, reverseTriple, reverse_precedes]'), 3568: ('      simp only [pattern2, pattern16, edge01, edge02, edge10, edge12, edge20, edge21, causalPair, Set.mem_preimage, Set.mem_inter_iff, Set.mem_union, Set.mem_compl_iff, Set.mem_setOf_eq, rotate, reverseTriple, reverse_precedes]', '      simp only [pattern2, pattern16, edge01, edge02, edge10, edge12, edge20, edge21, causalPair, Set.mem_preimage, Set.mem_inter_iff, Set.mem_compl_iff, Set.mem_setOf_eq, reverseTriple, reverse_precedes]'), 3575: ('      simp only [pattern3, pattern12, edge01, edge02, edge10, edge12, edge20, edge21, causalPair, Set.mem_preimage, Set.mem_inter_iff, Set.mem_union, Set.mem_compl_iff, Set.mem_setOf_eq, rotate, reverseTriple, reverse_precedes]', '      simp only [pattern3, pattern12, edge01, edge02, edge10, edge12, edge20, edge21, causalPair, Set.mem_preimage, Set.mem_inter_iff, Set.mem_compl_iff, Set.mem_setOf_eq, rotate]'), 3582: ('      simp only [pattern3, pattern20, edge01, edge02, edge10, edge12, edge20, edge21, causalPair, Set.mem_preimage, Set.mem_inter_iff, Set.mem_union, Set.mem_compl_iff, Set.mem_setOf_eq, rotate, reverseTriple, reverse_precedes]', '      simp only [pattern3, pattern20, edge01, edge02, edge10, edge12, edge20, edge21, causalPair, Set.mem_preimage, Set.mem_inter_iff, Set.mem_compl_iff, Set.mem_setOf_eq, reverseTriple, reverse_precedes]'), 3589: ('      simp only [pattern12, pattern48, edge01, edge02, edge10, edge12, edge20, edge21, causalPair, Set.mem_preimage, Set.mem_inter_iff, Set.mem_union, Set.mem_compl_iff, Set.mem_setOf_eq, rotate, reverseTriple, reverse_precedes]', '      simp only [pattern12, pattern48, edge01, edge02, edge10, edge12, edge20, edge21, causalPair, Set.mem_preimage, Set.mem_inter_iff, Set.mem_compl_iff, Set.mem_setOf_eq, rotate]'), 3596: ('      simp only [pattern12, pattern33, edge01, edge02, edge10, edge12, edge20, edge21, causalPair, Set.mem_preimage, Set.mem_inter_iff, Set.mem_union, Set.mem_compl_iff, Set.mem_setOf_eq, rotate, reverseTriple, reverse_precedes]', '      simp only [pattern12, pattern33, edge01, edge02, edge10, edge12, edge20, edge21, causalPair, Set.mem_preimage, Set.mem_inter_iff, Set.mem_compl_iff, Set.mem_setOf_eq, reverseTriple, reverse_precedes]'), 3603: ('      simp only [pattern10, pattern48, edge01, edge02, edge10, edge12, edge20, edge21, causalPair, Set.mem_preimage, Set.mem_inter_iff, Set.mem_union, Set.mem_compl_iff, Set.mem_setOf_eq, rotate, reverseTriple, reverse_precedes]', '      simp only [pattern10, pattern48, edge01, edge02, edge10, edge12, edge20, edge21, causalPair, Set.mem_preimage, Set.mem_inter_iff, Set.mem_compl_iff, Set.mem_setOf_eq, reverseTriple, reverse_precedes]'), 3610: ('      simp only [pattern11, pattern28, edge01, edge02, edge10, edge12, edge20, edge21, causalPair, Set.mem_preimage, Set.mem_inter_iff, Set.mem_union, Set.mem_compl_iff, Set.mem_setOf_eq, rotate, reverseTriple, reverse_precedes]', '      simp only [pattern11, pattern28, edge01, edge02, edge10, edge12, edge20, edge21, causalPair, Set.mem_preimage, Set.mem_inter_iff, Set.mem_compl_iff, Set.mem_setOf_eq, rotate]'), 3617: ('      simp only [pattern11, pattern52, edge01, edge02, edge10, edge12, edge20, edge21, causalPair, Set.mem_preimage, Set.mem_inter_iff, Set.mem_union, Set.mem_compl_iff, Set.mem_setOf_eq, rotate, reverseTriple, reverse_precedes]', '      simp only [pattern11, pattern52, edge01, edge02, edge10, edge12, edge20, edge21, causalPair, Set.mem_preimage, Set.mem_inter_iff, Set.mem_compl_iff, Set.mem_setOf_eq, reverseTriple, reverse_precedes]'), 3624: ('      simp only [pattern28, pattern49, edge01, edge02, edge10, edge12, edge20, edge21, causalPair, Set.mem_preimage, Set.mem_inter_iff, Set.mem_union, Set.mem_compl_iff, Set.mem_setOf_eq, rotate, reverseTriple, reverse_precedes]', '      simp only [pattern28, pattern49, edge01, edge02, edge10, edge12, edge20, edge21, causalPair, Set.mem_preimage, Set.mem_inter_iff, Set.mem_compl_iff, Set.mem_setOf_eq, rotate]'), 3631: ('      simp only [pattern28, pattern35, edge01, edge02, edge10, edge12, edge20, edge21, causalPair, Set.mem_preimage, Set.mem_inter_iff, Set.mem_union, Set.mem_compl_iff, Set.mem_setOf_eq, rotate, reverseTriple, reverse_precedes]', '      simp only [pattern28, pattern35, edge01, edge02, edge10, edge12, edge20, edge21, causalPair, Set.mem_preimage, Set.mem_inter_iff, Set.mem_compl_iff, Set.mem_setOf_eq, reverseTriple, reverse_precedes]'), 3638: ('      simp only [pattern14, pattern49, edge01, edge02, edge10, edge12, edge20, edge21, causalPair, Set.mem_preimage, Set.mem_inter_iff, Set.mem_union, Set.mem_compl_iff, Set.mem_setOf_eq, rotate, reverseTriple, reverse_precedes]', '      simp only [pattern14, pattern49, edge01, edge02, edge10, edge12, edge20, edge21, causalPair, Set.mem_preimage, Set.mem_inter_iff, Set.mem_compl_iff, Set.mem_setOf_eq, reverseTriple, reverse_precedes]'), 3773: ('      simp only [pattern49, pattern52, edge01, edge02, edge10, edge12, edge20, edge21, causalPair, Set.mem_preimage, Set.mem_inter_iff, Set.mem_union, Set.mem_compl_iff, Set.mem_setOf_eq] at hz hw', '      simp only [pattern49, pattern52, edge01, edge02, edge10, edge12, edge20, edge21, causalPair, Set.mem_preimage, Set.mem_inter_iff, Set.mem_compl_iff, Set.mem_setOf_eq] at hz hw'), 3832: ('      simp only [pattern49, pattern52, edge01, edge02, edge10, edge12, edge20, edge21, causalPair, Set.mem_preimage, Set.mem_inter_iff, Set.mem_union, Set.mem_compl_iff, Set.mem_setOf_eq] at hz hw', '      simp only [pattern49, pattern52, edge01, edge02, edge10, edge12, edge20, edge21, causalPair, Set.mem_preimage, Set.mem_inter_iff, Set.mem_compl_iff, Set.mem_setOf_eq] at hz hw'), 3846: ('      simp only [pattern11, pattern35, edge01, edge02, edge10, edge12, edge20, edge21, causalPair, Set.mem_preimage, Set.mem_inter_iff, Set.mem_union, Set.mem_compl_iff, Set.mem_setOf_eq] at hz hw', '      simp only [pattern11, pattern35, edge01, edge02, edge10, edge12, edge20, edge21, causalPair, Set.mem_preimage, Set.mem_inter_iff, Set.mem_compl_iff, Set.mem_setOf_eq] at hz hw'), 3855: ('      simp only [pattern11, pattern35, edge01, edge02, edge10, edge12, edge20, edge21, causalPair, Set.mem_preimage, Set.mem_inter_iff, Set.mem_union, Set.mem_compl_iff, Set.mem_setOf_eq] at hz hw', '      simp only [pattern11, pattern35, edge01, edge02, edge10, edge12, edge20, edge21, causalPair, Set.mem_preimage, Set.mem_inter_iff, Set.mem_compl_iff, Set.mem_setOf_eq] at hz hw'), 3889: ('      simp only [pattern16, pattern32, edge01, edge02, edge10, edge12, edge20, edge21, causalPair, Set.mem_preimage, Set.mem_inter_iff, Set.mem_union, Set.mem_compl_iff, Set.mem_setOf_eq] at hz hw', '      simp only [pattern16, pattern32, edge01, edge02, edge10, edge12, edge20, edge21, causalPair, Set.mem_preimage, Set.mem_inter_iff, Set.mem_compl_iff, Set.mem_setOf_eq] at hz hw'), 3906: ('      simp only [pattern12, pattern48, edge01, edge02, edge10, edge12, edge20, edge21, causalPair, Set.mem_preimage, Set.mem_inter_iff, Set.mem_union, Set.mem_compl_iff, Set.mem_setOf_eq] at hz hw', '      simp only [pattern12, pattern48, edge01, edge02, edge10, edge12, edge20, edge21, causalPair, Set.mem_preimage, Set.mem_inter_iff, Set.mem_compl_iff, Set.mem_setOf_eq] at hz hw'), 3923: ('      simp only [pattern20, pattern33, edge01, edge02, edge10, edge12, edge20, edge21, causalPair, Set.mem_preimage, Set.mem_inter_iff, Set.mem_union, Set.mem_compl_iff, Set.mem_setOf_eq] at hz hw', '      simp only [pattern20, pattern33, edge01, edge02, edge10, edge12, edge20, edge21, causalPair, Set.mem_preimage, Set.mem_inter_iff, Set.mem_compl_iff, Set.mem_setOf_eq] at hz hw'), 3955: ('      simp only [pattern49, pattern52, edge01, edge02, edge10, edge12, edge20, edge21, causalPair, Set.mem_preimage, Set.mem_inter_iff, Set.mem_union, Set.mem_compl_iff, Set.mem_setOf_eq] at hz hw', '      simp only [pattern49, pattern52, edge01, edge02, edge10, edge12, edge20, edge21, causalPair, Set.mem_preimage, Set.mem_inter_iff, Set.mem_compl_iff, Set.mem_setOf_eq] at hz hw'), 3349: ('theorem partition_set_all : (Set.univ : Set (Triple E)) = (pattern0 ∪ (pattern1 ∪ (pattern2 ∪ (pattern3 ∪ (pattern4 ∪ (pattern8 ∪ (pattern10 ∪ (pattern11 ∪ (pattern12 ∪ (pattern14 ∪ (pattern16 ∪ (pattern20 ∪ (pattern28 ∪ (pattern32 ∪ (pattern33 ∪ (pattern35 ∪ (pattern48 ∪ (pattern49 ∪ pattern52)))))))))))))))))) := by', 'omit [InnerProductSpace ℝ E] [FiniteDimensional ℝ E] [ProperSpace E] [MeasurableSpace E] [BorelSpace E] in\ntheorem partition_set_all : (Set.univ : Set (Triple E)) = (pattern0 ∪ (pattern1 ∪ (pattern2 ∪ (pattern3 ∪ (pattern4 ∪ (pattern8 ∪ (pattern10 ∪ (pattern11 ∪ (pattern12 ∪ (pattern14 ∪ (pattern16 ∪ (pattern20 ∪ (pattern28 ∪ (pattern32 ∪ (pattern33 ∪ (pattern35 ∪ (pattern48 ∪ (pattern49 ∪ pattern52)))))))))))))))))) := by'), 3364: ('theorem partition_set_pair : (edge12 ∪ edge21 : Set (Triple E)) = (pattern8 ∪ (pattern10 ∪ (pattern11 ∪ (pattern12 ∪ (pattern14 ∪ (pattern28 ∪ (pattern32 ∪ (pattern33 ∪ (pattern35 ∪ (pattern48 ∪ (pattern49 ∪ pattern52))))))))))) := by', 'omit [InnerProductSpace ℝ E] [FiniteDimensional ℝ E] [ProperSpace E] [MeasurableSpace E] [BorelSpace E] in\ntheorem partition_set_pair : (edge12 ∪ edge21 : Set (Triple E)) = (pattern8 ∪ (pattern10 ∪ (pattern11 ∪ (pattern12 ∪ (pattern14 ∪ (pattern28 ∪ (pattern32 ∪ (pattern33 ∪ (pattern35 ∪ (pattern48 ∪ (pattern49 ∪ pattern52))))))))))) := by'), 3379: ('theorem partition_set_fork : (forkEvent : Set (Triple E)) = (pattern3 ∪ (pattern11 ∪ pattern35)) := by', 'omit [InnerProductSpace ℝ E] [FiniteDimensional ℝ E] [ProperSpace E] [MeasurableSpace E] [BorelSpace E] in\ntheorem partition_set_fork : (forkEvent : Set (Triple E)) = (pattern3 ∪ (pattern11 ∪ pattern35)) := by'), 3394: ('theorem partition_set_earliest : (earliestComparable : Set (Triple E)) = (pattern11 ∪ pattern35) := by', 'omit [InnerProductSpace ℝ E] [FiniteDimensional ℝ E] [ProperSpace E] [MeasurableSpace E] [BorelSpace E] in\ntheorem partition_set_earliest : (earliestComparable : Set (Triple E)) = (pattern11 ∪ pattern35) := by'), 3098: ('    simpa using h', '    simp'), 3857: ('    all_goals ring', '')}

def apply_final_linter_cleanup(src):
    rows=src.splitlines()
    for n,(old,new) in sorted(
        LINTER_CLEANUP_EDITS.items(),reverse=True
    ):
        assert rows[n-1]==old,(
            "STOP_GENERATOR_CLEANUP_MISMATCH",n
        )
        rows[n-1:n]=new.splitlines()
    return "\n".join(rows)+"\n"

out.write_text(apply_final_linter_cleanup(out.read_text()))
