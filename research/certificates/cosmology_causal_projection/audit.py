import pathlib,re,sys

root=pathlib.Path(__file__).resolve().parent
src=(root/"receipt/CausalProjection.lean").read_text()
log=pathlib.Path(sys.argv[1]).read_text()

expected={
    "Chronos.CosmologyBridge."+n
    for n in re.findall(r"^#print axioms (\w+)$",src,re.M)
}

required={
    "Chronos.CosmologyBridge.stripArea_closed",
    "Chronos.CosmologyBridge.probability_bounds",
    "Chronos.CosmologyBridge.projection_collision",
    "Chronos.CosmologyBridge.no_perfect_visible_decoder",
    "Chronos.CosmologyBridge.strip_optimal_decoder"
}

assert len(expected)==11
assert required <= expected

found={}
for n,a in re.findall(
    r"'([^']+)' depends on axioms: \[([^\]]*)\]",log
):
    found[n]={x.strip() for x in a.split(",") if x.strip()}

for n in re.findall(
    r"'([^']+)' does not depend on any axioms",log
):
    found[n]=set()

allowed={"propext","Classical.choice","Quot.sound"}

assert set(found)==expected
assert all(a<=allowed for a in found.values()),found
assert not re.search(
    r"\b(?:axiom|opaque|sorry|admit|native_decide)\b",src
)
assert not re.search(r"\b(?:sorryAx|sorry|admit)\b",log)
assert not re.search(r"(?m)^.*error(?:\([^)]*\))?:",log)

print("AXIOM_AUDIT := PASS_11_OF_11")
