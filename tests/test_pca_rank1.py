import pytest
import sys
import os
import numpy as np

# Force local path inclusion for CI environment
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from radiative_rigidity_pca.radiative_rigidity_pca import covariance, is_rank1
