import argparse, json

def clause_to_linpoly(S, b):
  # represent as dict var->coeff in F2 plus constant b
  # polynomial: (⊕_{e in S} x_e) + b
  return {"vars": [tuple(e) for e in S], "b": b}

def main():
  ap=argparse.ArgumentParser()
  ap.add_argument("--in_json", required=True)
  ap.add_argument("--out_json", required=True)
  args=ap.parse_args()
  D=json.load(open(args.in_json))
  polys=[]
  for st in D.get("steps", []):
    if "S" in st and "b" in st:
      polys.append({"op": st["op"], "poly": clause_to_linpoly(st["S"], st["b"])})
  json.dump({"meta": {"source": args.in_json}, "polys": polys}, open(args.out_json,"w"), indent=2)

if __name__=="__main__":
  main()
