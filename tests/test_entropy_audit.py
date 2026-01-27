import sys
import os
# This line tells Python: "Look one folder up to find the packages"
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import numpy as np
# Now the imports will work
from chronos.entropy_audit import AuditParams, lower_bound_steps
from radiative_rigidity_pca.radiative_rigidity_pca import covariance, is_rank1
