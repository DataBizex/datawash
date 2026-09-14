"""Shared pytest fixtures for barcelona-airbnb tests."""

import sys
from pathlib import Path

# Make our src/ folder importable in tests
TESTS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = TESTS_DIR.parent
SRC_DIR = PROJECT_ROOT / "src"
DATAWASH_ROOT = PROJECT_ROOT.parent

sys.path.insert(0, str(SRC_DIR))
sys.path.insert(0, str(DATAWASH_ROOT))
