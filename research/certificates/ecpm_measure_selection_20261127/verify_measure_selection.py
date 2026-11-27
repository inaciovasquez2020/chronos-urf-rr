from fractions import Fraction as F
from itertools import product
import json

assert __debug__, "Optimized Python is not permitted"

p = F(1, 10)
second = 2 * F(1, 105) + 2 * F(1, 2100)
variance = second - p * p

assert second == F(1, 50)
assert variance == F(1, 100)

perturbation_checks = 0

for k in range(-100, 101):
    r = F(k, 10000)

    pplus = p + 2 * variance + r
    pminus = p - 2 * variance + r

    assert pplus >= F(11, 100)
    assert pminus <= F(9, 100)

    perturbation_checks += 1

product_checks = 0

for eps in (F(0), F(1, 100), F(1, 4), F(1)):
    for n in range(7):
        for factors in product(
            [1-eps, F(1), 1+eps],
            repeat=n
        ):
            density = F(1)

            for f in factors:
                density *= f

            assert abs(density-1) <= (2**n-1)*eps

            product_checks += 1

assert perturbation_checks == 201
assert product_checks == 4372

receipt = {
    "first_moment": str(p),
    "second_moment": str(second),
    "variance": str(variance),
    "perturbation_checks": perturbation_checks,
    "product_checks": product_checks,
    "total_checks": perturbation_checks + product_checks,
    "mismatches": 0,
    "arithmetic": "exact rational",
    "status": "COMPUTATION_PASS",
    "scope": "bounded arithmetic and product-density tests"
}

print(json.dumps(receipt, indent=2))
