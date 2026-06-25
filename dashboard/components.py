"""
Reusable, football-flavoured UI building blocks for the Streamlit app.
Keeps app.py focused on page composition rather than markup.
"""

from html import escape

import streamlit as st

_FLAG_IMAGE_CODES = {
    "England": "gb-eng",
    "Scotland": "gb-sct",
    "Wales": "gb-wls",
    "Northern Ireland": "gb-nir",
}


def _flag_image_url(team, size: str = "w40") -> str | None:
    code = _FLAG_IMAGE_CODES.get(team.name) or getattr(team, "iso2", "")
    code = str(code).strip().lower()
    if not code:
        return None
    return f"https://flagcdn.com/{size}/{code}.png"


def _flag_image_html(team, class_name: str = "wc-team-flag-img") -> str:
    size = "w320" if class_name == "wc-detail-team-flag" else "w40"
    url = _flag_image_url(team, size)
    if not url:
        return f'<span class="wc-team-flag">{team.flag}</span>'
    if class_name == "wc-detail-team-flag":
        return (
            f'<span class="{class_name}" role="img" aria-label="{team.name} flag" '
            f'style="background-image:url({url});"></span>'
        )
    return (
        f'<img class="{class_name}" '
        f'src="{url}" '
        f'alt="{team.name} flag" loading="lazy">'
    )


CSS = """
<style>
html, body, [data-testid="stAppViewContainer"] {
    background:
        radial-gradient(circle at 20% 0%, rgba(29, 83, 132, 0.30), transparent 34%),
        radial-gradient(circle at 92% 6%, rgba(97, 74, 20, 0.22), transparent 30%),
        linear-gradient(135deg, #050b14 0%, #071624 46%, #04101b 100%);
    color: #f5f7fb;
}

[data-testid="stAppViewContainer"] > .main {
    background: transparent;
}

.block-container {
    padding-top: 4.25rem;
    padding-bottom: 2rem;
    max-width: 1600px;
}

[data-testid="stSidebar"] {
    background:
        linear-gradient(180deg, rgba(8, 24, 42, 0.98), rgba(2, 11, 22, 0.98)),
        radial-gradient(circle at top left, rgba(32, 92, 156, 0.25), transparent 38%);
    border-right: 1px solid rgba(129, 173, 223, 0.12);
}

[data-testid="stSidebar"] * {
    color: #f5f7fb;
}

[data-testid="stRadio"] label {
    background: transparent;
    border-radius: 8px;
}

h1, h2, h3 {
    letter-spacing: 0;
}

.wc-page-title {
    font-size: 2rem;
    line-height: 1.05;
    font-weight: 800;
    text-transform: uppercase;
    margin: 0 0 4px 0;
    color: #ffffff;
}

.wc-top-spacer {
    height: 44px;
}

.wc-page-subtitle {
    color: #9bb8d7;
    font-size: 0.92rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    margin-top: 6px;
}

.wc-panel {
    background: linear-gradient(145deg, rgba(9, 28, 46, 0.94), rgba(5, 17, 30, 0.96));
    border: 1px solid rgba(130, 173, 222, 0.16);
    border-radius: 8px;
    padding: 16px;
    box-shadow: 0 18px 50px rgba(0,0,0,0.22);
    min-height: 100%;
}

.wc-panel-title {
    color: #ffffff;
    font-weight: 800;
    font-size: 0.92rem;
    text-transform: uppercase;
    margin-bottom: 12px;
}

.wc-card {
    background: linear-gradient(135deg, rgba(9, 36, 66, 0.96) 0%, rgba(5, 20, 38, 0.98) 100%);
    border: 1px solid rgba(118, 165, 224, 0.22);
    border-radius: 8px;
    padding: 18px 20px;
    color: #f4f7f5;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.06), 0 12px 30px rgba(0,0,0,0.20);
    margin-bottom: 10px;
    min-height: 116px;
}
.wc-card-green { background: linear-gradient(135deg, rgba(13, 56, 35, 0.96), rgba(7, 41, 26, 0.96)); border-color: rgba(93, 181, 102, 0.28); }
.wc-card-purple { background: linear-gradient(135deg, rgba(33, 22, 66, 0.96), rgba(17, 13, 44, 0.96)); border-color: rgba(135, 90, 218, 0.32); }
.wc-card-gold { background: linear-gradient(135deg, rgba(78, 55, 10, 0.96), rgba(44, 31, 5, 0.96)); border-color: rgba(214, 166, 54, 0.32); }
.wc-kpi-label { font-size: 0.78rem; opacity: 0.86; text-transform: uppercase; letter-spacing: 0.04em; }
.wc-kpi-value { font-size: 1.75rem; font-weight: 800; margin-top: 8px; color: #ffffff; }
.wc-kpi-sub { font-size: 0.82rem; opacity: 0.85; margin-top: 5px; max-width: 14rem; }
.wc-kpi-icon { float: right; font-size: 2.5rem; opacity: 0.35; margin-top: -4px; }

.wc-match-card {
    background: rgba(11, 30, 48, 0.72);
    border: 1px solid rgba(139, 177, 219, 0.14);
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 10px;
}
.wc-team-row { display: flex; justify-content: space-between; align-items: center; font-size: 1.05rem; font-weight: 600; }
.wc-prob-bar-wrap { display: flex; height: 10px; border-radius: 6px; overflow: hidden; margin: 10px 0; background: #00000022; }
.wc-prob-seg { height: 100%; }
.wc-prob-labels { display: flex; justify-content: space-between; font-size: 0.78rem; opacity: 0.85; }
.wc-pill {
    display: inline-block; padding: 2px 10px; border-radius: 999px;
    font-size: 0.75rem; font-weight: 600;
}
.wc-pill-high { background: #1e7d4733; color: #5fd98f; }
.wc-pill-medium { background: #c98a1f33; color: #f0b94d; }
.wc-pill-low { background: #b8333322; color: #ef7b7b; }
.wc-upset { color: #f0b94d; font-size: 0.8rem; }
.wc-match-meta { margin-top: 8px; font-size: 0.78rem; opacity: 0.78; }

.wc-team-rank {
    display: grid;
    grid-template-columns: 24px 28px minmax(92px, 1fr) minmax(90px, 170px) 46px;
    gap: 10px;
    align-items: center;
    padding: 5px 0;
    font-size: 0.84rem;
}
.wc-team-flag {
    font-size: 1.05rem;
    line-height: 1;
}
.wc-team-flag-img {
    width: 24px;
    height: 16px;
    object-fit: cover;
    border-radius: 2px;
    box-shadow: 0 0 0 1px rgba(255,255,255,0.16);
}
.wc-rank-bar {
    height: 6px;
    border-radius: 999px;
    background: rgba(255,255,255,0.08);
    overflow: hidden;
}
.wc-rank-fill {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, #5ca736, #98c94d);
}

.wc-donut-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(76px, 1fr));
    gap: 16px 18px;
}
.wc-donut-item { text-align: center; }
.wc-donut {
    --p: 50;
    width: 70px;
    height: 70px;
    margin: 0 auto 6px;
    border-radius: 50%;
    display: grid;
    place-items: center;
    background:
        radial-gradient(circle closest-side, #071827 69%, transparent 70% 100%),
        conic-gradient(#7fb345 calc(var(--p) * 1%), rgba(130, 169, 216, 0.22) 0);
    color: #ffffff;
    font-weight: 800;
}
.wc-donut-name {
    font-size: 0.82rem;
    color: #e8eef6;
}

.wc-compact-match {
    display: grid;
    grid-template-columns: 78px minmax(145px, 1fr) minmax(150px, 190px);
    gap: 10px;
    align-items: center;
    padding: 8px 10px;
    margin-bottom: 7px;
    border: 1px solid rgba(130, 173, 222, 0.13);
    border-radius: 8px;
    background: rgba(10, 27, 43, 0.76);
    font-size: 0.84rem;
}
.wc-compact-date {
    color: #a9bdd4;
    line-height: 1.2;
    font-weight: 700;
}
.wc-compact-date small {
    display: block;
    color: rgba(205, 221, 239, 0.62);
    font-weight: 500;
    margin-top: 3px;
}
.wc-compact-teams {
    display: grid;
    grid-template-columns: 1fr 26px 1fr;
    gap: 8px;
    align-items: center;
    color: #ffffff;
}
.wc-compact-team {
    display: flex;
    align-items: center;
    gap: 8px;
    min-width: 0;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.wc-compact-vs {
    opacity: .72;
    text-align: center;
    font-weight: 700;
    font-size: .72rem;
}
.wc-compact-probs {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 5px;
    min-width: 0;
}
.wc-prob-chip {
    position: relative;
    overflow: hidden;
    background: rgba(255,255,255,0.075);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 5px;
    padding: 5px 4px;
    color: #dce8f4;
    font-size: 0.68rem;
    text-align: center;
    font-weight: 700;
}
.wc-prob-chip-fill {
    position: absolute;
    inset: 0 auto 0 0;
    width: var(--w);
    background: linear-gradient(90deg, rgba(91, 166, 50, 0.90), rgba(125, 196, 72, 0.82));
    opacity: .85;
}
.wc-prob-chip-fill-draw {
    background: linear-gradient(90deg, rgba(129, 145, 162, 0.92), rgba(172, 184, 196, 0.78));
}
.wc-prob-chip-fill-away {
    background: linear-gradient(90deg, rgba(58, 117, 185, 0.92), rgba(89, 153, 219, 0.78));
}
.wc-prob-chip span {
    position: relative;
    z-index: 1;
}
.wc-prob-chip-muted {
    background: rgba(136, 152, 170, 0.20);
}
.wc-prob-chip-away {
    background: rgba(45, 96, 150, 0.22);
    border-color: rgba(93, 160, 230, 0.22);
}

.wc-group-shell {
    background:
        radial-gradient(circle at 16% 0%, rgba(34, 90, 151, 0.22), transparent 34%),
        linear-gradient(145deg, rgba(5, 18, 31, 0.98), rgba(2, 11, 20, 0.98));
    border: 1px solid rgba(130, 173, 222, 0.22);
    border-radius: 8px;
    padding: 18px;
    box-shadow: 0 22px 58px rgba(0,0,0,0.32);
}
.wc-group-title {
    color: #ffffff;
    font-size: 1.35rem;
    font-weight: 800;
    text-transform: uppercase;
    margin-bottom: 18px;
}
.wc-group-table {
    display: grid;
    gap: 0;
    overflow-x: auto;
}
.wc-group-row {
    display: grid;
    grid-template-columns: 32px minmax(180px, 1.8fr) repeat(8, minmax(44px, .42fr)) minmax(128px, .9fr);
    align-items: center;
    min-width: 780px;
    min-height: 40px;
    border-bottom: 1px solid rgba(130, 173, 222, 0.12);
    color: #f4f7fb;
    font-size: .84rem;
}
.wc-group-row:last-child {
    border-bottom: 0;
}
.wc-group-head {
    min-height: 34px;
    color: rgba(221, 232, 245, .78);
    font-size: .68rem;
    font-weight: 800;
    text-transform: uppercase;
}
.wc-group-team-cell {
    display: flex;
    align-items: center;
    gap: 9px;
    min-width: 0;
    font-weight: 800;
}
.wc-group-team-cell span:last-child {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.wc-group-flag-img {
    width: 30px;
    height: 20px;
    object-fit: cover;
    border-radius: 2px;
    box-shadow: 0 0 0 1px rgba(255,255,255,.16);
}
.wc-group-stat {
    text-align: center;
    font-weight: 700;
}
.wc-qual-cell {
    padding-left: 8px;
}
.wc-qual-bar {
    position: relative;
    height: 24px;
    overflow: hidden;
    border-radius: 4px;
    background: rgba(255,255,255,.08);
    border: 1px solid rgba(255,255,255,.08);
}
.wc-qual-fill {
    position: absolute;
    inset: 0 auto 0 0;
    width: var(--w);
    background: linear-gradient(90deg, #5ca736, #91c84c);
}
.wc-qual-cell span {
    position: relative;
    z-index: 1;
    display: block;
    text-align: right;
    padding: 3px 8px 0 0;
    font-size: .75rem;
    font-weight: 800;
    color: #ffffff;
}
.wc-group-mid {
    display: grid;
    grid-template-columns: 1.08fr .95fr;
    gap: 14px;
    margin-top: 16px;
}
.wc-points-row {
    display: grid;
    grid-template-columns: minmax(110px, .7fr) minmax(150px, 1.4fr) 42px;
    align-items: center;
    gap: 10px;
    margin: 10px 0;
    color: #ffffff;
    font-size: .82rem;
}
.wc-points-track {
    height: 22px;
    border-radius: 3px;
    background: rgba(255,255,255,.08);
    overflow: hidden;
}
.wc-points-fill {
    display: block;
    height: 100%;
    width: var(--w);
    border-radius: 3px;
}
.wc-axis {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    margin-left: calc(110px + 10px);
    color: rgba(221,232,245,.58);
    font-size: .72rem;
}
.wc-stat-line {
    display: grid;
    grid-template-columns: 1fr auto;
    gap: 14px;
    padding: 11px 0;
    border-bottom: 1px solid rgba(255,255,255,.08);
    color: #eaf1f8;
    font-size: .84rem;
}
.wc-stat-line:last-child {
    border-bottom: 0;
}
.wc-stat-value {
    font-weight: 800;
    color: #ffffff;
}
.wc-next-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 10px;
}
.wc-next-card {
    min-height: 82px;
    display: grid;
    align-content: center;
    gap: 8px;
    padding: 12px;
    border-radius: 8px;
    border: 1px solid rgba(130, 173, 222, 0.13);
    background: rgba(10, 27, 43, 0.76);
    color: #ffffff;
}
.wc-next-teams {
    display: grid;
    grid-template-columns: 1fr 24px 1fr;
    align-items: center;
    gap: 8px;
    font-size: .82rem;
    font-weight: 800;
}
.wc-next-team {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 7px;
    min-width: 0;
}
.wc-next-team span {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.wc-next-date {
    text-align: center;
    color: #dce8f4;
    font-size: .8rem;
    font-weight: 800;
}
.wc-next-status {
    text-align: center;
    color: rgba(221,232,245,.62);
    font-size: .68rem;
    text-transform: uppercase;
}

.wc-bracket-shell {
    background:
        radial-gradient(circle at 18% 0%, rgba(34, 90, 151, 0.22), transparent 34%),
        radial-gradient(circle at 82% 18%, rgba(115, 84, 16, 0.18), transparent 28%),
        linear-gradient(145deg, rgba(5, 18, 31, 0.98), rgba(2, 11, 20, 0.98));
    border: 1px solid rgba(130, 173, 222, 0.22);
    border-radius: 8px;
    padding: 18px;
    box-shadow: 0 22px 58px rgba(0,0,0,0.32);
}
.wc-bracket-tabs {
    display: grid;
    grid-template-columns: repeat(4, minmax(120px, 1fr));
    gap: 8px;
    max-width: 700px;
    margin: 0 auto 16px;
}
.wc-bracket-tab {
    text-align: center;
    padding: 8px 12px;
    border-radius: 6px;
    background: rgba(255,255,255,.06);
    border: 1px solid rgba(130, 173, 222, 0.08);
    color: rgba(235,243,252,.70);
    font-size: .78rem;
    font-weight: 800;
}
.wc-bracket-tab-active {
    color: #ffffff;
    background: linear-gradient(135deg, rgba(58, 102, 161, .92), rgba(28, 55, 94, .92));
    border-color: rgba(119, 168, 226, .28);
}
.wc-bracket-grid {
    display: grid;
    grid-template-columns: 1.15fr .92fr .88fr .82fr .72fr;
    gap: 22px;
    align-items: center;
}
.wc-bracket-col-title {
    color: rgba(235,243,252,.76);
    font-size: .7rem;
    font-weight: 800;
    text-transform: uppercase;
    margin: 0 0 8px 4px;
}
.wc-bracket-col {
    display: grid;
    gap: 10px;
}
.wc-bracket-col-r16 { gap: 32px; }
.wc-bracket-col-qf { gap: 74px; }
.wc-bracket-col-sf { gap: 152px; }
.wc-bracket-match {
    position: relative;
    border-radius: 7px;
    overflow: hidden;
    background: linear-gradient(135deg, rgba(17, 38, 58, .92), rgba(10, 24, 39, .96));
    border: 1px solid rgba(130, 173, 222, 0.15);
    box-shadow: inset 0 1px 0 rgba(255,255,255,.05);
}
.wc-bracket-team {
    display: grid;
    grid-template-columns: 34px 28px minmax(70px, 1fr) 42px;
    align-items: center;
    gap: 7px;
    min-height: 30px;
    padding: 4px 8px;
    border-bottom: 1px solid rgba(255,255,255,.07);
    color: #ffffff;
    font-size: .76rem;
}
.wc-bracket-team:last-child {
    border-bottom: 0;
}
.wc-bracket-slot {
    color: rgba(221,232,245,.62);
    font-weight: 800;
}
.wc-bracket-team-name {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    font-weight: 800;
}
.wc-bracket-prob {
    text-align: right;
    color: #dce8f4;
    font-weight: 800;
}
.wc-bracket-single {
    grid-template-columns: 28px minmax(90px, 1fr) 48px;
    min-height: 36px;
}
.wc-bracket-winner {
    background: linear-gradient(145deg, rgba(60, 44, 8, .96), rgba(22, 22, 12, .96));
    border: 1px solid rgba(218, 166, 40, .68);
    border-radius: 8px;
    padding: 14px;
    color: #ffffff;
    text-align: center;
}
.wc-trophy {
    font-size: 2.4rem;
    margin-bottom: 4px;
}
.wc-winner-title {
    color: #e7c359;
    font-weight: 800;
    text-transform: uppercase;
    font-size: .82rem;
    margin-bottom: 12px;
}
.wc-winner-main {
    display: grid;
    place-items: center;
    gap: 7px;
    font-size: 1.05rem;
    font-weight: 800;
    margin-bottom: 10px;
}
.wc-winner-list {
    display: grid;
    gap: 8px;
    margin-top: 10px;
}
.wc-winner-row {
    display: grid;
    grid-template-columns: 28px 1fr 42px;
    gap: 8px;
    align-items: center;
    text-align: left;
    font-size: .76rem;
}
.wc-title-card-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 12px;
}
.wc-title-card {
    display: grid;
    grid-template-columns: 42px 1fr;
    gap: 12px;
    align-items: center;
    min-height: 84px;
    padding: 12px;
    background: rgba(12, 30, 48, .76);
    border: 1px solid rgba(130, 173, 222, 0.15);
    border-radius: 8px;
    color: #ffffff;
}
.wc-title-rank {
    height: 58px;
    border-radius: 6px;
    display: grid;
    place-items: center;
    font-size: 1.35rem;
    font-weight: 800;
    background: rgba(255,255,255,.08);
}
.wc-title-card:first-child {
    background: linear-gradient(135deg, rgba(27, 73, 124, .88), rgba(12, 36, 70, .88));
    border-color: rgba(113, 169, 232, .32);
}
.wc-title-team {
    font-weight: 800;
    margin-bottom: 8px;
}
.wc-title-prob {
    font-size: 1.2rem;
    font-weight: 800;
}

.wc-team-stats-grid {
    display: grid;
    grid-template-columns: repeat(6, minmax(0, 1fr));
    gap: 12px;
}
.wc-team-stat-card {
    min-height: 150px;
    position: relative;
    overflow: hidden;
    border-radius: 8px;
    padding: 14px;
    background: linear-gradient(135deg, rgba(9, 36, 66, .96), rgba(5, 20, 38, .98));
    border: 1px solid rgba(118, 165, 224, .22);
    color: #ffffff;
}
.wc-team-stat-card-green { background: linear-gradient(135deg, rgba(13, 56, 35, .96), rgba(7, 41, 26, .96)); border-color: rgba(93, 181, 102, .28); }
.wc-team-stat-card-purple { background: linear-gradient(135deg, rgba(33, 22, 66, .96), rgba(17, 13, 44, .96)); border-color: rgba(135, 90, 218, .32); }
.wc-team-stat-card-gold { background: linear-gradient(135deg, rgba(78, 55, 10, .96), rgba(44, 31, 5, .96)); border-color: rgba(214, 166, 54, .32); }
.wc-team-stat-card-blue { background: linear-gradient(135deg, rgba(8, 48, 82, .96), rgba(5, 24, 44, .96)); border-color: rgba(71, 142, 219, .28); }
.wc-team-stat-card::after {
    content: "";
    position: absolute;
    right: -30px;
    bottom: -48px;
    width: 126px;
    height: 126px;
    border-radius: 50%;
    background: rgba(255,255,255,.05);
}
.wc-team-stat-label {
    color: rgba(234, 244, 252, .82);
    font-size: .72rem;
    font-weight: 800;
    text-transform: uppercase;
}
.wc-team-stat-value {
    font-size: 1.85rem;
    font-weight: 800;
    margin: 16px 0 4px;
}
.wc-team-stat-name {
    font-weight: 800;
    margin-top: 12px;
}
.wc-team-stat-sub {
    color: rgba(234, 244, 252, .82);
    font-size: .78rem;
    margin-top: 8px;
}
.wc-team-stat-flag {
    position: absolute;
    right: 14px;
    bottom: 16px;
    width: 54px;
    height: 36px;
    object-fit: cover;
    border-radius: 4px;
    box-shadow: 0 10px 28px rgba(0,0,0,.28), 0 0 0 1px rgba(255,255,255,.18);
}
.wc-team-dashboard-grid {
    display: grid;
    grid-template-columns: 1.45fr .95fr .9fr;
    gap: 14px;
    margin-top: 14px;
}
.wc-team-table {
    display: grid;
    gap: 0;
}
.wc-team-table-row {
    display: grid;
    grid-template-columns: 28px minmax(130px, 1.3fr) 54px 40px 40px 44px 52px 58px;
    gap: 8px;
    align-items: center;
    min-height: 32px;
    border-bottom: 1px solid rgba(255,255,255,.07);
    color: #eef6ff;
    font-size: .78rem;
}
.wc-team-table-row:last-child { border-bottom: 0; }
.wc-team-table-head {
    color: rgba(221,232,245,.62);
    text-transform: uppercase;
    font-size: .64rem;
    font-weight: 800;
}
.wc-team-table-team {
    display: flex;
    align-items: center;
    gap: 8px;
    min-width: 0;
    font-weight: 800;
}
.wc-team-table-team span:last-child {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.wc-team-impact-row {
    display: grid;
    grid-template-columns: 28px minmax(110px, 1fr) minmax(110px, 1.2fr) 48px;
    gap: 8px;
    align-items: center;
    min-height: 34px;
    color: #ffffff;
    font-size: .78rem;
}
.wc-team-impact-bar {
    height: 8px;
    border-radius: 999px;
    background: rgba(255,255,255,.08);
    overflow: hidden;
}
.wc-team-impact-fill {
    display: block;
    height: 100%;
    width: var(--w);
    background: linear-gradient(90deg, #67ad3b, #9cca4f);
    border-radius: 999px;
}
.wc-team-bars {
    display: grid;
    gap: 12px;
}
.wc-team-bar-row {
    display: grid;
    grid-template-columns: minmax(100px, .9fr) 1fr 32px;
    gap: 10px;
    align-items: center;
    color: #ffffff;
    font-size: .78rem;
}
.wc-team-bar-track {
    height: 13px;
    border-radius: 4px;
    background: rgba(255,255,255,.08);
    overflow: hidden;
}
.wc-team-bar-fill {
    display: block;
    height: 100%;
    width: var(--w);
    background: linear-gradient(90deg, #5ca736, #91c84c);
    border-radius: 4px;
}
.wc-mini-panel-grid {
    display: grid;
    grid-template-columns: 1.25fr .7fr 1fr;
    gap: 12px;
    margin-top: 14px;
}
.wc-team-donut-row {
    display: grid;
    grid-template-columns: repeat(5, minmax(64px, 1fr));
    gap: 10px;
}
.wc-team-note {
    color: rgba(221,232,245,.72);
    font-size: .75rem;
    margin-top: 12px;
}
@media (max-width: 1100px) {
    .wc-bracket-grid {
        grid-template-columns: 1fr;
    }
    .wc-bracket-col,
    .wc-bracket-col-r16,
    .wc-bracket-col-qf,
    .wc-bracket-col-sf,
    .wc-title-card-grid,
    .wc-team-stats-grid,
    .wc-team-dashboard-grid,
    .wc-mini-panel-grid {
        grid-template-columns: 1fr;
        gap: 10px;
    }
}
@media (max-width: 900px) {
    .wc-group-mid,
    .wc-next-grid {
        grid-template-columns: 1fr;
    }
}

.wc-detail-shell {
    background:
        radial-gradient(circle at 22% 14%, rgba(34, 90, 151, 0.22), transparent 35%),
        radial-gradient(circle at 78% 18%, rgba(44, 106, 89, 0.18), transparent 30%),
        linear-gradient(145deg, rgba(5, 18, 31, 0.98), rgba(2, 11, 20, 0.98));
    border: 1px solid rgba(130, 173, 222, 0.22);
    border-radius: 8px;
    padding: 18px;
    box-shadow: 0 22px 58px rgba(0,0,0,0.32);
}
.wc-detail-back {
    color: #c5d6e8;
    font-size: .82rem;
    margin-bottom: 8px;
}
.wc-detail-head {
    text-align: center;
    margin-bottom: 12px;
}
.wc-detail-title {
    color: #ffffff;
    font-size: 1rem;
    font-weight: 800;
    text-transform: uppercase;
}
.wc-detail-meta {
    color: #b8c6d6;
    font-size: .82rem;
    margin-top: 6px;
}
.wc-detail-teams {
    display: grid;
    grid-template-columns: minmax(120px, 1fr) minmax(260px, 1.35fr) minmax(120px, 1fr);
    align-items: center;
    gap: 16px;
    margin: 8px 0 16px;
}
.wc-detail-team {
    text-align: center;
    color: #ffffff;
    font-weight: 800;
    text-transform: uppercase;
}
.wc-detail-team-flag {
    display: block;
    width: 216px;
    height: 144px;
    border-radius: 8px;
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    box-shadow: 0 8px 22px rgba(0,0,0,.28), 0 0 0 1px rgba(255,255,255,.18);
    margin: 0 auto 12px;
}
.wc-detail-vs {
    text-align: center;
}
.wc-detail-vs-text {
    color: #ffffff;
    font-size: 1.75rem;
    font-weight: 800;
    margin-bottom: 10px;
}
.wc-detail-prob-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(80px, 1fr));
    gap: 8px;
}
.wc-detail-prob {
    border-radius: 7px;
    padding: 10px 8px;
    color: #ffffff;
    box-shadow: inset 0 1px 0 rgba(255,255,255,.08);
    border: 1px solid rgba(255,255,255,.12);
}
.wc-detail-prob-home { background: linear-gradient(135deg, rgba(70, 126, 192, .95), rgba(42, 80, 130, .95)); }
.wc-detail-prob-draw { background: linear-gradient(135deg, rgba(72, 79, 87, .95), rgba(42, 48, 55, .95)); }
.wc-detail-prob-away { background: linear-gradient(135deg, rgba(30, 97, 55, .95), rgba(15, 69, 39, .95)); }
.wc-detail-prob-value {
    font-size: 1.55rem;
    font-weight: 800;
    line-height: 1;
}
.wc-detail-prob-label {
    font-size: .67rem;
    font-weight: 800;
    text-transform: uppercase;
    opacity: .88;
    margin-top: 6px;
}
.wc-detail-confidence {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    color: #b8c6d6;
    font-size: .75rem;
    margin-bottom: 18px;
}
.wc-detail-confidence-track {
    width: min(180px, 36vw);
    height: 6px;
    border-radius: 999px;
    background: rgba(255,255,255,.16);
    overflow: hidden;
}
.wc-detail-confidence-fill {
    display: block;
    height: 100%;
    width: var(--w);
    background: linear-gradient(90deg, #6fa8dc, #9fd4ff);
}
.wc-factor-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    border-top: 1px solid rgba(255,255,255,.08);
}
.wc-factor {
    text-align: center;
    padding: 12px 10px;
    border-left: 1px solid rgba(255,255,255,.08);
}
.wc-factor:first-child { border-left: 0; }
.wc-factor-label {
    color: #c6d1de;
    font-size: .68rem;
    font-weight: 800;
    text-transform: uppercase;
}
.wc-factor-value {
    color: #ffffff;
    font-size: 1.12rem;
    font-weight: 800;
    margin: 8px 0;
}
.wc-form-row {
    display: flex;
    justify-content: center;
    gap: 4px;
    margin: 8px 0;
}
.wc-form-chip {
    min-width: 18px;
    height: 18px;
    border-radius: 3px;
    background: #4c9d39;
    color: #ffffff;
    display: inline-grid;
    place-items: center;
    font-size: .68rem;
    font-weight: 800;
}
.wc-form-chip-D { background: #7f8b92; }
.wc-form-chip-L { background: #a74a45; }
.wc-factor-sub {
    color: #aebdcc;
    font-size: .72rem;
    line-height: 1.35;
}
.wc-detail-bottom {
    display: grid;
    grid-template-columns: .8fr 1.05fr 1.35fr;
    gap: 12px;
    margin-top: 14px;
}
.wc-detail-mini {
    background: rgba(13, 31, 49, .72);
    border: 1px solid rgba(130, 173, 222, .16);
    border-radius: 8px;
    padding: 14px;
}
.wc-detail-mini-title {
    color: #ffffff;
    font-size: .8rem;
    font-weight: 800;
    text-transform: uppercase;
    padding-bottom: 10px;
    margin-bottom: 12px;
    border-bottom: 1px solid rgba(255,255,255,.08);
}
.wc-score-big {
    color: #ffffff;
    font-size: 1.75rem;
    font-weight: 800;
    text-align: center;
}
.wc-score-sub {
    color: #cbd8e5;
    text-align: center;
    font-size: .82rem;
    margin-top: 8px;
}
.wc-xg-grid {
    display: grid;
    grid-template-columns: 1fr 42px 1fr;
    align-items: center;
    text-align: center;
    color: #ffffff;
}
.wc-xg-value {
    font-size: 1.35rem;
    font-weight: 800;
}
.wc-xg-ball {
    width: 34px;
    height: 34px;
    margin: 0 auto;
    border-radius: 50%;
    display: grid;
    place-items: center;
    background: rgba(255,255,255,.08);
    color: rgba(255,255,255,.35);
}
.wc-xg-team {
    color: #cbd8e5;
    font-size: .75rem;
    margin-top: 8px;
}
.wc-prob-svg {
    width: 100%;
    height: 118px;
}
@media (max-width: 900px) {
    .wc-detail-teams,
    .wc-detail-bottom,
    .wc-factor-grid {
        grid-template-columns: 1fr;
    }
    .wc-factor {
        border-left: 0;
        border-top: 1px solid rgba(255,255,255,.08);
    }
}
</style>
"""


def inject_css():
    st.markdown(CSS, unsafe_allow_html=True)


def _compact_html(html: str) -> str:
    return "".join(line.strip() for line in html.splitlines() if line.strip())


def kpi_card(label: str, value: str, sub: str = "", accent: str = "", icon: str = ""):
    accent_class = f" wc-card-{accent}" if accent else ""
    icon_html = f'<div class="wc-kpi-icon">{icon}</div>' if icon else ""
    st.markdown(
        f"""<div class="wc-card{accent_class}">
            {icon_html}
            <div class="wc-kpi-label">{label}</div>
            <div class="wc-kpi-value">{value}</div>
            <div class="wc-kpi-sub">{sub}</div>
        </div>""",
        unsafe_allow_html=True,
    )


def confidence_pill(label: str) -> str:
    css_class = {"High": "wc-pill-high", "Medium": "wc-pill-medium", "Low": "wc-pill-low"}.get(label, "wc-pill-medium")
    return f'<span class="wc-pill {css_class}">{label} confidence</span>'


def status_pill(status: str, played: bool) -> str:
    label = "Final" if played else str(status or "Scheduled").replace("_", " ").title()
    css_class = "wc-pill-high" if played else "wc-pill-medium"
    return f'<span class="wc-pill {css_class}">{label}</span>'


def probability_bar(home_pct: float, draw_pct: float, away_pct: float,
                     home_label: str, away_label: str):
    st.markdown(
        f"""
        <div class="wc-prob-bar-wrap">
            <div class="wc-prob-seg" style="width:{home_pct}%; background:#2e9e5b;"></div>
            <div class="wc-prob-seg" style="width:{draw_pct}%; background:#7a7a7a;"></div>
            <div class="wc-prob-seg" style="width:{away_pct}%; background:#c1473d;"></div>
        </div>
        <div class="wc-prob-labels">
            <span>{home_label} {home_pct:.0f}%</span>
            <span>Draw {draw_pct:.0f}%</span>
            <span>{away_label} {away_pct:.0f}%</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _form_chips(results: list) -> str:
    if not results:
        return '<span class="wc-factor-sub">No recent form</span>'
    return "".join(f'<span class="wc-form-chip wc-form-chip-{escape(str(r))}">{escape(str(r))}</span>' for r in results[-5:])


def _venue_advantage(match_row, team1, team2) -> tuple[str, str]:
    country = str(match_row.get("country", "") or "").strip()
    aliases = {"USA": "United States"}
    home_country = aliases.get(team1.name, team1.name)
    away_country = aliases.get(team2.name, team2.name)
    if country == home_country:
        return team1.name, f"{team1.name} host venue"
    if country == away_country:
        return team2.name, f"{team2.name} host venue"
    return "Neutral", "No significant home advantage"


def _projected_score(home_pct: float, draw_pct: float, away_pct: float) -> tuple[int, int]:
    if draw_pct >= home_pct and draw_pct >= away_pct:
        return 1, 1
    if home_pct >= away_pct:
        gap = home_pct - away_pct
        return (2, 0) if gap >= 45 else (2, 1)
    gap = away_pct - home_pct
    return (0, 2) if gap >= 45 else (1, 2)


def _expected_goal_proxy(home_pct: float, away_pct: float) -> tuple[float, float]:
    home_xg = 0.8 + (home_pct / 100) * 1.8
    away_xg = 0.8 + (away_pct / 100) * 1.8
    return home_xg, away_xg


def _probability_profile_svg(home_pct: float, draw_pct: float, away_pct: float) -> str:
    home_y = 98 - home_pct * 0.72
    away_y = 98 - away_pct * 0.72
    draw_y = 98 - draw_pct * 0.72
    return f"""
    <svg class="wc-prob-svg" viewBox="0 0 320 118" preserveAspectRatio="none" aria-hidden="true">
        <line x1="22" y1="18" x2="22" y2="98" stroke="rgba(255,255,255,.16)" />
        <line x1="22" y1="98" x2="304" y2="98" stroke="rgba(255,255,255,.16)" />
        <line x1="22" y1="58" x2="304" y2="58" stroke="rgba(255,255,255,.08)" />
        <text x="0" y="21" fill="rgba(255,255,255,.55)" font-size="9">100%</text>
        <text x="8" y="101" fill="rgba(255,255,255,.55)" font-size="9">0%</text>
        <polyline points="22,{home_y + 18:.1f} 70,{home_y + 4:.1f} 125,{home_y:.1f} 190,{home_y - 3:.1f} 245,{home_y - 6:.1f} 304,{home_y - 6:.1f}"
            fill="none" stroke="#6fa8dc" stroke-width="3" />
        <polyline points="22,{away_y - 6:.1f} 82,{away_y:.1f} 145,{away_y + 4:.1f} 220,{away_y + 10:.1f} 304,{away_y + 12:.1f}"
            fill="none" stroke="#6aa84f" stroke-width="3" />
        <polyline points="22,{draw_y:.1f} 100,{draw_y + 2:.1f} 180,{draw_y + 1:.1f} 304,{draw_y + 3:.1f}"
            fill="none" stroke="#9aa5b1" stroke-width="2" opacity=".9" />
        <text x="23" y="114" fill="rgba(255,255,255,.55)" font-size="9">prediction profile</text>
    </svg>
    """


def match_detail_panel(match_row, team1, team2, focus_team: str | None = None):
    played = bool(match_row.get("played", False))
    home_pct = float(match_row.get("home_win_probability", 0) or 0) * 100
    draw_pct = float(match_row.get("draw_probability", 0) or 0) * 100
    away_pct = float(match_row.get("away_win_probability", 0) or 0) * 100
    confidence = max(home_pct, draw_pct, away_pct)
    match_date = escape(str(match_row.get("match_date", match_row.get("date", "")) or ""))
    kickoff = escape(str(match_row.get("kickoff_time_utc", "") or ""))
    venue = escape(str(match_row.get("venue", "") or "TBD"))
    city = escape(str(match_row.get("city", "") or ""))
    country = escape(str(match_row.get("country", "") or ""))
    group = escape(str(match_row.get("group", "") or ""))
    status = escape(str(match_row.get("status", "SCHEDULED") or "SCHEDULED").replace("_", " ").title())
    score = escape(str(match_row.get("score_display", "TBD") or "TBD"))
    title = f"Group {group} - Match Preview"
    meta_bits = [match_date]
    if kickoff:
        meta_bits.append(f"{kickoff} UTC")
    meta_bits.append(", ".join(bit for bit in [venue, city, country] if bit))
    meta = " - ".join(bit for bit in meta_bits if bit)

    home_flag = _flag_image_html(team1, "wc-detail-team-flag")
    away_flag = _flag_image_html(team2, "wc-detail-team-flag")
    home_name = escape(team1.name)
    away_name = escape(team2.name)
    elo_diff = float(match_row.get("elo_difference", 0) or 0)
    stronger = team1.name if elo_diff >= 0 else team2.name
    if focus_team == team2.name:
        form_owner = team2
    elif focus_team == team1.name:
        form_owner = team1
    else:
        form_owner = team1 if team1.campaign_played >= team2.campaign_played else team2
    form_results = form_owner.campaign_results or form_owner.recent_form
    form_label = "This World Cup Form" if form_owner.campaign_results else "Recent Form"
    form_text = (
        f"{escape(form_owner.name)} current tournament form"
        if form_owner.campaign_results
        else f"{escape(form_owner.name)} pre-tournament form"
    )
    predicted_home, predicted_away = _projected_score(home_pct, draw_pct, away_pct)

    if played and score != "TBD":
        projected_home, projected_away = score.replace(" ", "").split("-")
        score_label = "Final Score"
        score_sub = status
    else:
        projected_home, projected_away = predicted_home, predicted_away
        score_label = "Predicted Score"
        score_sub = team1.name if projected_home > projected_away else team2.name if projected_away > projected_home else "Draw"
    key_score_label = "Predicted Score"
    key_score_sub = "Model-derived score proxy"

    home_xg, away_xg = _expected_goal_proxy(home_pct, away_pct)
    profile_svg = _probability_profile_svg(home_pct, draw_pct, away_pct)

    html = f"""<div class="wc-detail-shell">
            <div class="wc-detail-back">&larr; Match Details</div>
            <div class="wc-detail-head">
                <div class="wc-detail-title">{title}</div>
                <div class="wc-detail-meta">{meta}</div>
            </div>

            <div class="wc-detail-teams">
                <div class="wc-detail-team">{home_flag}<div>{home_name}</div></div>
                <div class="wc-detail-vs">
                    <div class="wc-detail-vs-text">VS</div>
                    <div class="wc-detail-prob-grid">
                        <div class="wc-detail-prob wc-detail-prob-home">
                            <div class="wc-detail-prob-value">{home_pct:.0f}%</div>
                            <div class="wc-detail-prob-label">{home_name} win</div>
                        </div>
                        <div class="wc-detail-prob wc-detail-prob-draw">
                            <div class="wc-detail-prob-value">{draw_pct:.0f}%</div>
                            <div class="wc-detail-prob-label">Draw</div>
                        </div>
                        <div class="wc-detail-prob wc-detail-prob-away">
                            <div class="wc-detail-prob-value">{away_pct:.0f}%</div>
                            <div class="wc-detail-prob-label">{away_name} win</div>
                        </div>
                    </div>
                </div>
                <div class="wc-detail-team">{away_flag}<div>{away_name}</div></div>
            </div>

            <div class="wc-detail-confidence">
                <span>Model Confidence</span>
                <span class="wc-detail-confidence-track"><span class="wc-detail-confidence-fill" style="--w:{confidence:.0f}%"></span></span>
                <span>{match_row.get("confidence_label", "Medium")}</span>
            </div>

            <div class="wc-detail-mini">
                <div class="wc-detail-mini-title">Key Factors</div>
                <div class="wc-factor-grid">
                    <div class="wc-factor">
                        <div class="wc-factor-label">Elo Difference</div>
                        <div class="wc-factor-value">{elo_diff:+.0f}</div>
                        <div class="wc-factor-sub">{escape(stronger)} stronger based on Elo rating</div>
                    </div>
                    <div class="wc-factor">
                        <div class="wc-factor-label">{form_label}</div>
                        <div class="wc-form-row">{_form_chips(form_results)}</div>
                        <div class="wc-factor-sub">{form_text}</div>
                    </div>
                    <div class="wc-factor">
                        <div class="wc-factor-label">Match Status</div>
                        <div class="wc-factor-value">{score if played else status}</div>
                        <div class="wc-factor-sub">{'Final result from live data' if played else 'Upcoming fixture from live data'}</div>
                    </div>
                    <div class="wc-factor">
                        <div class="wc-factor-label">{key_score_label}</div>
                        <div class="wc-factor-value">{predicted_home} - {predicted_away}</div>
                        <div class="wc-factor-sub">{key_score_sub}</div>
                    </div>
                </div>
            </div>

            <div class="wc-detail-bottom">
                <div class="wc-detail-mini">
                    <div class="wc-detail-mini-title">{score_label}</div>
                    <div class="wc-score-big">{projected_home} - {projected_away}</div>
                    <div class="wc-score-sub">{escape(str(score_sub))}</div>
                </div>
                <div class="wc-detail-mini">
                    <div class="wc-detail-mini-title">Expected Goals (proxy)</div>
                    <div class="wc-xg-grid">
                        <div><div class="wc-xg-value">{home_xg:.2f}</div><div class="wc-xg-team">{home_name}</div></div>
                        <div class="wc-xg-ball">⚽</div>
                        <div><div class="wc-xg-value">{away_xg:.2f}</div><div class="wc-xg-team">{away_name}</div></div>
                    </div>
                </div>
                <div class="wc-detail-mini">
                    <div class="wc-detail-mini-title">Win Probability Profile</div>
                    {profile_svg}
                </div>
            </div>
        </div>"""
    st.markdown(_compact_html(html), unsafe_allow_html=True)


def top_teams_panel(teams):
    if not teams:
        st.markdown('<div class="wc-panel"><div class="wc-panel-title">Top 10 strongest teams</div>No teams available.</div>',
                    unsafe_allow_html=True)
        return

    top = sorted(teams, key=lambda t: -t.elo)[:10]
    max_elo = max(t.elo for t in top)
    min_elo = min(t.elo for t in top)
    spread = max(max_elo - min_elo, 1)
    rows = []
    for i, team in enumerate(top, start=1):
        width = 58 + ((team.elo - min_elo) / spread) * 40
        flag_html = _flag_image_html(team)
        rows.append(
            f"""<div class="wc-team-rank">
                <span>{i}</span>
                {flag_html}
                <span>{team.name}</span>
                <span class="wc-rank-bar"><span class="wc-rank-fill" style="display:block;width:{width:.0f}%"></span></span>
                <span>{team.elo}</span>
            </div>"""
        )
    st.markdown(
        f"""<div class="wc-panel">
            <div class="wc-panel-title">Top 10 strongest teams <span style="font-weight:400;">(by Elo)</span></div>
            {''.join(rows)}
        </div>""",
        unsafe_allow_html=True,
    )


def qualification_panel(round_reach, top_n: int = 8):
    rows = []
    for _, row in round_reach.head(top_n).iterrows():
        pct = row["group_qualification_probability"] * 100
        rows.append(
            f"""<div class="wc-donut-item">
                <div class="wc-donut" style="--p:{pct:.0f};">{pct:.0f}%</div>
                <div class="wc-donut-name">{row.flag} {row.team}</div>
            </div>"""
        )
    st.markdown(
        f"""<div class="wc-panel">
            <div class="wc-panel-title">Qualification chance (top 8 teams)</div>
            <div class="wc-donut-grid">{''.join(rows)}</div>
        </div>""",
        unsafe_allow_html=True,
    )


def compact_matches_panel(matches, title: str, empty_message: str = "No matches available.", teams_by_name: dict | None = None):
    teams_by_name = teams_by_name or {}
    rows = []
    for _, match in matches.iterrows():
        date = match.get("match_date", match.get("date", ""))
        kickoff = match.get("kickoff_time_utc", "")
        group = str(match.get("group", "")).replace("GROUP_", "Group ")
        home = match.get("home_team", "")
        away = match.get("away_team", "")
        home_flag = getattr(teams_by_name.get(home), "flag", "")
        away_flag = getattr(teams_by_name.get(away), "flag", "")
        score = match.get("score_display", "TBD")
        home_tla = str(home)[:3].upper()
        away_tla = str(away)[:3].upper()
        if bool(match.get("played", False)):
            probs = f'<div class="wc-prob-chip"><span>{score}</span></div>'
        else:
            home_prob = match.get("home_win_probability", 0) * 100
            draw_prob = match.get("draw_probability", 0) * 100
            away_prob = match.get("away_win_probability", 0) * 100
            max_prob = max(home_prob, draw_prob, away_prob)
            home_fill = f'<div class="wc-prob-chip-fill" style="--w:{home_prob:.0f}%;"></div>' if home_prob == max_prob else ""
            draw_fill = f'<div class="wc-prob-chip-fill wc-prob-chip-fill-draw" style="--w:{draw_prob:.0f}%;"></div>' if draw_prob == max_prob else ""
            away_fill = f'<div class="wc-prob-chip-fill wc-prob-chip-fill-away" style="--w:{away_prob:.0f}%;"></div>' if away_prob == max_prob else ""
            probs = (
                f'<div class="wc-prob-chip">{home_fill}<span>{home_tla} {home_prob:.0f}%</span></div>'
                f'<div class="wc-prob-chip wc-prob-chip-muted">{draw_fill}<span>DRAW {draw_prob:.0f}%</span></div>'
                f'<div class="wc-prob-chip wc-prob-chip-away">{away_fill}<span>{away_tla} {away_prob:.0f}%</span></div>'
            )
        rows.append(
            f"""<div class="wc-compact-match">
                <div class="wc-compact-date">{date}<small>{kickoff} UTC<br>{group}</small></div>
                <div class="wc-compact-teams">
                    <div class="wc-compact-team">{home_flag} {home}</div>
                    <div class="wc-compact-vs">vs</div>
                    <div class="wc-compact-team">{away_flag} {away}</div>
                </div>
                <div class="wc-compact-probs">{probs}</div>
            </div>"""
        )

    body = "".join(rows) if rows else f'<div style="opacity:.72;font-size:.86rem;">{empty_message}</div>'
    st.markdown(
        f"""<div class="wc-panel">
            <div class="wc-panel-title">{title}</div>
            {body}
        </div>""",
        unsafe_allow_html=True,
    )


def group_stage_panel(group_name: str, standings, matches, teams_by_name: dict):
    group_rows = standings[standings.group == group_name].sort_values(
        ["points", "goal_difference", "goals_for"], ascending=[False, False, False]
    ).reset_index(drop=True)
    group_matches = matches[matches.group == group_name].sort_values(["match_date", "kickoff_time_utc"])

    expected_points = {row.team: float(row.points) for _, row in group_rows.iterrows()}
    xg_for = {row.team: 0.0 for _, row in group_rows.iterrows()}
    xg_against = {row.team: 0.0 for _, row in group_rows.iterrows()}
    for _, match in group_matches.iterrows():
        home = match.home_team
        away = match.away_team
        home_prob = float(match.home_win_probability)
        draw_prob = float(match.draw_probability)
        away_prob = float(match.away_win_probability)
        if not bool(match.played):
            expected_points[home] += home_prob * 3 + draw_prob
            expected_points[away] += away_prob * 3 + draw_prob
        home_xg, away_xg = _expected_goal_proxy(home_prob * 100, away_prob * 100)
        xg_for[home] += home_xg
        xg_against[home] += away_xg
        xg_for[away] += away_xg
        xg_against[away] += home_xg

    # Build the table separately so W/D/L can come from the Team objects.
    table_rows = []
    for rank, row in enumerate(group_rows.itertuples(index=False), start=1):
        team_obj = teams_by_name.get(row.team)
        flag = _flag_image_html(team_obj, "wc-group-flag-img") if team_obj else ""
        w = getattr(team_obj, "campaign_w", 0)
        d = getattr(team_obj, "campaign_d", 0)
        l = getattr(team_obj, "campaign_l", 0)
        gd = f"{int(row.goal_difference):+d}"
        pct = float(row.group_qualification_probability) * 100
        table_rows.append(
            f"""<div class="wc-group-row">
                <div class="wc-group-stat">{rank}</div>
                <div class="wc-group-team-cell">{flag}<span>{escape(row.team)}</span></div>
                <div class="wc-group-stat">{int(row.played)}</div>
                <div class="wc-group-stat">{int(w)}</div>
                <div class="wc-group-stat">{int(d)}</div>
                <div class="wc-group-stat">{int(l)}</div>
                <div class="wc-group-stat">{int(row.goals_for)}</div>
                <div class="wc-group-stat">{int(row.goals_against)}</div>
                <div class="wc-group-stat">{gd}</div>
                <div class="wc-group-stat">{int(row.points)}</div>
                <div class="wc-qual-cell">
                    <div class="wc-qual-bar">
                        <div class="wc-qual-fill" style="--w:{pct:.1f}%;"></div>
                        <span>{pct:.0f}%</span>
                    </div>
                </div>
            </div>"""
        )

    max_points = max(max(expected_points.values()), 8.0)
    colors = ["#6f93c7", "#a6815f", "#7fb34d", "#8b715c"]
    points_rows = []
    for i, row in enumerate(group_rows.itertuples(index=False)):
        pts = expected_points[row.team]
        width = (pts / max_points) * 100
        points_rows.append(
            f"""<div class="wc-points-row">
                <div>{escape(row.team)}</div>
                <div class="wc-points-track"><span class="wc-points-fill" style="--w:{width:.1f}%;background:{colors[i % len(colors)]};"></span></div>
                <div>{pts:.1f}</div>
            </div>"""
        )

    most_goals = group_rows.sort_values(["goals_for", "points"], ascending=[False, False]).iloc[0]
    best_defense = group_rows.sort_values(["goals_against", "points"], ascending=[True, False]).iloc[0]
    highest_xg_team = max(xg_for, key=xg_for.get)
    lowest_xga_team = min(xg_against, key=xg_against.get)

    upcoming = group_matches[~group_matches.played].head(3)
    next_cards = []
    for _, match in upcoming.iterrows():
        home_obj = teams_by_name.get(match.home_team)
        away_obj = teams_by_name.get(match.away_team)
        home_flag = _flag_image_html(home_obj, "wc-group-flag-img") if home_obj else ""
        away_flag = _flag_image_html(away_obj, "wc-group-flag-img") if away_obj else ""
        date_label = str(match.match_date)[5:].replace("-", " ")
        next_cards.append(
            f"""<div class="wc-next-card">
                <div class="wc-next-teams">
                    <div class="wc-next-team">{home_flag}<span>{escape(match.home_team)}</span></div>
                    <div style="text-align:center;opacity:.72;">vs</div>
                    <div class="wc-next-team">{away_flag}<span>{escape(match.away_team)}</span></div>
                </div>
                <div class="wc-next-date">{escape(date_label)}</div>
                <div class="wc-next-status">{escape(str(match.kickoff_time_utc or ""))} UTC</div>
            </div>"""
        )
    if not next_cards:
        next_cards.append('<div class="wc-next-card"><div class="wc-next-date">No upcoming group matches</div></div>')

    html = f"""<div class="wc-group-shell">
        <div class="wc-group-title">Group {escape(str(group_name))}</div>
        <div class="wc-group-table">
            <div class="wc-group-row wc-group-head">
                <div></div><div>Team</div><div class="wc-group-stat">P</div><div class="wc-group-stat">W</div>
                <div class="wc-group-stat">D</div><div class="wc-group-stat">L</div><div class="wc-group-stat">GF</div>
                <div class="wc-group-stat">GA</div><div class="wc-group-stat">GD</div><div class="wc-group-stat">PTS</div>
                <div class="wc-group-stat">Qualification<br>Probability</div>
            </div>
            {''.join(table_rows)}
        </div>
        <div class="wc-group-mid">
            <div class="wc-detail-mini">
                <div class="wc-detail-mini-title">Predicted Points (Final)</div>
                {''.join(points_rows)}
                <div class="wc-axis"><span>0</span><span>2</span><span>4</span><span>6</span><span>8</span></div>
            </div>
            <div class="wc-detail-mini">
                <div class="wc-detail-mini-title">Stats Overview</div>
                <div class="wc-stat-line"><span>Most Goals For</span><span class="wc-stat-value">{escape(most_goals.team)} ({int(most_goals.goals_for)})</span></div>
                <div class="wc-stat-line"><span>Best Defense</span><span class="wc-stat-value">{escape(best_defense.team)} ({int(best_defense.goals_against)} GA)</span></div>
                <div class="wc-stat-line"><span>Highest XG</span><span class="wc-stat-value">{escape(highest_xg_team)} ({xg_for[highest_xg_team]:.2f})</span></div>
                <div class="wc-stat-line"><span>Lowest XG Against</span><span class="wc-stat-value">{escape(lowest_xga_team)} ({xg_against[lowest_xga_team]:.2f})</span></div>
            </div>
        </div>
        <div class="wc-detail-mini" style="margin-top:16px;">
            <div class="wc-detail-mini-title">Next Matches - Group {escape(str(group_name))}</div>
            <div class="wc-next-grid">{''.join(next_cards)}</div>
        </div>
    </div>"""
    st.markdown(_compact_html(html), unsafe_allow_html=True)


def _prob_for_round(round_reach, team: str, column: str) -> float:
    row = round_reach[round_reach.team == team]
    if row.empty:
        return 0.0
    return float(row.iloc[0][column])


def _bracket_team_row(slot: str, team: str, prob: float, teams_by_name: dict, single: bool = False) -> str:
    team_obj = teams_by_name.get(team)
    flag = _flag_image_html(team_obj, "wc-group-flag-img") if team_obj else ""
    pct = f"{prob * 100:.0f}%"
    extra = " wc-bracket-single" if single else ""
    slot_html = "" if single else f'<span class="wc-bracket-slot">{escape(slot)}</span>'
    return (
        f'<div class="wc-bracket-team{extra}">'
        f'{slot_html}{flag}<span class="wc-bracket-team-name">{escape(team)}</span>'
        f'<span class="wc-bracket-prob">{pct}</span></div>'
    )


def _winner_from_pair(pair: tuple[str, str], round_reach, column: str) -> str:
    a, b = pair
    return a if _prob_for_round(round_reach, a, column) >= _prob_for_round(round_reach, b, column) else b


def knockout_bracket_panel(standings, round_reach, teams_by_name: dict):
    ranked_groups = {
        group: g.sort_values(["points", "goal_difference", "goals_for"], ascending=[False, False, False]).reset_index(drop=True)
        for group, g in standings.groupby("group")
    }

    slots = {}
    third_rows = []
    for group, rows in ranked_groups.items():
        if len(rows) >= 1:
            slots[f"1{group}"] = rows.iloc[0].team
        if len(rows) >= 2:
            slots[f"2{group}"] = rows.iloc[1].team
        if len(rows) >= 3:
            third = rows.iloc[2].copy()
            third["slot_group"] = group
            third_rows.append(third)

    third_ranked = sorted(
        third_rows,
        key=lambda r: (r.points, r.goal_difference, r.goals_for, r.group_qualification_probability),
        reverse=True,
    )[:8]
    for i, row in enumerate(third_ranked, start=1):
        slots[f"Best 3rd #{i}"] = row.team

    slot_pairs = [
        ("1A", "2B"), ("1B", "2A"), ("1C", "2D"), ("1D", "2C"),
        ("1E", "2F"), ("1F", "2E"), ("1G", "2H"), ("1H", "2G"),
        ("1I", "2J"), ("1J", "2I"), ("1K", "2L"), ("1L", "2K"),
        ("Best 3rd #1", "Best 3rd #2"), ("Best 3rd #3", "Best 3rd #4"),
        ("Best 3rd #5", "Best 3rd #6"), ("Best 3rd #7", "Best 3rd #8"),
    ]
    r32_pairs = [(a, b, slots.get(a, "TBD"), slots.get(b, "TBD")) for a, b in slot_pairs]

    r32_cards = []
    r16_teams = []
    for slot_a, slot_b, team_a, team_b in r32_pairs:
        prob_a = _prob_for_round(round_reach, team_a, "round_of_16")
        prob_b = _prob_for_round(round_reach, team_b, "round_of_16")
        r16_teams.append(_winner_from_pair((team_a, team_b), round_reach, "round_of_16"))
        r32_cards.append(
            f'<div class="wc-bracket-match">'
            f'{_bracket_team_row(slot_a, team_a, prob_a, teams_by_name)}'
            f'{_bracket_team_row(slot_b, team_b, prob_b, teams_by_name)}'
            f'</div>'
        )

    def round_cards(source_teams: list[str], reach_col: str, next_col: str) -> tuple[list[str], list[str]]:
        cards = []
        winners = []
        for i in range(0, len(source_teams), 2):
            team_a, team_b = source_teams[i], source_teams[i + 1]
            prob_a = _prob_for_round(round_reach, team_a, reach_col)
            prob_b = _prob_for_round(round_reach, team_b, reach_col)
            winners.append(_winner_from_pair((team_a, team_b), round_reach, next_col))
            cards.append(
                f'<div class="wc-bracket-match">'
                f'{_bracket_team_row("", team_a, prob_a, teams_by_name, single=True)}'
                f'{_bracket_team_row("", team_b, prob_b, teams_by_name, single=True)}'
                f'</div>'
            )
        return cards, winners

    r16_cards, qf_teams = round_cards(r16_teams, "quarterfinal", "quarterfinal")
    qf_cards, sf_teams = round_cards(qf_teams, "semifinal", "semifinal")
    sf_cards, final_teams = round_cards(sf_teams, "final", "final")

    final_cards = []
    if len(final_teams) >= 2:
        final_cards.append(
            f'<div class="wc-bracket-match">'
            f'{_bracket_team_row("", final_teams[0], _prob_for_round(round_reach, final_teams[0], "tournament_win_probability"), teams_by_name, single=True)}'
            f'{_bracket_team_row("", final_teams[1], _prob_for_round(round_reach, final_teams[1], "tournament_win_probability"), teams_by_name, single=True)}'
            f'</div>'
        )

    top_winners = round_reach.head(4)
    champion = top_winners.iloc[0]
    champion_obj = teams_by_name.get(champion.team)
    champion_flag = _flag_image_html(champion_obj, "wc-group-flag-img") if champion_obj else ""
    winner_rows = []
    title_cards = []
    for rank, row in enumerate(top_winners.itertuples(index=False), start=1):
        team_obj = teams_by_name.get(row.team)
        flag = _flag_image_html(team_obj, "wc-group-flag-img") if team_obj else ""
        winner_rows.append(
            f'<div class="wc-winner-row">{flag}<span>{escape(row.team)}</span><span>{row.tournament_win_probability * 100:.0f}%</span></div>'
        )
        title_cards.append(
            f"""<div class="wc-title-card">
                <div class="wc-title-rank">{rank}</div>
                <div>
                    <div class="wc-title-team">{flag} {escape(row.team)}</div>
                    <div class="wc-title-prob">{row.tournament_win_probability * 100:.0f}%</div>
                </div>
            </div>"""
        )

    html = f"""<div class="wc-bracket-shell">
        <div class="wc-bracket-tabs">
            <div class="wc-bracket-tab wc-bracket-tab-active">Round of 32</div>
            <div class="wc-bracket-tab">Round of 16</div>
            <div class="wc-bracket-tab">Quarter Finals</div>
            <div class="wc-bracket-tab">Final</div>
        </div>
        <div class="wc-bracket-grid">
            <div>
                <div class="wc-bracket-col-title">Round of 32 - projected from live standings</div>
                <div class="wc-bracket-col">{''.join(r32_cards)}</div>
            </div>
            <div>
                <div class="wc-bracket-col-title">Round of 16</div>
                <div class="wc-bracket-col wc-bracket-col-r16">{''.join(r16_cards)}</div>
            </div>
            <div>
                <div class="wc-bracket-col-title">Quarter Finals</div>
                <div class="wc-bracket-col wc-bracket-col-qf">{''.join(qf_cards)}</div>
            </div>
            <div>
                <div class="wc-bracket-col-title">Semi Finals</div>
                <div class="wc-bracket-col wc-bracket-col-sf">{''.join(sf_cards)}</div>
            </div>
            <div class="wc-bracket-winner">
                <div class="wc-trophy">🏆</div>
                <div class="wc-winner-title">Winner</div>
                <div class="wc-winner-main">{champion_flag}<span>{escape(champion.team)}</span><span>{champion.tournament_win_probability * 100:.0f}%</span></div>
                <div class="wc-winner-list">{''.join(winner_rows[1:])}</div>
            </div>
        </div>
        <div class="wc-detail-mini" style="margin-top:18px;">
            <div class="wc-detail-mini-title">Chance to Win the Tournament</div>
            <div class="wc-title-card-grid">{''.join(title_cards)}</div>
        </div>
    </div>"""
    st.markdown(_compact_html(html), unsafe_allow_html=True)


def team_stats_dashboard(teams: list, standings, round_reach, selected_team: str | None = None):
    teams_by_name = {t.name: t for t in teams}
    rr = round_reach.set_index("team")
    st_by_team = standings.set_index("team")

    def team_row(name: str):
        return teams_by_name[name], st_by_team.loc[name], rr.loc[name]

    highest_elo = max(teams, key=lambda t: t.elo)
    most_points_name = standings.sort_values(["points", "goal_difference"], ascending=[False, False]).iloc[0].team
    most_goals_name = standings.sort_values(["goals_for", "points"], ascending=[False, False]).iloc[0].team
    best_def_name = standings.sort_values(["goals_against", "points"], ascending=[True, False]).iloc[0].team
    best_qual_name = round_reach.sort_values(["group_qualification_probability", "tournament_win_probability"], ascending=[False, False]).iloc[0].team
    fav_name = round_reach.sort_values("tournament_win_probability", ascending=False).iloc[0].team

    card_specs = [
        ("Highest Elo", highest_elo.name, f"{highest_elo.elo}", "Elo rating", "blue"),
        ("Most Points", most_points_name, f"{int(st_by_team.loc[most_points_name].points)}", "points", "green"),
        ("Most Goals", most_goals_name, f"{int(st_by_team.loc[most_goals_name].goals_for)}", "goals for", ""),
        ("Best Defense", best_def_name, f"{int(st_by_team.loc[best_def_name].goals_against)}", "goals against", "purple"),
        ("Best Qualification", best_qual_name, f"{rr.loc[best_qual_name].group_qualification_probability * 100:.0f}%", "qualification chance", "green"),
        ("Tournament Favorite", fav_name, f"{rr.loc[fav_name].tournament_win_probability * 100:.0f}%", "win probability", "gold"),
    ]

    cards = []
    for label, name, value, sub, accent in card_specs:
        team = teams_by_name[name]
        flag = _flag_image_html(team, "wc-team-stat-flag")
        accent_class = f" wc-team-stat-card-{accent}" if accent else ""
        cards.append(
            f"""<div class="wc-team-stat-card{accent_class}">
                <div class="wc-team-stat-label">{label}</div>
                <div class="wc-team-stat-value">{value}</div>
                <div class="wc-team-stat-sub">{sub}</div>
                <div class="wc-team-stat-name">{escape(name)}</div>
                {flag}
            </div>"""
        )

    ranking_names = [t.name for t in sorted(teams, key=lambda t: -t.elo)[:10]]
    table_rows = []
    for rank, name in enumerate(ranking_names, start=1):
        team, standing, reach = team_row(name)
        flag = _flag_image_html(team, "wc-group-flag-img")
        table_rows.append(
            f"""<div class="wc-team-table-row">
                <div>{rank}</div>
                <div class="wc-team-table-team">{flag}<span>{escape(name)}</span></div>
                <div>{escape(team.group)}</div>
                <div>{int(standing.played)}</div>
                <div>{int(standing.points)}</div>
                <div>{int(standing.goals_for)}</div>
                <div>{team.elo}</div>
                <div>{reach.tournament_win_probability * 100:.1f}%</div>
            </div>"""
        )

    impact_df = standings.merge(round_reach[["team", "tournament_win_probability"]], on="team")
    impact_df["impact_score"] = (
        impact_df["points"] * 9
        + impact_df["goal_difference"] * 3
        + impact_df["group_qualification_probability"] * 25
        + impact_df["tournament_win_probability"] * 100
    )
    impact_df = impact_df.sort_values("impact_score", ascending=False).head(10)
    max_impact = max(float(impact_df["impact_score"].max()), 1.0)
    impact_rows = []
    for rank, row in enumerate(impact_df.itertuples(index=False), start=1):
        width = float(row.impact_score) / max_impact * 100
        impact_rows.append(
            f"""<div class="wc-team-impact-row">
                <div>{rank}</div><div>{escape(row.team)}</div>
                <div class="wc-team-impact-bar"><span class="wc-team-impact-fill" style="--w:{width:.1f}%;"></span></div>
                <div>{row.impact_score:.1f}</div>
            </div>"""
        )

    goals_df = standings.sort_values(["goals_for", "points"], ascending=[False, False]).head(8)
    max_goals = max(float(goals_df["goals_for"].max()), 1.0)
    goal_rows = []
    for row in goals_df.itertuples(index=False):
        width = float(row.goals_for) / max_goals * 100
        goal_rows.append(
            f"""<div class="wc-team-bar-row">
                <div>{escape(row.team)}</div>
                <div class="wc-team-bar-track"><span class="wc-team-bar-fill" style="--w:{width:.1f}%;"></span></div>
                <div>{int(row.goals_for)}</div>
            </div>"""
        )

    defense_df = standings.sort_values(["goals_against", "points"], ascending=[True, False]).head(5)
    defense_donuts = []
    max_ga = max(float(standings["goals_against"].max()), 1.0)
    for row in defense_df.itertuples(index=False):
        pct = max(0, 100 - (float(row.goals_against) / max_ga) * 100)
        defense_donuts.append(
            f"""<div class="wc-donut-item">
                <div class="wc-donut" style="--p:{pct:.0f};">{int(row.goals_against)}</div>
                <div class="wc-donut-name">{escape(row.team)}<br><span style="opacity:.7;">GA</span></div>
            </div>"""
        )

    selected = teams_by_name.get(selected_team) or teams[0]
    selected_rr = rr.loc[selected.name]
    selected_st = st_by_team.loc[selected.name]
    selected_flag = _flag_image_html(selected, "wc-group-flag-img")
    selected_form = " ".join(selected.campaign_results or selected.recent_form) or "n/a"

    html = f"""<div class="wc-panel">
        <div class="wc-panel-title">Top Team Performers Overview</div>
        <div class="wc-team-stats-grid">{''.join(cards)}</div>
    </div>
    <div class="wc-team-dashboard-grid">
        <div class="wc-detail-mini">
            <div class="wc-detail-mini-title">Top Teams Overview</div>
            <div class="wc-team-table">
                <div class="wc-team-table-row wc-team-table-head">
                    <div>#</div><div>Team</div><div>Grp</div><div>P</div><div>Pts</div><div>GF</div><div>Elo</div><div>Win %</div>
                </div>
                {''.join(table_rows)}
            </div>
        </div>
        <div class="wc-detail-mini">
            <div class="wc-detail-mini-title">Team Impact Ranking</div>
            <div class="wc-team-note">Impact combines live points, goal difference, qualification chance, and title probability.</div>
            {''.join(impact_rows)}
        </div>
        <div class="wc-detail-mini">
            <div class="wc-detail-mini-title">Goals Scored</div>
            <div class="wc-team-bars">{''.join(goal_rows)}</div>
        </div>
    </div>
    <div class="wc-mini-panel-grid">
        <div class="wc-detail-mini">
            <div class="wc-detail-mini-title">Best Defenses</div>
            <div class="wc-team-donut-row">{''.join(defense_donuts)}</div>
        </div>
        <div class="wc-detail-mini">
            <div class="wc-detail-mini-title">Selected Team</div>
            <div class="wc-score-big">{selected_flag} {escape(selected.name)}</div>
            <div class="wc-score-sub">Group {escape(selected.group)} | {escape(selected.confederation)}</div>
            <div class="wc-team-note">Form: {escape(selected_form)} | {int(selected_st.points)} pts | GF {int(selected_st.goals_for)} / GA {int(selected_st.goals_against)}</div>
        </div>
        <div class="wc-detail-mini">
            <div class="wc-detail-mini-title">Tournament Outlook</div>
            <div class="wc-stat-line"><span>Qualification Chance</span><span class="wc-stat-value">{selected_rr.group_qualification_probability * 100:.1f}%</span></div>
            <div class="wc-stat-line"><span>Round of 16</span><span class="wc-stat-value">{selected_rr.round_of_16 * 100:.1f}%</span></div>
            <div class="wc-stat-line"><span>Quarterfinal</span><span class="wc-stat-value">{selected_rr.quarterfinal * 100:.1f}%</span></div>
            <div class="wc-stat-line"><span>Win Tournament</span><span class="wc-stat-value">{selected_rr.tournament_win_probability * 100:.1f}%</span></div>
        </div>
    </div>"""
    st.markdown(_compact_html(html), unsafe_allow_html=True)


def match_card(match_row, team1, team2):
    st.markdown('<div class="wc-match-card">', unsafe_allow_html=True)

    played = bool(match_row.get("played", False))
    score_display = match_row.get("score_display", "TBD")
    status = match_row.get("status", "SCHEDULED")
    match_date = match_row.get("match_date", match_row.get("date", ""))
    kickoff_time = match_row.get("kickoff_time_utc", "")
    if played:
        st.markdown(
            f"""<div class="wc-team-row">
                <span>{team1.flag} {team1.name}</span>
                <span style="opacity:0.9; font-weight:700;">{score_display}</span>
                <span>{team2.name} {team2.flag}</span>
            </div>""",
            unsafe_allow_html=True,
        )
        st.markdown(status_pill(status, played), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        return

    home_pct = match_row["home_win_probability"] * 100
    draw_pct = match_row["draw_probability"] * 100
    away_pct = match_row["away_win_probability"] * 100

    st.markdown(
        f"""<div class="wc-team-row">
            <span>{team1.flag} {team1.name}</span>
            <span style="opacity:0.6; font-weight:400;">{score_display if score_display != "TBD" else "vs"}</span>
            <span>{team2.name} {team2.flag}</span>
        </div>""",
        unsafe_allow_html=True,
    )
    probability_bar(home_pct, draw_pct, away_pct, team1.name, team2.name)
    if match_date or kickoff_time:
        st.markdown(
            f'<div class="wc-match-meta">Kickoff: {match_date} {kickoff_time} UTC</div>',
            unsafe_allow_html=True,
        )
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            status_pill(status, played) + " " + confidence_pill(match_row["confidence_label"]),
            unsafe_allow_html=True,
        )
    with c2:
        if match_row["upset_risk_score"] >= 0.7:
            st.markdown(f'<span class="wc-upset">\u26a0 Upset potential ({match_row["upset_risk_score"]:.2f})</span>',
                         unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
