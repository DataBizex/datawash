"""Tests for the profile module."""

import pandas as pd
import pytest
from barcelona_airbnb.profile import profile_dataframe


@pytest.fixture
def sample_df() -> pd.DataFrame:
    """A tiny synthetic DataFrame with known quality issues."""
    return pd.DataFrame(
        {
            "id": [1, 2, 3, 4, 5],
            "name": ["Loft", "Studio", None, "Room", "Room"],
            "price": [100.0, 150.0, None, 80.0, 80.0],
            "neighbourhood": ["Eixample", "Gracia", "Eixample", "Gracia", "Gracia"],
        }
    )


def test_profile_returns_string(sample_df):
    """profile_dataframe should return a Markdown string."""
    report = profile_dataframe(sample_df, title="Test")
    assert isinstance(report, str)
    assert len(report) > 0


def test_profile_contains_title(sample_df):
    """The report should include the given title as a heading."""
    report = profile_dataframe(sample_df, title="My Custom Title")
    assert "# My Custom Title" in report


def test_profile_reports_row_count(sample_df):
    """The report should mention the correct row count."""
    report = profile_dataframe(sample_df, title="Test")
    assert "5" in report


def test_profile_flags_missing_values(sample_df):
    """The report should include the missing values section."""
    report = profile_dataframe(sample_df, title="Test")
    assert "Missing Values" in report


def test_profile_handles_empty_dataframe():
    """The profiler should not crash on an empty DataFrame."""
    empty = pd.DataFrame(columns=["a", "b"])
    report = profile_dataframe(empty, title="Empty")
    assert isinstance(report, str)


pythonpath = ["src", ".."]
