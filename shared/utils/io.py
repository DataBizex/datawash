"""Path helpers for locating data files consistently across modules."""

from pathlib import Path


def project_root(project_name: str) -> Path:
    """
    Return the root folder of a specific project inside datawash.

    Parameters
    ----------
    project_name : str
        The folder name of the project (e.g., 'barcelona-airbnb').

    Returns
    -------
    Path
        Absolute path to the project's root folder.
    """
    # This file is at: datawash/shared/utils/io.py
    # datawash root is 2 levels up from here
    datawash_root = Path(__file__).resolve().parent.parent.parent
    return datawash_root / project_name


def raw_dir(project_name: str) -> Path:
    """Return the raw data folder for a project."""
    return project_root(project_name) / "data" / "raw"


def interim_dir(project_name: str) -> Path:
    """Return the interim data folder for a project."""
    return project_root(project_name) / "data" / "interim"


def processed_dir(project_name: str) -> Path:
    """Return the processed data folder for a project."""
    return project_root(project_name) / "data" / "processed"


def reports_dir(project_name: str) -> Path:
    """Return the reports folder for a project."""
    return project_root(project_name) / "reports"
