# datawash

A collection of data cleaning and data quality projects, each focused on a real-world industry and country context.

## Projects

- **barcelona-airbnb** — Data quality pipeline for Barcelona short-term rental listings (tourism sector, Spain).

## Approach

Each project follows a modular, testable, production-oriented structure:

- Separated extract, profile, clean, transform, validate, and orchestrate modules
- Data contract testing with pytest
- Configuration in YAML, not hard-coded
- Quality reports before and after processing
- Reproducible with a single command

## Shared Utilities

The shared/ directory contains reusable modules used across projects, including quality metrics, validators, and reporting helpers.

## Author

Ali Soltanhosseini
[a.soltanhosseini@gmail.com](mailto:a.soltanhosseini@gmail.com)
[LinkedIn](https://www.linkedin.com/in/ali-soltanhosseini-aut/) | [databizex.com](https://databizex.com)