# From:
assert is_rank1(data) is True
assert is_rank1(noisy_data) is False

# To:
assert bool(is_rank1(data)) is True
assert bool(is_rank1(noisy_data)) is False
