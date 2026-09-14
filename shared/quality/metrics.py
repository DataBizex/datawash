"""Reusable data quality metrics for pandas DataFrames."""

from __future__ import annotations

import pandas as pd


def total_rows(df: pd.DataFrame) -> int:
    """Return the total number of rows in the DataFrame."""
    return len(df)


def total_columns(df: pd.DataFrame) -> int:
    """Return the total number of columns in the DataFrame."""
    return len(df.columns)


def missing_per_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Count missing (NaN) values per column with percentage.

    Returns
    -------
    pd.DataFrame
        Columns: column, missing_count, missing_pct
        Sorted by missing_count descending.
    """
    total = len(df)
    counts = df.isna().sum()
    percentages = (counts / total * 100).round(2) if total > 0 else counts * 0
    result = pd.DataFrame(
        {
            "column": counts.index,
            "missing_count": counts.values,
            "missing_pct": percentages.values,
        }
    )
    return result.sort_values("missing_count", ascending=False).reset_index(drop=True)


def duplicate_rows(df: pd.DataFrame, subset: list[str] | None = None) -> int:
    """
    Count rows that are exact duplicates.

    Parameters
    ----------
    subset : list of column names or None
        If provided, only consider these columns when checking duplicates.
        If None, consider all columns.
    """
    return int(df.duplicated(subset=subset).sum())


def column_types_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Group columns by their pandas dtype.

    Returns
    -------
    pd.DataFrame
        Columns: dtype, column_count, columns
    """
    type_map: dict[str, list[str]] = {}
    for col in df.columns:
        dtype_name = str(df[col].dtype)
        type_map.setdefault(dtype_name, []).append(col)

    rows = [
        {"dtype": dtype, "column_count": len(cols), "columns": ", ".join(cols)}
        for dtype, cols in sorted(type_map.items())
    ]
    return pd.DataFrame(rows)


def high_cardinality_columns(df: pd.DataFrame, threshold: int = 100) -> pd.DataFrame:
    """
    Find columns with more distinct values than the threshold.

    Useful for spotting free-text columns disguised as categoricals.
    """
    result = []
    for col in df.columns:
        n_unique = df[col].nunique(dropna=True)
        if n_unique > threshold:
            result.append(
                {
                    "column": col,
                    "unique_count": n_unique,
                    "sample_value": (
                        str(df[col].dropna().iloc[0])
                        if not df[col].dropna().empty
                        else ""
                    ),
                }
            )

    columns = ["column", "unique_count", "sample_value"]
    if not result:
        return pd.DataFrame(columns=columns)

    return (
        pd.DataFrame(result)
        .sort_values("unique_count", ascending=False)
        .reset_index(drop=True)
    )


def numeric_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Statistical summary for numeric columns only.

    Returns
    -------
    pd.DataFrame
        Descriptive statistics: count, mean, std, min, 25%, 50%, 75%, max.
    """
    numeric_df = df.select_dtypes(include="number")
    if numeric_df.empty:
        return pd.DataFrame()
    return numeric_df.describe().transpose().round(2)
