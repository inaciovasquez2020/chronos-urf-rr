import itertools
from math import comb
def parity(x):
return sum(x) & 1
def mu_parity_probs(n, target_parity):
xs = list(itertools.product([0,1], repeat=n))
supp = [x for x in xs if parity(x) == target_parity]
p = {x: 1.0/len(supp) for x in supp}
return p
def witness_depends_on_prefix(s):
def f(x):
return (sum(x[:s]) & 1)
return f
def bias_of_witness(n, s):
mu0 = mu_parity_probs(n, 0)
mu1 = mu_parity_probs(n, 1)
f = witness_depends_on_prefix(s)
p0 = sum(mu0[x] * (1 if f(x) else 0) for x in mu0)
p1 = sum(mu1[x] * (1 if f(x) else 0) for x in mu1)
return abs(p0 - p1)
def upper_bound(n, s):
return 2.0 ** (-(n - s))
def test_bias_bound_small_exact():
for n in range(2, 13):
for s in range(1, n):
b = bias_of_witness(n, s)
ub = upper_bound(n, s)
assert b <= ub + 1e-12
def tv_distance_disjoint_support(n):
mu0 = mu_parity_probs(n, 0)
mu1 = mu_parity_probs(n, 1)
all_x = set(mu0.keys()) | set(mu1.keys())
tv = 0.5 * sum(abs(mu0.get(x,0.0) - mu1.get(x,0.0)) for x in all_x)
return tv
def test_tv_is_one():
for n in range(1, 13):
assert abs(tv_distance_disjoint_support(n) - 1.0) < 1e-12
