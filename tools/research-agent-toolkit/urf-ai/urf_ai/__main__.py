from __future__ import annotations
import argparse,json
from .assistant import answer,benchmark

def main():
    p=argparse.ArgumentParser(description="URF-AI read-only synthetic research adapter")
    p.add_argument("case",nargs="?",default="benchmark")
    a=p.parse_args()
    print(json.dumps(benchmark() if a.case=="benchmark" else answer(a.case),indent=2,sort_keys=True))
if __name__=="__main__":main()
