# models/support_compression_wall/tests/test_family_size_not_imply_bias.py

import itertools


def parity(x):
    return sum(x) & 1


def test_family_size_not_imply_bias():
    """
    Large family size does not imply observable bias
    under local observations.
    """

    n = 6

    even = []
    odd = []

    for x in itertools.product([0, 1], repeat=n):
        if parity(x) == 0:
            even.append(x)
        else:
            odd.append(x)

    # families are equal size
    assert len(even) == len(odd)

    # coordinate marginals are identical
    for i in range(n):
        even_avg = sum(x[i] for x in even) / len(even)
        odd_avg = sum(x[i] for x in odd) / len(odd)

        assert even_avg == odd_avg
