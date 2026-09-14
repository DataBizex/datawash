"""Reusable data validation functions returning boolean pass/fail with details."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass
class ValidationResult:
    """Outcome of a single validation check."""

    name: str
    passed: bool
    message: str
    failing_rows: int = 0


def check_no_nulls(df: pd.DataFrame, column: str) -> ValidationResult:
    """Column must have zero null values."""
    if column not in df.columns:
        return ValidationResult(
            name=f"no_nulls[{column}]",
            passed=False,
            message=f"Column '{column}' not in DataFrame",
        )
    null_count = int(df[column].isna().sum())
    return ValidationResult(
        name=f"no_nulls[{column}]",
        passed=null_count == 0,
        message=f"{null_count} null values" if null_count > 0 else "no nulls",
        failing_rows=null_count,
    )


def check_unique(df: pd.DataFrame, column: str) -> ValidationResult:
    """Column values must be unique across all rows."""
    if column not in df.columns:
        return ValidationResult(
            name=f"unique[{column}]",
            passed=False,
            message=f"Column '{column}' not in DataFrame",
        )
    dup_count = int(df[column].duplicated().sum())
    return ValidationResult(
        name=f"unique[{column}]",
        passed=dup_count == 0,
        message=f"{dup_count} duplicated values" if dup_count > 0 else "all unique",
        failing_rows=dup_count,
    )


def check_range(
    df: pd.DataFrame,
    column: str,
    min_value: float | None = None,
    max_value: float | None = None,
) -> ValidationResult:
    """Numeric column values must fall between min_value and max_value (inclusive)."""
    if column not in df.columns:
        return ValidationResult(
            name=f"range[{column}]",
            passed=False,
            message=f"Column '{column}' not in DataFrame",
        )

    series = pd.to_numeric(df[column], errors="coerce").dropna()
    failing = pd.Series(False, index=series.index)

    if min_value is not None:
        failing = failing | (series < min_value)
    if max_value is not None:
        failing = failing | (series > max_value)

    failing_count = int(failing.sum())
    bounds = f"[{min_value if min_value is not None else '-inf'}, {max_value if max_value is not None else '+inf'}]"
    return ValidationResult(
        name=f"range[{column}]",
        passed=failing_count == 0,
        message=(
            f"{failing_count} values outside {bounds}"
            if failing_count > 0
            else f"all within {bounds}"
        ),
        failing_rows=failing_count,
    )


def check_allowed_values(
    df: pd.DataFrame, column: str, allowed: list
) -> ValidationResult:
    """Column values must be from the allowed list."""
    if column not in df.columns:
        return ValidationResult(
            name=f"allowed_values[{column}]",
            passed=False,
            message=f"Column '{column}' not in DataFrame",
        )

    invalid = df[~df[column].isin(allowed) & df[column].notna()]
    failing_count = len(invalid)
    return ValidationResult(
        name=f"allowed_values[{column}]",
        passed=failing_count == 0,
        message=(
            f"{failing_count} values not in allowed set"
            if failing_count > 0
            else "all allowed"
        ),
        failing_rows=failing_count,
    )


def check_min_rows(df: pd.DataFrame, min_rows: int) -> ValidationResult:
    """DataFrame must have at least min_rows rows."""
    return ValidationResult(
        name=f"min_rows[{min_rows}]",
        passed=len(df) >= min_rows,
        message=(
            f"{len(df):,} rows"
            if len(df) >= min_rows
            else f"only {len(df):,} rows (min {min_rows:,})"
        ),
    )


def summarize_results(results: list[ValidationResult]) -> pd.DataFrame:
    """Turn a list of ValidationResults into a summary DataFrame."""
    return pd.DataFrame(
        [
            {
                "check": r.name,
                "passed": r.passed,
                "message": r.message,
                "failing_rows": r.failing_rows,
            }
            for r in results
        ]
    )
