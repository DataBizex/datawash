"""Tests for the cleaning module."""

import numpy as np
import pandas as pd
import pytest
from barcelona_airbnb.clean import (
    clean_percentage,
    clean_price,
    clean_text,
    drop_id_duplicates,
    standardize_column_names,
)

# ---------- clean_price ----------


def test_clean_price_strips_dollar_sign():
    df = pd.DataFrame({"price": ["$100.00", "$50.50"]})
    result = clean_price(df)
    assert result["price"].tolist() == [100.00, 50.50]


def test_clean_price_handles_commas():
    df = pd.DataFrame({"price": ["$1,250.00"]})
    result = clean_price(df)
    assert result["price"].tolist() == [1250.00]


def test_clean_price_bad_values_become_nan():
    df = pd.DataFrame({"price": ["$100.00", "invalid", None]})
    result = clean_price(df)
    assert result["price"].iloc[0] == 100.00
    assert pd.isna(result["price"].iloc[1])
    assert pd.isna(result["price"].iloc[2])


def test_clean_price_missing_column_no_crash():
    df = pd.DataFrame({"other": [1, 2, 3]})
    result = clean_price(df)  # should not raise
    assert list(result.columns) == ["other"]


# ---------- clean_percentage ----------


def test_clean_percentage_strips_percent_sign():
    df = pd.DataFrame({"rate": ["99%", "50%", "0%"]})
    result = clean_percentage(df, columns=["rate"])
    assert result["rate"].tolist() == [99.0, 50.0, 0.0]


def test_clean_percentage_handles_missing():
    df = pd.DataFrame({"rate": ["100%", None, "80%"]})
    result = clean_percentage(df, columns=["rate"])
    assert result["rate"].iloc[0] == 100.0
    assert pd.isna(result["rate"].iloc[1])
    assert result["rate"].iloc[2] == 80.0


# ---------- clean_text ----------


def test_clean_text_strips_html():
    df = pd.DataFrame({"desc": ["<p>Nice flat</p>", "<b>Studio</b>"]})
    result = clean_text(df, columns=["desc"])
    assert result["desc"].tolist() == ["Nice flat", "Studio"]


def test_clean_text_collapses_whitespace():
    df = pd.DataFrame({"desc": ["Nice   flat   in   center"]})
    result = clean_text(df, columns=["desc"])
    assert result["desc"].tolist() == ["Nice flat in center"]


def test_clean_text_preserves_nan():
    df = pd.DataFrame({"desc": ["Nice flat", None, ""]})
    result = clean_text(df, columns=["desc"])
    assert result["desc"].iloc[0] == "Nice flat"
    assert pd.isna(result["desc"].iloc[1])


# ---------- drop_id_duplicates ----------


def test_drop_id_duplicates_removes_repeats():
    df = pd.DataFrame({"id": [1, 2, 2, 3], "name": ["a", "b", "c", "d"]})
    result = drop_id_duplicates(df)
    assert len(result) == 3
    assert result["id"].tolist() == [1, 2, 3]


def test_drop_id_duplicates_no_duplicates():
    df = pd.DataFrame({"id": [1, 2, 3], "name": ["a", "b", "c"]})
    result = drop_id_duplicates(df)
    assert len(result) == 3


# ---------- standardize_column_names ----------


def test_standardize_lowercases_columns():
    df = pd.DataFrame({"MyColumn": [1], "Another Column": [2]})
    result = standardize_column_names(df)
    assert list(result.columns) == ["mycolumn", "another_column"]


def test_standardize_replaces_special_chars():
    df = pd.DataFrame({"host response rate (%)": [1]})
    result = standardize_column_names(df)
    assert list(result.columns) == ["host_response_rate"]
