"""Build human-readable quality reports from metric DataFrames."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pandas as pd


def build_markdown_report(
    title: str,
    total_rows: int,
    total_columns: int,
    missing_df: pd.DataFrame,
    duplicate_count: int,
    type_summary: pd.DataFrame,
    high_cardinality: pd.DataFrame,
    numeric_stats: pd.DataFrame,
    top_n_missing: int = 20,
) -> str:
    """
    Assemble a Markdown quality report from metric DataFrames.

    Parameters
    ----------
    title : str
        Report title, e.g. 'Barcelona Airbnb – Raw Data Quality'.
    top_n_missing : int
        How many columns to show in the missing values table.

    Returns
    -------
    str
        Full Markdown text ready to write to disk.
    """
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines: list[str] = [
        f"# {title}",
        "",
        f"_Generated: {generated_at}_",
        "",
        "## Overview",
        "",
        f"- **Total rows:** {total_rows:,}",
        f"- **Total columns:** {total_columns}",
        f"- **Exact duplicate rows:** {duplicate_count:,}",
        "",
        f"## Missing Values (Top {top_n_missing})",
        "",
    ]

    if missing_df.empty:
        lines.append("_No missing values detected._")
    else:
        top_missing = missing_df.head(top_n_missing)
        lines.append(top_missing.to_markdown(index=False))
    lines.append("")

    lines.extend(
        [
            "## Column Types",
            "",
            (
                type_summary.to_markdown(index=False)
                if not type_summary.empty
                else "_None._"
            ),
            "",
            "## High-Cardinality Columns (>100 unique values)",
            "",
            (
                high_cardinality.to_markdown(index=False)
                if not high_cardinality.empty
                else "_None._"
            ),
            "",
            "## Numeric Column Statistics",
            "",
            (
                numeric_stats.to_markdown()
                if not numeric_stats.empty
                else "_No numeric columns._"
            ),
            "",
        ]
    )

    return "\n".join(lines)


def write_report(content: str, output_path: Path) -> None:
    """Write the report content to disk, creating parent folders if needed."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")
