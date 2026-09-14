"""Tests for the extract module."""

from pathlib import Path

import pandas as pd
import pytest
from barcelona_airbnb.extract import extract_listings


def test_extract_returns_dataframe():
    """extract_listings should return a pandas DataFrame."""
    df = extract_listings()
    assert isinstance(df, pd.DataFrame)


def test_extract_has_rows():
    """The loaded DataFrame should contain at least 1,000 rows."""
    df = extract_listings()
    assert len(df) >= 1_000, f"Expected at least 1,000 rows, got {len(df)}"


def test_extract_has_expected_columns():
    """The DataFrame should have essential Airbnb columns."""
    df = extract_listings()
    essential_columns = {"id", "name", "price"}
    missing = essential_columns - set(df.columns)
    assert not missing, f"Missing expected columns: {missing}"


def test_extract_raises_on_missing_file():
    """When source file is missing, extract_listings should raise FileNotFoundError."""
    fake_path = Path("nonexistent_file.csv")
    with pytest.raises(FileNotFoundError):
        extract_listings(source_path=fake_path)
