from tools.ef_game.src.ef_game import GameSpec, spec_digest

def test_digest_stable():
    A = {0:[1],1:[0]}
    B = {0:[1],1:[0]}
    s1 = spec_digest(GameSpec(k=2, rounds=3, graphA=A, graphB=B, seed=7))
    s2 = spec_digest(GameSpec(k=2, rounds=3, graphA={1:[0],0:[1]}, graphB=B, seed=7))
    assert s1 == s2
