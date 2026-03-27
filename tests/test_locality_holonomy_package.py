from toolkit.oblivion.scripts.cfi_pair_generator import cfi_pair_on_cycle
from toolkit.oblivion.scripts.cfi_holonomy_test import cfi_labeled_pair_on_cycle, holonomy_phi
from toolkit.oblivion.scripts.cfi_wl_verification import wl_signature

def test_cfi_wl_and_holonomy_separation():
    G0, G1 = cfi_pair_on_cycle(6, {(0, 1)})
    assert wl_signature(G0, 2) == wl_signature(G1, 2)

    D0, D1 = cfi_labeled_pair_on_cycle(6, {(0, 1)})
    assert holonomy_phi(D0, 6) == 0
    assert holonomy_phi(D1, 6) == 1
