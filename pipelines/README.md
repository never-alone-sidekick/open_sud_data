# Pipelines

ETL pipelines that download public datasets and load them into BigQuery.

## Available Pipelines

### Medicaid Provider Spending

**Script:** `medicaid_provider_spending.py`
**Source:** [HHS Open Data — Medicaid Provider Spending](https://opendata.hhs.gov/datasets/medicaid-provider-spending/)
**BigQuery table:** `medicaid.provider_spending`

Provider-level Medicaid spending data from T-MSIS (Transformed Medicaid Statistical Information System), aggregated by billing/servicing provider, procedure code, and month. Covers fee-for-service, managed care, and CHIP claims from January 2018 through December 2024.

**~227 million rows | ~2.9 GB Parquet download**

```bash
# Full pipeline: download + load into BigQuery
python pipelines/medicaid_provider_spending.py

# Download only (no BigQuery load)
python pipelines/medicaid_provider_spending.py --download-only

# Load only (skip download, use existing file in data/)
python pipelines/medicaid_provider_spending.py --load-only

# Override defaults
python pipelines/medicaid_provider_spending.py --project my-project --dataset my_dataset --table my_table
```

| Option | Default | Description |
|--------|---------|-------------|
| `--project` | `open-sud` | GCP project ID |
| `--dataset` | `medicaid` | BigQuery dataset name |
| `--table` | `provider_spending` | BigQuery table name |
| `--location` | `US` | BigQuery location |
| `--data-dir` | `./data` | Local directory for downloaded files |
| `--download-only` | — | Download the file but don't load into BigQuery |
| `--load-only` | — | Skip download, load existing local file |

## How Pipelines Work

Each pipeline follows the same pattern:

1. **Download** the raw data (usually Parquet or CSV) from a public URL
2. **Verify** the file checksum against a known hash
3. **Create** the BigQuery dataset if it doesn't exist
4. **Load** the data into BigQuery using `WRITE_TRUNCATE` (full replace — safe to re-run)

Pipelines are **idempotent** — running them again replaces the table with fresh data.

Downloaded files land in `data/` which is gitignored (files are too large to commit). The pipeline scripts themselves are the reproducible record of how data was sourced.

## Adding a New Pipeline

Use `medicaid_provider_spending.py` as a template. Each pipeline should:

1. **Define source metadata** at the top of the file:
   - `DATASET_URL` — Direct download link
   - `DATASET_SHA256` — Checksum for verification
   - `SOURCE_PAGE` — Human-readable source page URL

2. **Support CLI arguments** for `--project`, `--dataset`, `--table`, and `--download-only` / `--load-only`

3. **Be self-contained** — a single `python pipelines/<name>.py` should do everything

4. **Document the dataset** — add it to this README and the project README with table schema

### Template structure

```python
#!/usr/bin/env python3
"""
Pipeline: <Dataset Name> → BigQuery

<One-line description of what this data is.>

Source: <URL to the source page>

Usage:
    python pipelines/<name>.py
"""

DATASET_URL = "https://..."
DATASET_SHA256 = "..."
SOURCE_PAGE = "https://..."

DEFAULT_PROJECT = "open-sud"
DEFAULT_DATASET = "<dataset_name>"
DEFAULT_TABLE = "<table_name>"

# ... download, verify, load functions ...
```

## Prerequisites

- Python dependencies: `pip install -r requirements.txt`
- GCP auth: `gcloud auth application-default login`
- BigQuery API enabled on your GCP project
