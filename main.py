from __future__ import annotations

from pathlib import Path

from src.cleaning.clean_elo import clean_elo
from src.cleaning.clean_results import clean_results
from src.cleaning.standardize_teams import standardize_teams
from src.enrichment.enrich_fixtures import enrich_fixtures
from src.export.build_model_dataset import build_model_dataset
from src.extract.football_data_api import fetch_competition_matches, get_api_key, save_json
from src.transform.live_matches import load_raw_matches, transform_matches, save_matches

BASE_DIR = Path(__file__).resolve().parent
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"


def run_live_data_pipeline() -> None:
    """Fetch and transform live World Cup data when an API key is configured."""
    if not get_api_key():
        print("[6/6] Skipping live World Cup matches: FOOTBALL_DATA_API_KEY is not set.")
        return

    print("[6/6] Fetching and transforming live World Cup matches...")
    matches = fetch_competition_matches("WC", 2026)
    raw_output_path = save_json(matches, "football_data_wc_matches.json")

    raw_live_matches = load_raw_matches(raw_output_path)
    live_matches = transform_matches(raw_live_matches)
    save_matches(live_matches)


def main() -> None:
    """Run the lightweight Data Engineering pipeline."""
    print("[1/6] Cleaning historical results...")
    clean_results(
        input_path=RAW_DIR / "IF_1872_2026" / "results.csv",
        output_dir=PROCESSED_DIR,
    )

    print("[2/6] Processing Elo ratings...")
    clean_elo(
        input_path=RAW_DIR / "FIFA_WK_Elo_Ratings" / "elo_ratings_wc2026.csv",
        teams_path=RAW_DIR / "FIFA_WC_1930_2026" / "wc_2026_teams.csv",
        output_dir=PROCESSED_DIR,
    )

    print("[3/6] Standardizing team and fixture references...")
    standardize_teams(
        teams_input_path=RAW_DIR / "FIFA_WC_1930_2026" / "wc_2026_teams.csv",
        fixtures_input_path=RAW_DIR / "FIFA_WC_1930_2026" / "wc_2026_fixtures.csv",
        elo_latest_path=PROCESSED_DIR / "elo_latest.csv",
        teams_output_path=PROCESSED_DIR / "wc_2026_teams_cleaned.csv",
        fixtures_output_path=PROCESSED_DIR / "wc_2026_fixtures_validated.csv",
    )

    print("[4/6] Enriching World Cup 2026 fixtures...")
    enrich_fixtures(
        fixtures_path=PROCESSED_DIR / "wc_2026_fixtures_validated.csv",
        teams_path=PROCESSED_DIR / "wc_2026_teams_cleaned.csv",
        elo_latest_path=PROCESSED_DIR / "elo_latest.csv",
        output_path=PROCESSED_DIR / "wc_2026_fixtures_enriched.csv",
    )

    print("[5/6] Building base model dataset...")
    build_model_dataset(
        historical_results_path=PROCESSED_DIR / "results_historical.csv",
        output_path=PROCESSED_DIR / "model_training_base.csv",
    )

    run_live_data_pipeline()

    print("Pipeline completed successfully.")


if __name__ == "__main__":
    main()
