import numpy as np

Δ = 6
λ = 0.2
η = 0.0

states = [(0,0),(0,1),(1,0),(1,1)]

def weight(x):
    a,b = x
    if x == (1,1):
        return λ**2 * np.exp(η)
    return λ**(a+b)

def allowed(x,y):
    a,b = x
    c,d = y
    return (a*c == 0) and (b*d == 0)

def normalize(v):
    s = sum(v)
    return np.array(v)/s

def cavity_update(m):
    new = []
    for x in states:
        s = 0
        for y in states:
            if allowed(x,y):
                s += m[states.index(y)]
        val = weight(x) * (s**(Δ-1))
        new.append(val)
    return normalize(new)

def fixed_point(iterations=200):
    m = normalize(np.ones(4))
    for _ in range(iterations):
        m = cavity_update(m)
    return m

def overlap(m):
    return m[3]

def compute_q(η_val):
    global η
    η = η_val
    m = fixed_point()
    return overlap(m)

def curvature(step=1e-3):
    q1 = compute_q(η-step)
    q2 = compute_q(η)
    q3 = compute_q(η+step)
    return (q1 - 2*q2 + q3)/(step**2)

if __name__ == "__main__":
    m = fixed_point()
    q = overlap(m)
    curv = curvature()
    print("fixed point:",m)
    print("overlap q:",q)
    print("curvature:",curv)
