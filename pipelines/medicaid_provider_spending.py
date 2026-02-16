#!/usr/bin/env python3
"""
Pipeline: Medicaid Provider Spending → BigQuery

Downloads the HHS Medicaid Provider Spending dataset and loads it into BigQuery.

Source: https://opendata.hhs.gov/datasets/medicaid-provider-spending/
Description: Provider-level Medicaid spending data from T-MSIS, aggregated by
    billing/servicing provider, procedure code, and month. Covers fee-for-service,
    managed care, and CHIP claims.

Usage:
    python pipelines/medicaid_provider_spending.py
    python pipelines/medicaid_provider_spending.py --project open-sud --dataset medicaid
    python pipelines/medicaid_provider_spending.py --download-only
    python pipelines/medicaid_provider_spending.py --load-only  # skip download, use existing file
"""

import argparse
import hashlib
import os
import sys
from pathlib import Path

import requests
from google.cloud import bigquery
from tqdm import tqdm

# Dataset metadata
DATASET_URL = "https://stopendataprod.blob.core.windows.net/datasets/medicaid-provider-spending/2026-02-09/medicaid-provider-spending.parquet"
DATASET_SHA256 = "a998e5ae11a391f1eb0d8464b3866a3ee7fe18aa13e56d411c50e72e3a0e35c7"
SOURCE_PAGE = "https://opendata.hhs.gov/datasets/medicaid-provider-spending/"

# Defaults
DEFAULT_PROJECT = "open-sud"
DEFAULT_DATASET = "medicaid"
DEFAULT_TABLE = "provider_spending"
DEFAULT_LOCATION = "US"
DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def download_parquet(dest: Path) -> Path:
    """Download the parquet file with progress bar and checksum verification."""
    dest.parent.mkdir(parents=True, exist_ok=True)

    print(f"Downloading from:\n  {DATASET_URL}")
    print(f"Saving to:\n  {dest}")

    resp = requests.get(DATASET_URL, stream=True, timeout=30)
    resp.raise_for_status()

    total_size = int(resp.headers.get("content-length", 0))
    chunk_size = 8 * 1024 * 1024  # 8 MB chunks

    sha256 = hashlib.sha256()
    with open(dest, "wb") as f, tqdm(
        total=total_size, unit="B", unit_scale=True, desc="Downloading"
    ) as pbar:
        for chunk in resp.iter_content(chunk_size=chunk_size):
            f.write(chunk)
            sha256.update(chunk)
            pbar.update(len(chunk))

    actual_hash = sha256.hexdigest()
    if actual_hash != DATASET_SHA256:
        print(f"WARNING: SHA256 mismatch!")
        print(f"  Expected: {DATASET_SHA256}")
        print(f"  Got:      {actual_hash}")
        print("The dataset may have been updated. Verify at:")
        print(f"  {SOURCE_PAGE}")
    else:
        print("Checksum verified.")

    return dest


def load_to_bigquery(
    parquet_path: Path, project: str, dataset: str, table: str, location: str
) -> None:
    """Load parquet file into BigQuery, replacing existing data."""
    table_id = f"{project}.{dataset}.{table}"

    print(f"Loading into BigQuery: {table_id}")

    client = bigquery.Client(project=project, location=location)

    # Create dataset if it doesn't exist
    dataset_ref = bigquery.Dataset(f"{project}.{dataset}")
    dataset_ref.location = location
    client.create_dataset(dataset_ref, exists_ok=True)

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.PARQUET,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    )

    with open(parquet_path, "rb") as f:
        load_job = client.load_table_from_file(f, table_id, job_config=job_config)

    print("Upload complete. Waiting for BigQuery to process...")
    load_job.result()  # Wait for completion

    table_ref = client.get_table(table_id)
    print(f"Loaded {table_ref.num_rows:,} rows into {table_id}")


def main():
    parser = argparse.ArgumentParser(
        description="Download HHS Medicaid Provider Spending data and load into BigQuery"
    )
    parser.add_argument(
        "--project", default=DEFAULT_PROJECT, help=f"GCP project ID (default: {DEFAULT_PROJECT})"
    )
    parser.add_argument(
        "--dataset", default=DEFAULT_DATASET, help=f"BigQuery dataset (default: {DEFAULT_DATASET})"
    )
    parser.add_argument(
        "--table", default=DEFAULT_TABLE, help=f"BigQuery table (default: {DEFAULT_TABLE})"
    )
    parser.add_argument(
        "--location", default=DEFAULT_LOCATION, help=f"BigQuery location (default: {DEFAULT_LOCATION})"
    )
    parser.add_argument(
        "--data-dir", type=Path, default=DATA_DIR, help="Directory for downloaded files"
    )
    parser.add_argument(
        "--download-only", action="store_true", help="Download file only, skip BigQuery load"
    )
    parser.add_argument(
        "--load-only", action="store_true", help="Skip download, load existing file into BigQuery"
    )
    args = parser.parse_args()

    parquet_path = args.data_dir / "medicaid-provider-spending.parquet"

    # Download
    if not args.load_only:
        if parquet_path.exists():
            print(f"File already exists: {parquet_path}")
            print("Use --load-only to skip download, or delete the file to re-download.")
            resp = input("Re-download? [y/N] ").strip().lower()
            if resp != "y":
                print("Skipping download.")
            else:
                download_parquet(parquet_path)
        else:
            download_parquet(parquet_path)

    if args.download_only:
        print("Done (download only).")
        return

    # Load
    if not parquet_path.exists():
        print(f"ERROR: File not found: {parquet_path}")
        print("Run without --load-only to download first.")
        sys.exit(1)

    load_to_bigquery(parquet_path, args.project, args.dataset, args.table, args.location)
    print("Done.")


if __name__ == "__main__":
    main()
