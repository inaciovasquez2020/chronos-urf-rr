import pytest
import sys
import os

# Force local path inclusion for CI environment
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from chronos.entropy_audit import AuditParams, lower_bound_steps
