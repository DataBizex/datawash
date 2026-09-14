"""Transform cleaned data into an analytics-ready dataset with a defined schema."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

DATAWASH_ROOT = Path(__file__).resolve().parent.parent.parent.parent
SRC_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DATAWASH_ROOT))
sys.path.insert(0, str(SRC_DIR))

from barcelona_airbnb.clean import clean_listings
from shared.utils.io import interim_dir, processed_dir, project_root
from shared.utils.logging_setup import setup_logger

PROJECT_NAME = "barcelona-airbnb"
CLEAN_INPUT_FILENAME = "listings_clean.parquet"
PROCESSED_FILENAME = "listings.parquet"
SCHEMA_PATH = project_root(PROJECT_NAME) / "config" / "schema.yaml"

logger = setup_logger(__name__)


def load_schema(schema_path: Path = SCHEMA_PATH) -> dict:
    """Load the schema definition from YAML."""
    with schema_path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def select_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Keep only the columns listed, in the given order.

    Columns that don't exist in the DataFrame are logged and skipped.
    """
    existing = [c for c in columns if c in df.columns]
    missing = [c for c in columns if c not in df.columns]

    if missing:
        logger.warning(f"Requested columns missing from source: {missing}")

    logger.info(f"Selected {len(existing)} of {len(columns)} requested columns")
    return df[existing].copy()


def coerce_types(df: pd.DataFrame, type_map: dict[str, str]) -> pd.DataFrame:
    """
    Coerce columns to their target dtypes.

    Errors during coercion produce NaN for numeric types and NA for string types.
    """
    df = df.copy()
    for col, target_type in type_map.items():
        if col not in df.columns:
            continue

        try:
            if target_type in ("int64", "float64"):
                df[col] = pd.to_numeric(df[col], errors="coerce")
                if target_type == "int64":
                    # int64 can't hold NaN; use nullable Int64
                    df[col] = df[col].astype("Int64")
                else:
                    df[col] = df[col].astype(target_type)
            elif target_type == "string":
                df[col] = df[col].astype("string")
            elif target_type == "bool":
                df[col] = df[col].astype("boolean")
            else:
                logger.warning(f"Unknown target type '{target_type}' for '{col}'")
        except Exception as exc:
            logger.error(f"Failed to coerce '{col}' to '{target_type}': {exc}")
    logger.info(f"Coerced types for {len(type_map)} columns")
    return df


def add_derived_columns(df: pd.DataFrame, derived: dict) -> pd.DataFrame:
    """
    Add computed columns using safe eval expressions.

    Only expressions referencing existing columns are added.
    """
    df = df.copy()
    added = 0
    for col, spec in derived.items():
        formula = spec["formula"]
        dtype = spec.get("dtype", "float64")

        try:
            # eval() with columns as local variables — no arbitrary Python execution
            df[col] = df.eval(formula, engine="python")
            if dtype == "bool":
                df[col] = df[col].astype("boolean")
            elif dtype == "float64":
                df[col] = pd.to_numeric(df[col], errors="coerce")
            added += 1
            logger.info(f"Derived '{col}' = {formula}")
        except Exception as exc:
            logger.error(f"Failed to compute derived '{col}': {exc}")

    logger.info(f"Added {added} derived columns")
    return df


def transform_listings(df: pd.DataFrame | None = None) -> pd.DataFrame:
    """
    Transform cleaned data into the final analytical schema.

    If df is None, read from data/interim/listings_clean.parquet.
    """
    if df is None:
        source = interim_dir(PROJECT_NAME) / CLEAN_INPUT_FILENAME
        if not source.exists():
            logger.info("Cleaned interim file not found — running clean pipeline first")
            df = clean_listings()
        else:
            logger.info(f"Reading cleaned data from {source.name}")
            df = pd.read_parquet(source)

    schema = load_schema()

    df = select_columns(df, list(schema["columns"].keys()))
    df = coerce_types(df, schema["columns"])
    df = add_derived_columns(df, schema.get("derived", {}))

    logger.info(f"Transform complete: {len(df):,} rows, {len(df.columns)} columns")
    return df


def transform_and_save() -> Path:
    """Run transform and save the processed dataset as Parquet."""
    df = transform_listings()

    output_path = processed_dir(PROJECT_NAME) / PROCESSED_FILENAME
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(output_path, index=False)
    logger.info(f"Processed data saved to: {output_path}")

    return output_path


if __name__ == "__main__":
    output = transform_and_save()
    print(f"\nProcessed data saved: {output}")
