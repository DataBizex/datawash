"""Profile raw Barcelona Airbnb data and produce a quality baseline report."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

# Import path setup
DATAWASH_ROOT = Path(__file__).resolve().parent.parent.parent.parent
SRC_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DATAWASH_ROOT))
sys.path.insert(0, str(SRC_DIR))

from barcelona_airbnb.extract import extract_listings
from shared.quality.metrics import (
    column_types_summary,
    duplicate_rows,
    high_cardinality_columns,
    missing_per_column,
    numeric_summary,
    total_columns,
    total_rows,
)
from shared.quality.report import build_markdown_report, write_report
from shared.utils.io import reports_dir
from shared.utils.logging_setup import setup_logger

PROJECT_NAME = "barcelona-airbnb"
REPORT_FILENAME = "quality_baseline.md"

logger = setup_logger(__name__)


def profile_dataframe(df: pd.DataFrame, title: str = "Raw Data Quality") -> str:
    """
    Compute all quality metrics for a DataFrame and return a Markdown report.
    """
    logger.info("Computing quality metrics...")

    missing_df = missing_per_column(df)
    dup_count = duplicate_rows(df)
    type_summary = column_types_summary(df)
    high_card = high_cardinality_columns(df)
    numeric_stats = numeric_summary(df)

    logger.info(
        f"Metrics: {missing_df['missing_count'].sum():,} total missing cells, "
        f"{dup_count:,} duplicate rows"
    )

    return build_markdown_report(
        title=title,
        total_rows=total_rows(df),
        total_columns=total_columns(df),
        missing_df=missing_df,
        duplicate_count=dup_count,
        type_summary=type_summary,
        high_cardinality=high_card,
        numeric_stats=numeric_stats,
    )


def profile_raw() -> Path:
    """
    Run the full profiling pipeline on the raw listings file.

    Returns
    -------
    Path
        Location of the written report.
    """
    df = extract_listings()
    report_text = profile_dataframe(
        df, title="Barcelona Airbnb – Raw Data Quality Baseline"
    )

    output_path = reports_dir(PROJECT_NAME) / REPORT_FILENAME
    write_report(report_text, output_path)
    logger.info(f"Report written to: {output_path}")

    return output_path


if __name__ == "__main__":
    output = profile_raw()
    print(f"\nReport saved: {output}")


def profile_processed() -> Path:
    """Profile the final processed dataset and write an after-cleaning report."""
    import pandas as pd
    from shared.utils.io import processed_dir

    processed_path = processed_dir(PROJECT_NAME) / "listings.parquet"
    if not processed_path.exists():
        raise FileNotFoundError(
            f"Processed file not found at {processed_path}. Run transform first."
        )

    logger.info(f"Reading processed data from {processed_path.name}")
    df = pd.read_parquet(processed_path)

    report_text = profile_dataframe(
        df,
        title="Barcelona Airbnb – Processed Data Quality (After Cleaning)",
    )

    output_path = reports_dir(PROJECT_NAME) / "quality_processed.md"
    write_report(report_text, output_path)
    logger.info(f"Report written to: {output_path}")

    return output_path
