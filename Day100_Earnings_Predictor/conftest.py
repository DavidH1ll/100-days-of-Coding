"""Test configuration for the Day 100 capstone.

Adds this directory to ``sys.path`` so the test suite can import the
sibling module without it needing to be installed as a package.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
