"""
FIFA World Cup 2026 — Prediction Dashboard
Streamlit entrypoint.

Page set and ordering follow the Data Analytics handoff doc:
  1. Tournament Overview
  2. Match Prediction Center
  3. Group Stage Analysis
  4. Team Explorer
  5. Knockout Bracket

Run with:  streamlit run dashboard/app.py
"""

import base64
from pathlib import Path
import sys

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from data import (
    get_teams,
    get_team,
    get_matches,
    get_group_standings,
    get_knockout_matches,
    get_round_reach,
    get_player_stats,
)
from components import (
    inject_css,
    kpi_card,
    match_card,
    top_teams_panel,
    qualification_panel,
    compact_matches_panel,
    match_detail_panel,
    group_stage_panel,
    knockout_bracket_panel,
    team_stats_dashboard,
    fifa_overview_dashboard,
)

st.set_page_config(page_title="World Cup 2026 Predictions", layout="wide", page_icon="⚽")
inject_css()

ASSET_DIR = Path(__file__).resolve().parent.parent / "assets"
TITLE_IMAGE_PATH = ASSET_DIR / "WC_trophy_transparent.png"


@st.cache_data(show_spinner=False)
def _title_image_src() -> str:
    if not TITLE_IMAGE_PATH.exists():
        return ""
    encoded = base64.b64encode(TITLE_IMAGE_PATH.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{encoded}"


def page_header(title: str, subtitle: str) -> None:
    image_src = _title_image_src()
    image_html = f'<img class="wc-page-emblem" src="{image_src}" alt="World Cup trophy">' if image_src else ""
    st.markdown(
        f"""<div class="wc-page-header">
            {image_html}
            <div class="wc-page-header-text">
                <div class="wc-page-title">{title}</div>
                <div class="wc-page-subtitle">{subtitle}</div>
            </div>
        </div>""",
        unsafe_allow_html=True,
    )


def _next_resolved_knockout_match(knockout_matches):
    if knockout_matches is None or knockout_matches.empty:
        return None
    required = {"home_team", "away_team", "is_resolved", "date", "kickoff_time"}
    if not required.issubset(set(knockout_matches.columns)):
        return None

    upcoming = knockout_matches[
        knockout_matches["is_resolved"].astype(bool)
        & knockout_matches["home_team"].notna()
        & knockout_matches["away_team"].notna()
        & ~knockout_matches["status"].astype(str).str.upper().eq("FINISHED")
    ].copy()
    if upcoming.empty:
        return None

    upcoming = upcoming.sort_values(["date", "kickoff_time", "match_id"], na_position="last")
    row = upcoming.iloc[0]
    home = str(row["home_team"])
    away = str(row["away_team"])
    try:
        from src.predict import predict_match

        prediction = predict_match(home, away)
    except Exception:
        prediction = {"home_win": 1 / 3, "draw": 1 / 3, "away_win": 1 / 3}

    return {
        "home_team": home,
        "away_team": away,
        "date": row.get("date"),
        "kickoff_time": row.get("kickoff_time"),
        "stage": row.get("stage", "Knockout"),
        "home_win_probability": prediction["home_win"],
        "draw_probability": prediction["draw"],
        "away_win_probability": prediction["away_win"],
    }


PAGES = ["Overview", "Match Details", "Groups", "Knockout Bracket", "Teams", "About"]

with st.sidebar:
    st.markdown("## ⚽ WC 2026 Predictions")
    page = st.radio("Navigate", PAGES, label_visibility="collapsed")
    st.markdown("---")
    matches_now = get_matches()
    st.caption(f"🟢 Live model: XGBoost classifier\n\n"
               f"{int(matches_now['played'].sum())}/{len(matches_now)} group matches played")


# ---------------------------------------------------------------- Overview
def page_overview():
    st.markdown('<div class="wc-top-spacer"></div>', unsafe_allow_html=True)
    matches = get_matches()
    teams = get_teams()
    round_reach = get_round_reach()
    player_stats = get_player_stats()
    knockout_matches = get_knockout_matches()
    fifa_overview_dashboard(
        matches=matches,
        teams=teams,
        round_reach=round_reach,
        player_stats=player_stats,
        next_match=_next_resolved_knockout_match(knockout_matches),
        trophy_src=_title_image_src(),
    )


# ---------------------------------------------------------- Match Details
def page_match_details():
    st.markdown('<div class="wc-top-spacer"></div>', unsafe_allow_html=True)
    matches = get_matches()
    teams_list = sorted(set(matches.home_team) | set(matches.away_team))

    page_header("Match Detail Page", "Prediction breakdown, live status, and match context")

    c1, c2, c3 = st.columns([0.9, 1.1, 2.4])
    with c1:
        group_filter = st.selectbox("Group", ["All"] + sorted(matches.group.unique()))
    with c2:
        team_filter = st.selectbox("Team", ["All"] + teams_list)

    filtered = matches.copy()
    if group_filter != "All":
        filtered = filtered[filtered.group == group_filter]
    if team_filter != "All":
        filtered = filtered[(filtered.home_team == team_filter) | (filtered.away_team == team_filter)]

    filtered = filtered.sort_values(["match_date", "kickoff_time_utc"]).reset_index(drop=True)
    if filtered.empty:
        st.info("No matches found for the selected filters.")
        return

    match_options = [
        f"{row.match_date} | Group {row.group} | {row.home_team} vs {row.away_team}"
        for _, row in filtered.iterrows()
    ]
    with c3:
        selected_label = st.selectbox("Match", match_options)

    selected_idx = match_options.index(selected_label)
    m = filtered.iloc[selected_idx]
    t1, t2 = get_team(m.home_team), get_team(m.away_team)
    focus_team = team_filter if team_filter != "All" else None
    match_detail_panel(m, t1, t2, focus_team=focus_team)


# ----------------------------------------------------------------- Groups
def page_groups():
    st.markdown('<div class="wc-top-spacer"></div>', unsafe_allow_html=True)
    standings = get_group_standings()
    matches = get_matches()
    teams = get_teams()
    teams_by_name = {t.name: t for t in teams}
    groups = sorted(standings.group.unique())
    header_col, select_col = st.columns([2.4, 1])
    with header_col:
        page_header("Group Stage Page", "Current standings, qualification probability, and next fixtures")
    with select_col:
        group_choice = st.selectbox("Select group", groups)

    group_stage_panel(group_choice, standings, matches, teams_by_name)


# --------------------------------------------------------- Knockout Bracket
def page_bracket():
    st.markdown('<div class="wc-top-spacer"></div>', unsafe_allow_html=True)
    standings = get_group_standings()
    round_reach = get_round_reach()
    knockout_matches = get_knockout_matches()
    teams = get_teams()
    teams_by_name = {t.name: t for t in teams}

    page_header("Knockout Bracket Page", "Resolved fixtures when available, with projected progression from simulations")
    knockout_bracket_panel(standings, round_reach, teams_by_name, knockout_matches=knockout_matches)


# ------------------------------------------------------------------- Teams
def page_teams():
    st.markdown('<div class="wc-top-spacer"></div>', unsafe_allow_html=True)
    teams = get_teams()
    names = [t.name for t in sorted(teams, key=lambda t: (-t.elo, t.name))]
    header_col, select_col = st.columns([2.35, 1])
    with header_col:
        page_header("Team Elo Rankings", "Search countries, compare Elo strength, and inspect tournament context")
    with select_col:
        choice = st.selectbox("Search country", names)
    team = get_team(choice)
    round_reach = get_round_reach()
    standings = get_group_standings()
    matches = get_matches()
    player_stats = get_player_stats()
    team_stats_dashboard(
        teams,
        standings,
        round_reach,
        matches=matches,
        player_stats=player_stats,
        selected_team=team.name,
    )


# ------------------------------------------------------------------- About
def page_about():
    st.markdown('<div class="wc-top-spacer"></div>', unsafe_allow_html=True)
    page_header("About This Dashboard", "Project context, data sources, and model scope")
    matches = get_matches()
    st.markdown(f"""
This dashboard is built around **football questions, not datasets** —
match-centric cards, qualification odds, and a road-to-the-final view
instead of raw tables, per the Data Analytics handoff brief.

**Model:** XGBoost multi-class classifier (`multi:softprob`) trained on
historical international results (1916-2026) using Elo difference, recent
win/draw rates, and average goals scored/conceded as features. Validated
on the 2022 World Cup, tested on the {int(matches['played'].sum())} WC 2026
group matches played so far: **53.6% accuracy** and **0.984 log-loss**
(vs. a 1.099 random baseline). `elo_diff` was by far the strongest feature,
followed by each side's average goals conceded and win rate.

**What's real vs. simulated:**
- Match outcomes for the {int(matches['played'].sum())} matches already played are the
  **actual final scores** — not predictions.
- Win/draw/loss probabilities for the remaining {int((~matches['played']).sum())} group
  matches are the **model's own output**, unmodified.
- Group standings combine real points earned so far with the model's
  probabilities for the matches still to come.
- Qualification and round-reach odds come from a **3,000-run Monte Carlo
  simulation** that resamples only the unplayed group matches, applies the
  official 48-team format (top 2 per group + best 8 third-place teams),
  and follows the real knockout bracket skeleton (1A vs 2B, etc.) through
  to the Final. Knockout matches themselves use a standard Elo win-probability
  curve, since the trained classifier needs recent-form features that don't
  exist yet for hypothetical knockout pairings — this is a clearly-flagged
  approximation layered on top of the model's group-stage predictions, not
  a replacement for them.

**Pages:**
- **Overview** — the big tournament story at a glance
- **Match Details** — match-preview style cards: real scores if played, model odds if not
- **Groups** — actual standings plus simulated qualification odds, one group at a time
- **Knockout Bracket** — round-reach funnel and tournament winner odds from the simulation
- **Teams** — per-country profile: Elo, this campaign's results, pre-tournament form, fixtures
""")


PAGE_FUNCS = {
    "Overview": page_overview,
    "Match Details": page_match_details,
    "Groups": page_groups,
    "Knockout Bracket": page_bracket,
    "Teams": page_teams,
    "About": page_about,
}

PAGE_FUNCS[page]()
