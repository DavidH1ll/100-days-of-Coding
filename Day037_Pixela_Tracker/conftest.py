"""Conftest for Day 037 tests.

Loads Day037/pixela_tracker.py as a regular import (the module name is
unique across the repo, so no sys.modules collision with other days).
"""
import sys
from pathlib import Path

_DAY_DIR = Path(__file__).resolve().parent.parent
if str(_DAY_DIR) not in sys.path:
    sys.path.insert(0, str(_DAY_DIR))
