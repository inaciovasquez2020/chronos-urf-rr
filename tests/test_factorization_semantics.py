def factors_through_example():
    f = lambda x: x + 1
    g = lambda x: f(x)
    for x in range(5):
        assert g(x) == f(x)

def test_factorization_semantics():
    factors_through_example()
