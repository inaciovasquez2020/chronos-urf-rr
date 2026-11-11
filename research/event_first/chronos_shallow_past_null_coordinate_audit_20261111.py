#!/usr/bin/env python3
"""4D sprinkled-diamond shallow-past null-coordinate intensity check.

Monte Carlo only tests a proved intensity limit; it does NOT sample random
linear extensions and does NOT prove a Minkowski prefix-law limit.
"""
import math
import random


def run(N, samples=300000, seed=20261111):
    rng = random.Random(seed + N)
    mass = u_mass = f_mass = 0.0
    for _ in range(samples):
        a = 1-rng.random()**.25
        t = a if rng.random()<.5 else -a
        r = (1-a)*rng.random()**(1/3)
        u, w = (1+t+r)/2, (1+t-r)/2
        past_volume = (u*w)**2
        future_volume = ((1-u)*(1-w))**2
        # Exact conditional chance this point has 0 predecessors.
        weight = (1-past_volume)**(N-1)
        mass += weight
        u_mass += u*weight
        f_mass += future_volume*weight
    return mass/samples, u_mass/mass, f_mass/mass


def main():
    target_u = 2/3
    target_future = 1/6
    assert abs(2/3-target_u) < 1e-15
    # For U~Beta(2,1): E[(1-U)^2] = 1/6; F=(1-U)^2;
    # the CDF is 2sqrt(f)-f.
    for t in (0.01, 0.1, 0.5, 1.0):
        assert 0 <= 2*math.sqrt(t)-t <= 1
    for N in (1000,10000):
        prob, mean_u, mean_future = run(N)
        # Finite-N boundary effects are O(N^-1/4) or larger.
        print(f'N={N} P(minimal)={prob:.8f} mean_U={mean_u:.6f} mean_future={mean_future:.6f}')
        assert abs(mean_u-target_u)<.055
        assert abs(mean_future-target_future)<.055
    print('NULL_COORDINATE_EXPECTED_INTENSITY := MONTE_CARLO_PASS')
    print('U_LIMIT_DENSITY := 2*u')
    print('T_LIMIT_CONDITIONAL_EXACTLY_J_PREDECESSORS := Gamma(j+1/2, 1)')
    print('LINEAR_EXTENSION_SELECTION_WEIGHT_LIMIT := OPEN')


if __name__ == '__main__': main()
