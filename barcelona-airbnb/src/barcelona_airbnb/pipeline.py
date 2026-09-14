"""End-to-end pipeline for the Barcelona Airbnb data quality project.

Executes: extract → profile-before → clean → transform → profile-after → validate.

Exit code 0 if everything succeeds and all validations pass.
Exit code 1 if any validation fails.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

DATAWASH_ROOT = Path(__file__).resolve().parent.parent.parent.parent
SRC_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DATAWASH_ROOT))
sys.path.insert(0, str(SRC_DIR))

from barcelona_airbnb.clean import clean_and_save
from barcelona_airbnb.profile import profile_processed, profile_raw
from barcelona_airbnb.transform import transform_and_save
from barcelona_airbnb.validate import validate_processed
from shared.utils.logging_setup import setup_logger

logger = setup_logger(__name__)


def run_pipeline() -> int:
    """
    Run the full pipeline and return an exit code.

    Returns
    -------
    int
        0 if all stages succeeded and validations passed.
        1 if any validation failed.
    """
    stages = [
        ("profile-before", profile_raw),
        ("clean", clean_and_save),
        ("transform", transform_and_save),
        ("profile-after", profile_processed),
    ]

    logger.info("=" * 60)
    logger.info("Starting Barcelona Airbnb data pipeline")
    logger.info("=" * 60)

    pipeline_start = time.time()

    for stage_name, stage_fn in stages:
        stage_start = time.time()
        logger.info(f"--- Stage: {stage_name} ---")
        try:
            stage_fn()
        except Exception as exc:
            logger.error(f"Stage '{stage_name}' failed: {exc}")
            return 1
        elapsed = time.time() - stage_start
        logger.info(f"Stage '{stage_name}' completed in {elapsed:.2f}s")

    logger.info("--- Stage: validate ---")
    try:
        all_passed, _ = validate_processed()
    except Exception as exc:
        logger.error(f"Validation stage failed: {exc}")
        return 1

    total_elapsed = time.time() - pipeline_start
    logger.info("=" * 60)
    logger.info(f"Pipeline finished in {total_elapsed:.2f}s")
    logger.info(f"All validations passed: {all_passed}")
    logger.info("=" * 60)

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(run_pipeline())
