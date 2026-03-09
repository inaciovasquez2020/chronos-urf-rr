#!/usr/bin/env python3

import json
from toolkit.oblivion.cor.cycle_overlap_rank import (
    random_regular_test,
    cayley_test,
    scaling_experiment,
    continuum_constant
)

def main():

    out = {}

    r = random_regular_test()
    out["random_regular"] = r

    c = cayley_test()
    out["cayley"] = c

    s = scaling_experiment()
    out["scaling"] = s

    out["continuum_constant"] = continuum_constant(s)

    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
