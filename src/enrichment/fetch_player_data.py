from __future__ import annotations

from src.enrichment.statbunker_client import fetch_statbunker_player_pages
from src.enrichment.transform_player_data import transform_player_data


def run_player_data_pipeline() -> None:
    """Fetch and transform free World Cup player data for dashboard enrichment."""
    print("Fetching free World Cup player data...")
    raw_paths = fetch_statbunker_player_pages()
    print(f"Raw player-data files saved: {len(raw_paths)}")

    print("Transforming player data...")
    processed_paths = transform_player_data()
    print(f"Processed player-data files saved: {len(processed_paths)}")
    print("Player data proof of concept completed.")


if __name__ == "__main__":
    try:
        run_player_data_pipeline()
    except Exception as exc:
        print(f"Player data pipeline failed: {exc}")
        raise SystemExit(1) from exc
