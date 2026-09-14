"""Tests for the transform module."""

import pandas as pd
import pytest
from barcelona_airbnb.transform import add_derived_columns, coerce_types, select_columns


def test_select_columns_keeps_requested_order():
    df = pd.DataFrame({"a": [1], "b": [2], "c": [3]})
    result = select_columns(df, ["c", "a"])
    assert list(result.columns) == ["c", "a"]


def test_select_columns_skips_missing():
    df = pd.DataFrame({"a": [1], "b": [2]})
    result = select_columns(df, ["a", "nonexistent"])
    assert list(result.columns) == ["a"]


def test_coerce_types_string_to_float():
    df = pd.DataFrame({"x": ["1.5", "2.5", "bad"]})
    result = coerce_types(df, {"x": "float64"})
    assert result["x"].iloc[0] == 1.5
    assert pd.isna(result["x"].iloc[2])


def test_coerce_types_to_nullable_int():
    df = pd.DataFrame({"x": [1, 2, None]})
    result = coerce_types(df, {"x": "int64"})
    assert str(result["x"].dtype) == "Int64"


def test_add_derived_columns_simple_formula():
    df = pd.DataFrame({"price": [100.0, 200.0], "accommodates": [2, 4]})
    result = add_derived_columns(
        df,
        {"price_per_person": {"formula": "price / accommodates", "dtype": "float64"}},
    )
    assert result["price_per_person"].tolist() == [50.0, 50.0]


def test_add_derived_columns_boolean():
    df = pd.DataFrame({"room_type": ["Entire home/apt", "Private room"]})
    result = add_derived_columns(
        df,
        {
            "is_entire_home": {
                "formula": "room_type == 'Entire home/apt'",
                "dtype": "bool",
            }
        },
    )
    assert result["is_entire_home"].tolist() == [True, False]
