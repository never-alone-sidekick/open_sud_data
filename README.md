# Open SUD Data

Open-source tools for collecting, processing, and visualizing publicly available data on **substance use disorder (SUD)** in the United States and beyond.

Built by [Sober Sidekick](https://sobersidekick.com) to make public health data more accessible and actionable.

## Architecture

```
opendata.hhs.gov          BigQuery (open-sud)          Dash App
CDC WONDER         →    pipelines/    →    medicaid.provider_spending    →    localhost:8050
SAMHSA, etc.             (ETL)              (+ future tables)                 (visualizations)
```

**Data flows through three stages:**

1. **Collect** — Pipelines download raw data from public sources (HHS, CDC, SAMHSA, etc.)
2. **Store** — Data is loaded into Google BigQuery for fast, scalable querying
3. **Visualize** — A Dash web app and Jupyter notebooks surface insights

## Project Structure

```
open_sud_data/
├── pipelines/          # ETL scripts — download public data → load into BigQuery
├── scrapers/           # Web scrapers for sources without direct downloads
├── notebooks/          # Jupyter notebooks for exploration and analysis
├── app/                # Dash (Plotly) web app for interactive visualizations
├── config/             # Configuration templates (.env.example)
├── data/               # Local data cache (gitignored — large files stay local)
└── requirements.txt    # Python dependencies
```

## Getting Started

### Prerequisites

- **Python 3.11+**
- **Google Cloud SDK** (`gcloud`) — [install guide](https://cloud.google.com/sdk/docs/install)
- A **GCP project** with BigQuery enabled (default: `open-sud`)

### 1. Clone and install

```bash
git clone https://github.com/jordansidekick/open_sud_data.git
cd open_sud_data

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Authenticate with Google Cloud

The pipelines need BigQuery access. Authenticate using Application Default Credentials:

```bash
gcloud auth application-default login
```

This opens a browser for Google login. Make sure to **grant all requested permissions** (including the `cloud-platform` scope). Your credentials are stored locally at `~/.config/gcloud/application_default_credentials.json`.

> **Alternative:** If using a service account, set the path in your `.env`:
> ```
> GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json
> ```

### 3. Configure environment

```bash
cp config/.env.example .env
# Edit .env with your project settings if they differ from defaults
```

### 4. Run a pipeline

```bash
# Download and load the Medicaid Provider Spending dataset (~2.9 GB)
python pipelines/medicaid_provider_spending.py
```

See [pipelines/README.md](pipelines/README.md) for all available pipelines and options.

### 5. Query data in BigQuery

Once loaded, you can query directly in BigQuery:

```sql
-- Total Medicaid spending by year
SELECT
  SUBSTR(CLAIM_FROM_MONTH, 1, 4) AS year,
  SUM(TOTAL_PAID) AS total_spending,
  SUM(TOTAL_CLAIMS) AS total_claims,
  SUM(TOTAL_UNIQUE_BENEFICIARIES) AS total_beneficiaries
FROM medicaid.provider_spending
GROUP BY year
ORDER BY year;
```

### 6. Run the Dash app

```bash
python app/app.py
# Open http://localhost:8050
```

### 7. Explore with notebooks

```bash
jupyter notebook notebooks/
```

## Datasets

### Currently loaded

| Dataset | BigQuery Table | Source | Records | Coverage |
|---------|---------------|--------|---------|----------|
| Medicaid Provider Spending | `medicaid.provider_spending` | [HHS Open Data](https://opendata.hhs.gov/datasets/medicaid-provider-spending/) | ~227M rows | Jan 2018 – Dec 2024 |

#### `medicaid.provider_spending` schema

| Column | Type | Description |
|--------|------|-------------|
| `BILLING_PROVIDER_NPI_NUM` | STRING | National Provider Identifier for the billing provider |
| `SERVICING_PROVIDER_NPI_NUM` | STRING | National Provider Identifier for the servicing provider |
| `HCPCS_CODE` | STRING | Healthcare Common Procedure Coding System code |
| `CLAIM_FROM_MONTH` | STRING | Month the claim originated (e.g. `2024-01`) |
| `TOTAL_UNIQUE_BENEFICIARIES` | INT64 | Count of unique Medicaid beneficiaries |
| `TOTAL_CLAIMS` | INT64 | Total number of claims filed |
| `TOTAL_PAID` | FLOAT64 | Total dollar amount paid |

### Planned data sources

- **SAMHSA** — Treatment facility locator and NSDUH survey data
- **CDC WONDER** — Overdose mortality and morbidity
- **DEA ARCOS** — Controlled substance distribution
- **TEDS** — Treatment admissions and discharges
- **WHO** — Global substance use statistics

## BigQuery Setup

| Setting | Value |
|---------|-------|
| GCP Project | `open-sud` |
| Location | `US` |
| Dataset | `medicaid` (more datasets added as pipelines grow) |

All pipelines create their BigQuery dataset automatically on first run. No manual setup needed beyond authentication.

## Contributing

We welcome contributions! Here's how to add value:

### Adding a new data source

1. Create a new pipeline in `pipelines/` (use `medicaid_provider_spending.py` as a template)
2. Add an entry to the dataset table in this README and in `pipelines/README.md`
3. Open a PR with a summary of what the data covers and why it's useful

### Branch naming

- `feature/*` — New features or data sources
- `fix/*` — Bug fixes
- `docs/*` — Documentation updates

### PR checklist

- [ ] No hardcoded secrets or API keys
- [ ] Pipeline is idempotent (safe to re-run)
- [ ] BigQuery table/dataset names documented
- [ ] README updated with new dataset details

## License

MIT License — see [LICENSE](LICENSE) for details.
