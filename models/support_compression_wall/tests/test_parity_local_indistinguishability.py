# models/support_compression_wall/tests/test_parity_local_indistinguishability.py

import itertools


def parity(x):
    return sum(x) & 1


def local_view(x, idx):
    return tuple(v for i, v in enumerate(x) if i != idx)


def test_parity_local_indistinguishability():
    n = 6

    even = []
    odd = []

    for x in itertools.product([0, 1], repeat=n):
        if parity(x) == 0:
            even.append(x)
        else:
            odd.append(x)

    for idx in range(n):
        even_views = {local_view(x, idx) for x in even}
        odd_views = {local_view(x, idx) for x in odd}

        assert even_views == odd_views
