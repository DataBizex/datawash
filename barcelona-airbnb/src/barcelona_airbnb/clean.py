"""Clean raw Barcelona Airbnb listings.

Each function handles one type of quality issue. They can be run individually
or composed via clean_listings().
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

DATAWASH_ROOT = Path(__file__).resolve().parent.parent.parent.parent
SRC_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DATAWASH_ROOT))
sys.path.insert(0, str(SRC_DIR))

from barcelona_airbnb.extract import extract_listings
from shared.utils.io import interim_dir
from shared.utils.logging_setup import setup_logger

PROJECT_NAME = "barcelona-airbnb"
CLEAN_FILENAME = "listings_clean.parquet"

logger = setup_logger(__name__)


# ---------- individual cleaning functions ----------


def clean_price(df: pd.DataFrame, column: str = "price") -> pd.DataFrame:
    """
    Convert price strings like '$130.00' into floats.

    Non-parseable values become NaN.
    """
    if column not in df.columns:
        logger.warning(f"Column '{column}' not found; skipping price cleanup")
        return df

    df = df.copy()
    before_dtype = df[column].dtype

    cleaned = (
        df[column]
        .astype(str)
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
    )
    df[column] = pd.to_numeric(cleaned, errors="coerce")

    logger.info(
        f"Cleaned '{column}': {before_dtype} -> {df[column].dtype}, "
        f"{df[column].isna().sum():,} unparseable values set to NaN"
    )
    return df


def clean_percentage(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """
    Convert percentage strings like '99%' into floats in 0-100 range.

    Non-parseable values become NaN.
    """
    df = df.copy()
    for column in columns:
        if column not in df.columns:
            logger.warning(f"Column '{column}' not found; skipping")
            continue

        cleaned = df[column].astype(str).str.replace("%", "", regex=False).str.strip()
        df[column] = pd.to_numeric(cleaned, errors="coerce")

        logger.info(
            f"Cleaned '{column}' as percentage, "
            f"{df[column].isna().sum():,} unparseable values set to NaN"
        )
    return df


_HTML_TAG_RE = re.compile(r"<[^>]+>")
_WHITESPACE_RE = re.compile(r"\s+")


def clean_text(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """
    For each column, strip HTML tags, collapse whitespace, and trim.

    Leaves NaN values as NaN (doesn't turn them into empty strings).
    """
    df = df.copy()
    for column in columns:
        if column not in df.columns:
            logger.warning(f"Column '{column}' not found; skipping text cleanup")
            continue

        mask_not_null = df[column].notna()
        df.loc[mask_not_null, column] = (
            df.loc[mask_not_null, column]
            .astype(str)
            .str.replace(_HTML_TAG_RE, " ", regex=True)
            .str.replace(_WHITESPACE_RE, " ", regex=True)
            .str.strip()
        )
        logger.info(
            f"Cleaned text in '{column}': stripped HTML and normalized whitespace"
        )
    return df


def drop_id_duplicates(df: pd.DataFrame, id_column: str = "id") -> pd.DataFrame:
    """
    Drop rows sharing the same id, keeping the first occurrence.
    """
    if id_column not in df.columns:
        logger.warning(f"Column '{id_column}' not found; skipping id-dedup")
        return df

    before = len(df)
    df = df.drop_duplicates(subset=[id_column], keep="first").reset_index(drop=True)
    dropped = before - len(df)
    logger.info(f"Dropped {dropped:,} duplicate rows on '{id_column}'")
    return df


def standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ensure all column names are lowercase snake_case.
    """
    df = df.copy()
    original = list(df.columns)
    df.columns = [
        re.sub(r"[^a-z0-9]+", "_", col.lower()).strip("_") for col in df.columns
    ]
    changed = sum(1 for a, b in zip(original, df.columns) if a != b)
    logger.info(f"Standardized column names: {changed} columns renamed")
    return df


# ---------- orchestrator ----------


def clean_listings(df: pd.DataFrame | None = None) -> pd.DataFrame:
    """
    Run the full cleaning pipeline on the raw listings.

    If df is None, load the raw file automatically.
    """
    if df is None:
        df = extract_listings()

    logger.info(f"Starting cleaning pipeline on {len(df):,} rows")

    df = standardize_column_names(df)
    df = drop_id_duplicates(df)
    df = clean_price(df, column="price")
    df = clean_percentage(df, columns=["host_response_rate", "host_acceptance_rate"])
    df = clean_text(df, columns=["name", "description", "neighborhood_overview"])

    logger.info(f"Cleaning complete: {len(df):,} rows in output")
    return df


def clean_and_save() -> Path:
    """
    Run the pipeline and persist the result as Parquet.

    Returns
    -------
    Path
        Location of the saved Parquet file.
    """
    df = clean_listings()

    output_path = interim_dir(PROJECT_NAME) / CLEAN_FILENAME
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(output_path, index=False)
    logger.info(f"Cleaned data saved to: {output_path}")

    return output_path


if __name__ == "__main__":
    output = clean_and_save()
    print(f"\nCleaned data saved: {output}")
