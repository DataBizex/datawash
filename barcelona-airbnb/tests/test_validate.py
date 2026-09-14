"""Tests for the validate module and shared validators."""

import pandas as pd
import pytest
from shared.quality.validators import (
    check_allowed_values,
    check_min_rows,
    check_no_nulls,
    check_range,
    check_unique,
)


def test_check_no_nulls_passes_on_clean_column():
    df = pd.DataFrame({"a": [1, 2, 3]})
    result = check_no_nulls(df, "a")
    assert result.passed
    assert result.failing_rows == 0


def test_check_no_nulls_fails_on_missing_values():
    df = pd.DataFrame({"a": [1, None, 3]})
    result = check_no_nulls(df, "a")
    assert not result.passed
    assert result.failing_rows == 1


def test_check_unique_passes_when_all_distinct():
    df = pd.DataFrame({"id": [1, 2, 3]})
    result = check_unique(df, "id")
    assert result.passed


def test_check_unique_fails_on_duplicates():
    df = pd.DataFrame({"id": [1, 2, 2, 3]})
    result = check_unique(df, "id")
    assert not result.passed
    assert result.failing_rows == 1


def test_check_range_passes_within_bounds():
    df = pd.DataFrame({"price": [10, 50, 100]})
    result = check_range(df, "price", min_value=0, max_value=1000)
    assert result.passed


def test_check_range_fails_below_min():
    df = pd.DataFrame({"price": [-5, 50, 100]})
    result = check_range(df, "price", min_value=0, max_value=1000)
    assert not result.passed
    assert result.failing_rows == 1


def test_check_range_fails_above_max():
    df = pd.DataFrame({"price": [10, 50, 10_000]})
    result = check_range(df, "price", min_value=0, max_value=1000)
    assert not result.passed


def test_check_allowed_values_passes():
    df = pd.DataFrame({"type": ["a", "b", "a"]})
    result = check_allowed_values(df, "type", allowed=["a", "b"])
    assert result.passed


def test_check_allowed_values_fails_on_invalid():
    df = pd.DataFrame({"type": ["a", "b", "c"]})
    result = check_allowed_values(df, "type", allowed=["a", "b"])
    assert not result.passed
    assert result.failing_rows == 1


def test_check_min_rows_passes():
    df = pd.DataFrame({"a": range(100)})
    result = check_min_rows(df, min_rows=50)
    assert result.passed


def test_check_min_rows_fails():
    df = pd.DataFrame({"a": range(10)})
    result = check_min_rows(df, min_rows=50)
    assert not result.passed
