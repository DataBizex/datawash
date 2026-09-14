"""Validate the processed Barcelona Airbnb dataset against data contracts.

Data contracts encode business rules the final data must satisfy.
Unlike unit tests (which test code with synthetic data), these run
against real production output.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

DATAWASH_ROOT = Path(__file__).resolve().parent.parent.parent.parent
SRC_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DATAWASH_ROOT))
sys.path.insert(0, str(SRC_DIR))

from shared.quality.validators import (
    ValidationResult,
    check_allowed_values,
    check_min_rows,
    check_no_nulls,
    check_range,
    check_unique,
    summarize_results,
)
from shared.utils.io import processed_dir, reports_dir
from shared.utils.logging_setup import setup_logger

PROJECT_NAME = "barcelona-airbnb"
PROCESSED_FILENAME = "listings.parquet"
REPORT_FILENAME = "validation.md"

logger = setup_logger(__name__)


ROOM_TYPES = ["Entire home/apt", "Private room", "Shared room", "Hotel room"]


def run_contracts(df: pd.DataFrame) -> list[ValidationResult]:
    """
    Run every business rule against the DataFrame and collect results.
    Contracts are declared in code but could be moved to YAML later.
    """
    return [
        # Row count sanity
        check_min_rows(df, min_rows=1_000),
        # Identifiers
        check_no_nulls(df, "id"),
        check_unique(df, "id"),
        check_no_nulls(df, "host_id"),
        # Location bounds (Barcelona is around 41.3°N, 2.1°E)
        check_range(df, "latitude", min_value=41.0, max_value=41.6),
        check_range(df, "longitude", min_value=1.9, max_value=2.3),
        # Business logic
        check_range(df, "price", min_value=0, max_value=10_000),
        check_range(df, "accommodates", min_value=1, max_value=30),
        check_range(df, "minimum_nights", min_value=1, max_value=365),
        check_allowed_values(df, "room_type", allowed=ROOM_TYPES),
        # Percentages
        check_range(df, "host_response_rate", min_value=0, max_value=100),
        check_range(df, "review_scores_rating", min_value=0, max_value=5),
    ]


def build_report(results: list[ValidationResult]) -> str:
    """Assemble a Markdown report from validation results."""
    from datetime import datetime

    summary_df = summarize_results(results)
    passed_count = int(summary_df["passed"].sum())
    total = len(summary_df)
    generated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines = [
        "# Barcelona Airbnb – Data Contract Validation",
        "",
        f"_Generated: {generated}_",
        "",
        "## Summary",
        "",
        f"- **Total checks:** {total}",
        f"- **Passed:** {passed_count}",
        f"- **Failed:** {total - passed_count}",
        "",
        "## Details",
        "",
        summary_df.to_markdown(index=False),
        "",
    ]

    return "\n".join(lines)


def validate_processed() -> tuple[bool, Path]:
    """
    Run all contracts against the processed dataset.

    Returns
    -------
    (all_passed, report_path)
        all_passed is True only if every contract passed.
        report_path points to the written Markdown report.
    """
    source = processed_dir(PROJECT_NAME) / PROCESSED_FILENAME
    if not source.exists():
        raise FileNotFoundError(
            f"Processed file not found at {source}. Run transform first."
        )

    logger.info(f"Reading processed data from {source.name}")
    df = pd.read_parquet(source)

    logger.info(f"Running data contracts on {len(df):,} rows")
    results = run_contracts(df)

    report_text = build_report(results)
    report_path = reports_dir(PROJECT_NAME) / REPORT_FILENAME
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report_text, encoding="utf-8")

    all_passed = all(r.passed for r in results)
    passed_count = sum(1 for r in results if r.passed)
    total = len(results)

    logger.info(
        f"Validation complete: {passed_count}/{total} contracts passed. "
        f"Report at {report_path}"
    )

    for r in results:
        level = logger.info if r.passed else logger.warning
        level(f"  [{'PASS' if r.passed else 'FAIL'}] {r.name}: {r.message}")

    return all_passed, report_path


if __name__ == "__main__":
    all_passed, path = validate_processed()
    print(f"\nValidation report: {path}")
    print(f"All checks passed: {all_passed}")
    sys.exit(0 if all_passed else 1)
