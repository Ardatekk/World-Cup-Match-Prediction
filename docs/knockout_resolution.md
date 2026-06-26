# Knockout Fixture Resolution

## Purpose

The dashboard receives live World Cup match data from `football-data.org`, but knockout fixtures can remain as empty placeholders until the provider fills both teams. The knockout resolution step creates a separate processed dataset that resolves known knockout slots from completed group standings without overwriting the live feed.

Output:

```text
data/processed/knockout_matches.csv
```

## Input Files

```text
data/processed/live_matches.csv
data/processed/wc_2026_fixtures_enriched.csv
```

`live_matches.csv` provides completed group results, match IDs, match dates, kickoff times, statuses, and scores.

`wc_2026_fixtures_enriched.csv` provides existing knockout fixture metadata such as venue, city, and country.

## Standings Logic

The resolver computes standings from finished group-stage matches in `live_matches.csv`.

For each team it calculates:

- matches played
- wins
- draws
- losses
- goals for
- goals against
- goal difference
- points

Teams are sorted by:

1. points
2. goal difference
3. goals for
4. team name

The resolver only resolves `1A`, `2A`, etc. for groups where all four teams have played three matches. This avoids treating an unfinished group table as final.

## Resolved Slots

The resolver supports simple group placement slots:

```text
1A, 2A
1B, 2B
...
1L, 2L
```

Example:

```text
1F = Group F winner
2C = Group C runner-up
```

## Unresolved Slots

Third-place slots are not guessed.

Examples:

```text
3A/B/C/D/F
3C/D/F/G/H
3E/F/G/I/J
```

These remain unresolved until the project implements the official third-place allocation logic.

Future-round slots also remain unresolved until prior knockout matches are played:

```text
W73
L101
Finalist 1
```

## Fixture Skeleton Limitation

The existing `wc_2026_fixtures_enriched.csv` knockout skeleton uses simplified placeholder pairings such as `1F vs 2E`.

The official Round of 32 schedule includes `1F vs 2C`, which is the slot path that resolves to Netherlands vs Morocco when Group F and Group C are complete in the current data.

Because of that mismatch, the resolver keeps the existing enriched fixture file unchanged and writes a separate `knockout_matches.csv` using an official slot map. Venue metadata is still taken from the existing fixture skeleton by row order, so venue details should be reviewed if the skeleton is later corrected.

## Dashboard Integration

The dashboard bracket now follows this priority:

1. use `data/processed/knockout_matches.csv` when available
2. fallback to the previous projected bracket from live standings

This keeps the current dashboard behavior safe while allowing confirmed knockout matchups to appear as soon as the resolver can determine them.

## Current Known Result

With the current local data:

```text
1F = Netherlands
2C = Morocco
```

So `knockout_matches.csv` resolves:

```text
Netherlands vs Morocco
```

## Limitations

- No hardcoded team-vs-team matchups are used.
- Third-place allocation is intentionally unresolved.
- Tiebreakers beyond points, goal difference, goals for, and team name are not implemented.
- Venue metadata depends on the current fixture skeleton and may need correction if the skeleton is updated to the official match-number structure.
