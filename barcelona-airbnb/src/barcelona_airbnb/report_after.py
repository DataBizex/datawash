"""Convenience runner for generating the after-cleaning report."""

import sys
from pathlib import Path

DATAWASH_ROOT = Path(__file__).resolve().parent.parent.parent.parent
SRC_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DATAWASH_ROOT))
sys.path.insert(0, str(SRC_DIR))

from barcelona_airbnb.profile import profile_processed

if __name__ == "__main__":
    output = profile_processed()
    print(f"\nAfter-cleaning report saved: {output}")
