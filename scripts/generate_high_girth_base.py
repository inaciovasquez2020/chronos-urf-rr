import json

def heawood_graph():
    adj = {
        0: [1, 5, 13],
        1: [0, 2, 10],
        2: [1, 3, 7],
        3: [2, 4, 12],
        4: [3, 5, 9],
        5: [0, 4, 6],
        6: [5, 7, 11],
        7: [2, 6, 8],
        8: [7, 9, 13],
        9: [4, 8, 10],
        10: [1, 9, 11],
        11: [6, 10, 12],
        12: [3, 11, 13],
        13: [0, 8, 12],
    }
    return {k: sorted(v) for k, v in adj.items()}

def main():
    R = 2
    target = 2 * R + 2
    out = {
        "name": "HeawoodGraph",
        "n": 14,
        "R": R,
        "adj": heawood_graph(),
        "girth": 6,
        "target": target,
    }
    with open("artifacts/high_girth_base.json", "w") as f:
        json.dump(out, f, indent=2, sort_keys=True)

if __name__ == "__main__":
    main()
