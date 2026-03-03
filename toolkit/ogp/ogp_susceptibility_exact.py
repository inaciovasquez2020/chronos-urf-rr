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
    v = np.array(v,dtype=float)
    return v / np.sum(v)

def cavity_update(m):
    new = []
    for x in states:
        s = 0.0
        for j,y in enumerate(states):
            if allowed(x,y):
                s += m[j]
        val = weight(x) * (s**(Δ-1))
        new.append(val)
    return normalize(new)

def fixed_point(iters=500):
    m = normalize(np.ones(4))
    for _ in range(iters):
        m = cavity_update(m)
    return m

def jacobian(m,eps=1e-7):
    J = np.zeros((4,4))
    base = cavity_update(m)
    for i in range(4):
        m2 = m.copy()
        m2[i] += eps
        m2 = normalize(m2)
        f = cavity_update(m2)
        J[:,i] = (f - base)/eps
    return J

def compute_overlap(m):
    return m[3]

def susceptibility():
    m = fixed_point()
    J = jacobian(m)
    I = np.eye(4)
    A = np.linalg.inv(I - J)
    v = np.array([0,0,0,1])
    resp = A @ v
    chi = resp[3]
    return m, chi

if __name__ == "__main__":
    m,chi = susceptibility()
    kappa = 1/chi
    print("fixed point:",m)
    print("susceptibility dq/dη:",chi)
    print("kappa_Bethe:",kappa)

