# Football Match Prediction Project (FIFA World Cup 2026)

[![Project Status](https://img.shields.io/badge/status-work%20in%20progress-yellow)](#)
[![Python](https://img.shields.io/badge/python-3.x-blue)](#)
[![BeCode](https://img.shields.io/badge/BeCode-team%20project-black)](#)
[![License](https://img.shields.io/badge/license-TBD-lightgrey)](#)

## Project Overview

This project is a BeCode team project focused on building an end-to-end football match prediction system for the FIFA World Cup 2026.

The goal is to combine Data Engineering, Data Science, and Data Analytics workflows into one complete project. The system will collect and clean historical football data, engineer useful match and team-level features, train machine learning models, and present predictions and insights through a Streamlit dashboard.

This project is currently **Work in Progress**.

## Objectives

- Collect historical football and FIFA World Cup data.
- Clean, transform, and structure raw datasets.
- Engineer features relevant to match outcome prediction.
- Store processed data in a database.
- Train and evaluate machine learning models.
- Predict FIFA World Cup 2026 match outcomes.
- Visualize team statistics and predictions in a Streamlit dashboard.
- Build a maintainable team project structure suitable for portfolio presentation.

## Architecture Overview

```text
Raw Data Sources
      |
      v
Data Scraping / Collection
      |
      v
Data Cleaning
      |
      v
Feature Engineering
      |
      v
Database Storage
      |
      v
Model Training & Evaluation
      |
      v
Prediction Pipeline
      |
      v
Streamlit Dashboard
```

## Repository Structure

```text
.
├── airflow/
│   └── .gitkeep
├── dashboard/
│   └── .gitkeep
├── data/
│   ├── external/
│   │   └── .gitkeep
│   ├── processed/
│   │   └── .gitkeep
│   └── raw/
│       └── .gitkeep
├── database/
│   └── schema.sql
├── models/
│   └── .gitkeep
├── notebooks/
│   └── .gitkeep
├── requirements/
│   ├── base.txt
│   ├── dashboard.txt
│   ├── de.txt
│   ├── dev.txt
│   └── ds.txt
├── src/
│   ├── extract/
│   │   └── .gitkeep
│   ├── features/
│   │   └── .gitkeep
│   ├── load/
│   │   └── .gitkeep
│   ├── transform/
│   │   └── .gitkeep
│   └── utils/
│       └── .gitkeep
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd World-Cup-Match-Prediction
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment:

```bash
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

Install the project requirements:

```bash
pip install -r requirements.txt
```

## Environment Setup

Environment variables should be stored in a local `.env` file.

Example:

```bash
cp .env.example .env
```

This section is **Work in Progress**. Environment variables will be documented as the database, scraping, dashboard, and deployment configuration are finalized.

## Running the Project

This project is still **Work in Progress**. The final execution workflow may include data pipelines, model training scripts, scheduled jobs, and a Streamlit dashboard.

Planned examples:

```bash
python src/extract/<script_name>.py
python src/transform/<script_name>.py
python src/features/<script_name>.py
streamlit run dashboard/<app_name>.py
```

Notebook-based exploration can be run from:

```bash
jupyter notebook
```

## Team Responsibilities

### Data Engineering

- Data scraping and collection.
- Raw data validation.
- Data cleaning and transformation.
- Feature engineering pipeline.
- Database schema and loading logic.
- Scheduling and automation.

### Data Science

- Exploratory data analysis.
- Model training.
- Model evaluation.
- Match outcome prediction.
- Experiment tracking and comparison.

### Data Analytics

- Streamlit dashboard development.
- Team statistics visualization.
- Prediction visualization.
- User-facing analytics views.

This section is **Work in Progress** and will be updated with team member names and responsibilities.

## Planned Features

- Historical match data ingestion.
- FIFA World Cup 2026 team and fixture integration.
- Elo rating and team strength features.
- Match outcome prediction model.
- Model evaluation workflow.
- Database-backed data pipeline.
- Automated scheduling for repeatable updates.
- Streamlit dashboard for team analysis and predictions.
- Clear separation between raw, processed, and external data.

## Technologies Used

- Python
- Pandas
- NumPy
- SQLAlchemy
- PostgreSQL / SQLite
- Requests
- BeautifulSoup
- lxml
- Jupyter Notebook
- Streamlit
- Machine Learning libraries: **Work in Progress**
- Airflow / scheduling tools: **Work in Progress**

## Future Improvements

- Add production-ready pipeline scripts.
- Add automated tests.
- Add data validation checks.
- Add model versioning.
- Add experiment tracking.
- Add CI/CD workflow.
- Add Docker support.
- Add deployment instructions for the dashboard.
- Add complete database documentation.
- Add model performance reporting once models are trained and evaluated.

## Contributors

This is a BeCode team project.

Contributors section is **Work in Progress**.
