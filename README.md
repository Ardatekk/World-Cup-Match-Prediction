# FIFA World Cup 2026 Match Prediction

[![Project Status](https://img.shields.io/badge/status-data%20engineering%20complete-green)](#)
[![Python](https://img.shields.io/badge/python-3.x-blue)](#)
[![BeCode](https://img.shields.io/badge/BeCode-team%20project-black)](#)

## Project Overview

This project aims to predict FIFA World Cup 2026 match outcomes using historical international football results, Elo ratings, qualified-team information, FIFA World Cup 2026 fixture data, model prediction outputs, and live match data.

The project is structured as an end-to-end data product. The Data Engineering layer cleans, validates, standardizes, enriches, and exports reusable datasets for modeling, dashboarding, and AI assistant workflows.

Recent additions include live World Cup match ingestion from football-data.org. The pipeline can fetch current match status, scores, kickoff times, and team information, then transform the raw API response into a dashboard-ready processed dataset.

## Project Objectives

- Build a clean and maintainable football match prediction dataset.
- Separate completed historical matches from future fixtures.
- Standardize team names across all input sources.
- Validate FIFA World Cup 2026 team and fixture coverage.
- Enrich World Cup 2026 fixtures with selected team metadata and Elo attributes.
- Produce lean processed datasets that can be reused by feature engineering, modeling, and dashboard workflows.
- Keep data engineering outputs separate from later machine learning features.
- Ingest live World Cup 2026 match data from football-data.org.
- Store raw live API responses separately from processed datasets.
- Transform live match data into a dashboard-ready match status dataset.
- Support scheduled refreshes for overnight match results and upcoming fixture status.

## Data Sources

The project uses five primary data source groups:

| Source | Purpose |
| --- | --- |
| Historical international results | Completed international match results used for training and historical analysis. |
| FIFA World Cup 2026 teams | Qualified team reference data, including group, confederation, FIFA rank, coach, best World Cup result, and debut status. |
| Elo ratings | Historical and latest Elo ratings for qualified teams. |
| FIFA World Cup 2026 fixtures | Group-stage fixtures and knockout-stage placeholder fixtures for the 2026 tournament. |
| football-data.org | Live World Cup match data, including match status, kickoff time, teams, scores, and result updates. |

Raw data is stored under `data/raw/`. Cleaned and reusable outputs are stored under `data/processed/`.

## Project Structure

```text
.
├── data/
│   ├── external/
│   ├── processed/
│   │   ├── elo_history.csv
│   │   ├── elo_latest.csv
│   │   ├── live_matches.csv
│   │   ├── model_training_base.csv
│   │   ├── results_future.csv
│   │   ├── results_historical.csv
│   │   ├── wc_2026_fixtures_enriched.csv
│   │   ├── wc_2026_fixtures_validated.csv
│   │   └── wc_2026_teams_cleaned.csv
│   └── raw/
│       └── live/
│           └── football_data_wc_matches.json
├── dashboard/
│   ├── app.py
│   ├── bracket.py
│   ├── components.py
│   ├── data.py
│   ├── realdata.py
│   └── simulate.py
├── database/
│   └── schema.sql
├── docs/
│   ├── ai_assistant_progress_report.md
│   ├── ai_assistant_report.md
│   ├── dashboard_recommendations.md
│   ├── data_findings.md
│   ├── fixture_enrichment_readiness_report.md
│   ├── modeling_recommendations.md
│   └── processed_data_report.md
├── models/
│   ├── poisson_model.pkl
│   └── xgb_model.pkl
├── notebooks/
│   ├── 00_shared_data_discovery.ipynb
│   ├── 01_de_cleaning_exploration.ipynb
│   └── 03_fixture_enrichment.ipynb
├── requirements/
│   ├── base.txt
│   ├── dashboard.txt
│   ├── de.txt
│   ├── dev.txt
│   └── ds.txt
├── src/
│   ├── assistant/
│   ├── cleaning/
│   │   ├── clean_elo.py
│   │   ├── clean_results.py
│   │   └── standardize_teams.py
│   ├── enrichment/
│   │   └── enrich_fixtures.py
│   ├── export/
│   │   └── build_model_dataset.py
│   ├── extract/
│   │   └── football_data_api.py
│   ├── features/
│   ├── load/
│   ├── transform/
│   │   ├── clean_elo.py
│   │   ├── clean_results.py
│   │   ├── enrich_fixtures.py
│   │   └── live_matches.py
│   └── utils/
├── .github/
│   └── workflows/
│       └── de_pipeline.yml
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

## Data Engineering Pipeline

The current pipeline converts raw football data into validated processed datasets and refreshes live World Cup match data for dashboard use.

```text
Raw data
  |
  v
Data discovery and validation
  |
  v
Team-name standardization
  |
  v
Historical/future result split
  |
  v
Elo history cleaning and latest snapshot creation
  |
  v
World Cup 2026 fixture validation
  |
  v
Fixture enrichment with team metadata and latest Elo ratings
  |
  v
Base model dataset export
  |
  v
Live World Cup match extraction from football-data.org
  |
  v
Live match transformation
  |
  v
Processed datasets for modeling, dashboarding, and assistant workflows
```

### Extract and Transform Scripts

| Script | Purpose | Main outputs |
| --- | --- | --- |
| `src/transform/clean_results.py` | Cleans historical results, standardizes team names, separates completed and future matches, and adds match outcome labels. | `results_historical.csv`, `results_future.csv` |
| `src/transform/clean_elo.py` | Cleans Elo ratings, standardizes country names, validates coverage, and creates the latest Elo snapshot. | `elo_history.csv`, `elo_latest.csv` |
| `src/transform/enrich_fixtures.py` | Enriches all 104 World Cup 2026 fixtures with lean team and Elo metadata while preserving knockout placeholders. | `wc_2026_fixtures_enriched.csv` |
| `src/extract/football_data_api.py` | Fetches World Cup 2026 match data from football-data.org and stores the raw API response. | `data/raw/live/football_data_wc_matches.json` |
| `src/transform/live_matches.py` | Flattens the live API response into a dashboard-ready match status dataset. | `live_matches.csv` |

### Pipeline Entry Point

The root-level `main.py` runs the lightweight Data Engineering pipeline end to end. It uses the pipeline modules under `src/cleaning/`, `src/enrichment/`, `src/export/`, `src/extract/`, and `src/transform/`.

The pipeline currently runs:

1. Clean historical results.
2. Process Elo ratings.
3. Standardize team and fixture references.
4. Enrich World Cup 2026 fixtures.
5. Build the base model dataset.
6. Fetch and transform live World Cup match data from football-data.org.

The live-data step requires `FOOTBALL_DATA_API_KEY`. When the key is available, the pipeline writes the raw API response to `data/raw/live/football_data_wc_matches.json` and the processed output to `data/processed/live_matches.csv`.

## Processed Datasets

| Dataset | Description |
| --- | --- |
| `results_historical.csv` | Completed historical international matches with scores and outcome labels. |
| `results_future.csv` | Future result-style rows separated from the raw results source. Scores are intentionally missing. |
| `elo_history.csv` | Historical Elo ratings for the 48 World Cup 2026 teams. Must be used with time-aware joins. |
| `elo_latest.csv` | Latest Elo snapshot for the 48 qualified teams. Used for fixture enrichment. |
| `wc_2026_teams_cleaned.csv` | Cleaned reference table for all 48 qualified World Cup 2026 teams. |
| `wc_2026_fixtures_validated.csv` | Validated fixture table with group-stage teams and knockout placeholders. |
| `wc_2026_fixtures_enriched.csv` | Lean enriched fixture dataset containing all 104 fixtures, selected team metadata, and selected Elo attributes. |
| `model_training_base.csv` | Lightweight base modeling export from completed historical matches. This is not feature-engineered yet. |
| `live_matches.csv` | Dashboard-ready live World Cup match data from football-data.org, including match status, kickoff date/time, teams, scores, and score display fields. |

The main enriched fixture output keeps all 104 fixtures:

- 72 known group-stage fixtures include team and Elo metadata.
- 32 knockout-stage placeholder fixtures remain present with null team/Elo metadata.
- No engineered ML features are included in this file.

More detailed dataset profiling is available in:

- `docs/data_findings.md`
- `docs/fixture_enrichment_readiness_report.md`
- `docs/processed_data_report.md`

## Live Match Data

Live World Cup match data is fetched from football-data.org.

Raw API output:

```text
data/raw/live/football_data_wc_matches.json
```

Processed output:

```text
data/processed/live_matches.csv
```

The processed live match dataset includes Streamlit-ready columns such as:

- `match_date`
- `kickoff_time_utc`
- `status`
- `is_finished`
- `is_scheduled`
- `has_score`
- `home_team`
- `away_team`
- `home_score`
- `away_score`
- `score_display`

Future matches can have null score fields. Knockout placeholder matches can have null team fields. These null values are expected and should be handled by dashboard logic.

## Current Project Status

The core Data Engineering pipeline is complete and has been extended with live match ingestion.

Completed work:

- Raw data discovery and documentation.
- Historical results cleaning.
- Future fixture separation from historical results.
- Team-name standardization across datasets.
- Elo history cleaning and latest snapshot creation.
- World Cup 2026 team reference validation.
- World Cup 2026 fixture validation.
- Lean fixture enrichment.
- Base model dataset export.
- Live World Cup match extraction from football-data.org.
- Live match transformation into `live_matches.csv`.
- GitHub Actions pipeline support for scheduled refreshes.
- Processed dataset documentation.

The project now supports modeling, dashboarding, and AI assistant workflows.

## Next Steps

The next phase should focus on creating modeling-ready features from the processed datasets.

Recommended next steps:

- Build feature engineering scripts under `src/features/`.
- Create team-level and match-level features from historical results and Elo history.
- Use time-aware joins to avoid data leakage.
- Keep model features separate from raw enrichment outputs.
- Define train/test validation strategy.
- Prepare modeling datasets for Data Science workflows.
- Add automated validation checks for feature outputs.
- Document feature definitions and assumptions.
- Integrate `live_matches.csv` into the Streamlit dashboard as the source for latest results, upcoming matches, match status, and live scores.
- Use live match status to distinguish finished, scheduled, and future matches in dashboard views.
- Add validation checks for `live_matches.csv` schema and expected null values.
- Keep API-based live data separate from static fixture enrichment outputs.

Model selection and detailed model evaluation should happen after the feature engineering layer is defined.

## How to Run the Project

### 1. Clone the repository

```bash
git clone <repository-url>
cd World-Cup-Match-Prediction
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a local `.env` file from `.env.example`:

```bash
cp .env.example .env
```

Add your football-data.org API token:

```text
FOOTBALL_DATA_API_KEY=your_api_token_here
```

The `.env` file is ignored by Git and must not be committed.

### 5. Run the Data Engineering pipeline

The full lightweight Data Engineering pipeline can be run from the project root:

```bash
python main.py
```

This runs the cleaning, team/fixture standardization, fixture enrichment, base modeling export, and live World Cup match refresh steps.

If your environment does not expose `python`, use:

```bash
.venv/bin/python main.py
```

### 6. Run individual Data Engineering transforms

Clean historical results:

```bash
python src/transform/clean_results.py
```

Clean Elo ratings:

```bash
python src/transform/clean_elo.py
```

Create the lean enriched fixture dataset:

```bash
python src/transform/enrich_fixtures.py
```

Expected enriched output:

```text
data/processed/wc_2026_fixtures_enriched.csv
```

Fetch live World Cup match data:

```bash
python src/extract/football_data_api.py
```

Transform live World Cup match data:

```bash
python src/transform/live_matches.py
```

Expected live output:

```text
data/processed/live_matches.csv
```

### 7. Explore notebooks

Notebook-based discovery and validation work is available in:

```text
notebooks/
```

Run notebooks with:

```bash
jupyter notebook
```

## GitHub Actions Automation

The Data Engineering pipeline is automated with GitHub Actions.

Workflow:

```text
.github/workflows/de_pipeline.yml
```

The workflow runs:

- on manual dispatch
- on relevant pushes to `main`
- on a daily schedule

Current schedule:

```text
06:00 UTC daily
08:00 Belgium time during summer
```

The scheduled run is intended to refresh World Cup results and match status after overnight matches.

The workflow requires the following GitHub repository secret:

```text
FOOTBALL_DATA_API_KEY
```

This secret is passed to `main.py` during the live-data extraction step. The API token should never be committed to the repository.

## Dashboard Data Availability

The dashboard can consume both static prediction datasets and refreshed live match data.

Relevant dashboard-ready datasets:

| Dataset | Dashboard use |
| --- | --- |
| `wc_2026_teams_cleaned.csv` | Team profiles, groups, confederations, FIFA ranks. |
| `elo_latest.csv` | Team strength, Elo-based comparisons, dashboard KPIs. |
| `wc_2026_fixtures_enriched.csv` | Fixture context, venues, cities, team metadata, Elo context. |
| `predictions_2026.csv` | Group-stage model probabilities for match prediction cards. |
| `live_matches.csv` | Latest match status, scores, kickoff times, and live/upcoming match display. |

`live_matches.csv` should be used by the frontend as the preferred source for current match status and score display.

## Technologies Used

- Python
- Pandas
- NumPy
- Requests
- python-dotenv
- Jupyter Notebook
- SQL / database schema planning
- Git and GitHub
- GitHub Actions
- Streamlit
- football-data.org API
- Airflow / scheduling tooling for local orchestration experiments

## Notes

- `wc_2026_fixtures_enriched.csv` is an enrichment output, not a feature-engineered modeling dataset.
- Knockout-stage placeholders are expected and intentionally retained.
- Historical Elo data must be joined with date cutoffs during future feature engineering to avoid leakage.
- Processed datasets are versioned so team members can work from the same Data Engineering outputs.
- `.env` files are ignored and should be used for local secrets only.
- `FOOTBALL_DATA_API_KEY` must be configured locally or as a GitHub Actions repository secret for live-data extraction.
- `live_matches.csv` is a live-data output for dashboard status and score display.
- Future live matches can have null score fields.
- Knockout placeholder matches can have null team fields.
