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

import streamlit as st

from data import get_teams, get_team, get_matches, get_group_standings, get_round_reach
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
)

st.set_page_config(page_title="World Cup 2026 Predictions", layout="wide", page_icon="⚽")
inject_css()

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
    teams_by_name = {t.name: t for t in teams}
    round_reach = get_round_reach()
    confederations = sorted({t.confederation for t in teams})

    title_col, stage_col, confed_col, reset_col = st.columns([2.2, 0.85, 0.95, 0.65])
    with title_col:
        st.markdown(
            """<div class="wc-page-title">Tournament Overview</div>
            <div class="wc-page-subtitle">AI predictions for FIFA World Cup 2026</div>""",
            unsafe_allow_html=True,
        )
    with stage_col:
        stage_filter = st.selectbox("Stage", ["All", "Group Stage"], key="overview_stage", label_visibility="visible")
    with confed_col:
        confed_filter = st.selectbox("Confederation", ["All"] + confederations, key="overview_confed", label_visibility="visible")
    with reset_col:
        st.write("")
        if st.button("Reset Filters", use_container_width=True):
            st.session_state["overview_stage"] = "All"
            st.session_state["overview_confed"] = "All"
            st.rerun()

    visible_matches = matches.copy()
    visible_teams = teams
    if confed_filter != "All":
        team_names = {t.name for t in teams if t.confederation == confed_filter}
        visible_matches = visible_matches[
            visible_matches.home_team.isin(team_names) | visible_matches.away_team.isin(team_names)
        ]
        visible_teams = [t for t in teams if t.name in team_names]

    upcoming = visible_matches[~visible_matches["played"]]
    latest_results = visible_matches[visible_matches["played"]].sort_values(
        ["match_date", "kickoff_time_utc"], ascending=[False, False]
    ).head(5)

    if not upcoming.empty:
        biggest_fav = upcoming.loc[upcoming[["home_win_probability", "away_win_probability"]].max(axis=1).idxmax()]
        fav_team, fav_prob, fav_opp = (
            (biggest_fav.home_team, biggest_fav.home_win_probability, biggest_fav.away_team)
            if biggest_fav.home_win_probability > biggest_fav.away_win_probability
            else (biggest_fav.away_team, biggest_fav.away_win_probability, biggest_fav.home_team)
        )
        biggest_upset = upcoming.loc[upcoming.upset_risk_score.idxmax()]
        avg_confidence = (1 - upcoming.upset_risk_score).mean() * 100
    else:
        fav_team, fav_prob, fav_opp = "n/a", 0, "n/a"
        biggest_upset = None
        avg_confidence = 0

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        kpi_card("Total matches", f"{len(visible_matches)}",
                 f"{int(visible_matches['played'].sum())} finished", icon="□")
    with c2:
        kpi_card("Avg. model confidence", f"{avg_confidence:.0f}%",
                 "Average prediction confidence", accent="green", icon="↗")
    with c3:
        kpi_card("Highest win probability", f"{fav_prob*100:.0f}%",
                 f"{fav_team} vs {fav_opp}", accent="purple", icon="◎")
    with c4:
        upset_match = f"{biggest_upset.home_team} vs {biggest_upset.away_team}" if biggest_upset is not None else "n/a"
        upset_sub = f"risk score {biggest_upset.upset_risk_score:.2f}" if biggest_upset is not None else "no upcoming matches"
        upset_value = f"{biggest_upset.upset_risk_score*100:.0f}%" if biggest_upset is not None else "n/a"
        kpi_card("Biggest upset risk", upset_value, f"{upset_match} | {upset_sub}", accent="gold", icon="!")

    left, mid, right = st.columns([1.1, 1.35, 1.75])
    with left:
        top_teams_panel(visible_teams)
    with mid:
        qualification_panel(round_reach, top_n=8)
    with right:
        upcoming_compact = upcoming.sort_values(["match_date", "kickoff_time_utc"]).head(5)
        compact_matches_panel(
            upcoming_compact,
            "Upcoming matches",
            "No upcoming matches are available.",
            teams_by_name=teams_by_name,
        )

    st.markdown("")
    compact_matches_panel(
        latest_results,
        "Latest results",
        "No finished matches are available yet.",
        teams_by_name=teams_by_name,
    )


# ---------------------------------------------------------- Match Details
def page_match_details():
    st.markdown('<div class="wc-top-spacer"></div>', unsafe_allow_html=True)
    matches = get_matches()
    teams_list = sorted(set(matches.home_team) | set(matches.away_team))

    st.markdown(
        """<div class="wc-page-title">Match Detail Page</div>
        <div class="wc-page-subtitle">Prediction breakdown, live status, and match context</div>""",
        unsafe_allow_html=True,
    )

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
        st.markdown(
            """<div class="wc-page-title">Group Stage Page</div>
            <div class="wc-page-subtitle">Current standings, qualification probability, and next fixtures</div>""",
            unsafe_allow_html=True,
        )
    with select_col:
        group_choice = st.selectbox("Select group", groups)

    group_stage_panel(group_choice, standings, matches, teams_by_name)


# --------------------------------------------------------- Knockout Bracket
def page_bracket():
    st.markdown('<div class="wc-top-spacer"></div>', unsafe_allow_html=True)
    standings = get_group_standings()
    round_reach = get_round_reach()
    teams = get_teams()
    teams_by_name = {t.name: t for t in teams}

    st.markdown(
        """<div class="wc-page-title">Knockout Bracket Page</div>
        <div class="wc-page-subtitle">Projected bracket from live standings and tournament simulations</div>""",
        unsafe_allow_html=True,
    )
    knockout_bracket_panel(standings, round_reach, teams_by_name)


# ------------------------------------------------------------------- Teams
def page_teams():
    st.markdown('<div class="wc-top-spacer"></div>', unsafe_allow_html=True)
    teams = get_teams()
    names = sorted(t.name for t in teams)
    header_col, group_col, select_col = st.columns([2.15, .9, 1])
    with header_col:
        st.markdown(
            """<div class="wc-page-title">Team Stats</div>
            <div class="wc-page-subtitle">Explore key team statistics and tournament performance</div>""",
            unsafe_allow_html=True,
        )
    with group_col:
        group_filter = st.selectbox("Group", ["All"] + sorted({t.group for t in teams}), key="team_group_filter")
    with select_col:
        choice = st.selectbox("Select a country", names)
    team = get_team(choice)
    round_reach = get_round_reach()
    standings = get_group_standings()
    visible_teams = [t for t in teams if group_filter == "All" or t.group == group_filter]
    visible_names = {t.name for t in visible_teams}
    visible_standings = standings[standings.team.isin(visible_names)]
    visible_round_reach = round_reach[round_reach.team.isin(visible_names)]
    team_stats_dashboard(visible_teams, visible_standings, visible_round_reach, selected_team=team.name)

    st.markdown("### Group-stage fixtures")
    matches = get_matches()
    team_matches = matches[(matches.home_team == team.name) | (matches.away_team == team.name)]
    for _, m in team_matches.iterrows():
        t1, t2 = get_team(m.home_team), get_team(m.away_team)
        match_card(m, t1, t2)


# ------------------------------------------------------------------- About
def page_about():
    st.title("About this dashboard")
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
