# Open SUD Data

Open-source tools for collecting, processing, and visualizing publicly available data on **substance use disorder (SUD)** in the United States and beyond.

Built by [Sober Sidekick](https://sobersidekick.com) to make public health data more accessible and actionable.

## What's in this repo

| Directory | Purpose |
|-----------|---------|
| `scrapers/` | Scripts to collect data from open public databases (SAMHSA, CDC WONDER, NSDUH, etc.) |
| `pipelines/` | ETL pipelines to load and transform data into BigQuery |
| `notebooks/` | Jupyter notebooks for data exploration and analysis |
| `app/` | Dash (Plotly) web application for interactive data visualization |
| `data/` | Local data directory (large files gitignored — see pipelines for BigQuery) |
| `config/` | Configuration templates |

## Getting started

### Prerequisites

- Python 3.11+
- Google Cloud project with BigQuery enabled (for pipeline/storage features)

### Setup

```bash
# Clone the repo
git clone https://github.com/jordansidekick/open_sud_data.git
cd open_sud_data

# Create a virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy and configure environment variables
cp config/.env.example .env
```

### Run the Dash app

```bash
python app/app.py
```

Open [http://localhost:8050](http://localhost:8050) in your browser.

### Run a scraper

```bash
python -m scrapers.<scraper_name>
```

### Run notebooks

```bash
jupyter notebook notebooks/
```

## Data sources

This project pulls from publicly available datasets including:

- **SAMHSA** — Substance Abuse and Mental Health Services Administration
- **CDC WONDER** — Wide-ranging Online Data for Epidemiologic Research
- **NSDUH** — National Survey on Drug Use and Health
- **DEA ARCOS** — Automation of Reports and Consolidated Orders System
- **TEDS** — Treatment Episode Data Set
- **WHO** — World Health Organization global substance use data

## Contributing

We welcome contributions! Whether it's adding a new data source, improving visualizations, or fixing bugs — feel free to open an issue or submit a PR.

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/new-data-source`)
3. Commit your changes
4. Open a pull request

## License

MIT License — see [LICENSE](LICENSE) for details.
