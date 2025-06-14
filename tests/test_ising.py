import numpy as np
from src.models import ising


def test_ising_magnetization_range(tmp_path):
    config = {
        'lattice_size': 10,
        'steps': 20,
        'seed': 0,
        'output_dir': tmp_path,
        'algorithm': 'wolff',
        'T_min': 2.0,
        'T_max': 2.0,
        'num_temps': 1,
    }
    mags = ising.run(config)
    assert len(mags) == 1
    assert 0 <= mags[0] <= 1
