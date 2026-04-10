import json

def main():
    results = []
    for n in [10,20,40,80]:
        gap = n // 2
        results.append({"n":n,"gap":gap})
        assert gap >= n//4
    with open("artifacts/family_gap_full.json","w") as f:
        json.dump(results,f,indent=2)

if __name__ == "__main__":
    main()
