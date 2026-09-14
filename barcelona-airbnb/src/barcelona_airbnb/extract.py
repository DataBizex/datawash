"""Extract raw Barcelona Airbnb listings data from CSV into a pandas DataFrame."""

import sys
from pathlib import Path

import pandas as pd

# Add the datawash root to Python's path so we can import from shared/
DATAWASH_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(DATAWASH_ROOT))

from shared.utils.io import raw_dir
from shared.utils.logging_setup import setup_logger

PROJECT_NAME = "barcelona-airbnb"
RAW_FILENAME = "barcelona_listings.csv"

logger = setup_logger(__name__)


def extract_listings(source_path: Path | None = None) -> pd.DataFrame:
    """
    Read the raw Barcelona Airbnb listings CSV into a DataFrame.

    Parameters
    ----------
    source_path : Path or None
        Path to the raw CSV file. If None, uses the default location
        under data/raw/.

    Returns
    -------
    pd.DataFrame
        Raw listings data, no cleaning applied.
    """
    if source_path is None:
        source_path = raw_dir(PROJECT_NAME) / RAW_FILENAME

    if not source_path.exists():
        logger.error(f"Source file not found: {source_path}")
        raise FileNotFoundError(f"Raw data not found at {source_path}")

    logger.info(f"Reading raw listings from {source_path.name}")
    df = pd.read_csv(source_path, low_memory=False)
    logger.info(f"Loaded {len(df):,} rows and {len(df.columns)} columns")

    return df


if __name__ == "__main__":
    df = extract_listings()
    print(f"\nDataFrame shape: {df.shape}")
    print(f"First 3 columns: {df.columns[:3].tolist()}")
