import itertools
def parity(x):
return sum(x) & 1
def mu_parity(n, target):
xs = list(itertools.product([0,1], repeat=n))
supp = [x for x in xs if parity(x) == target]
p = {x: 1.0/len(supp) for x in supp}
return p
def all_witnesses_on_support(n, support):
support = tuple(support)
m = len(support)
for table in itertools.product([0,1], repeat=(2**m)):
def f(x, table=table, support=support):
idx = 0
for j, pos in enumerate(support):
idx |= (x[pos] << j)
return table[idx]
yield f
def max_bias_over_support(n, support):
mu0 = mu_parity(n, 0)
mu1 = mu_parity(n, 1)
mb = 0.0
for f in all_witnesses_on_support(n, support):
p0 = sum(mu0[x] * (1 if f(x) else 0) for x in mu0)
p1 = sum(mu1[x] * (1 if f(x) else 0) for x in mu1)
b = abs(p0 - p1)
if b > mb:
mb = b
return mb
def test_max_bias_matches_bound_for_small():
for n in range(3, 11):
for s in range(1, n):
support = list(range(s))
mb = max_bias_over_support(n, support)
ub = 2.0 ** (-(n - s))
assert mb <= ub + 1e-12
