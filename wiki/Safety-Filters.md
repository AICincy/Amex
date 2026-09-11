# Safety Filters

Crowd Control and Reputation are Reddit Safety Filters. They are not AutoMod. Do not encode them as YAML. Do not toggle them from this repository.

## Crowd Control

Recorded inspect on 2026-09-11:

1. Posts On, comments On, Targeting Moderate, comments Collapse.
2. Operator then set posts Off and comments Off.

Draft rule: leave posts and comments Off unless a separate influx or abuse problem requires a filter.

Crowd Control is not the 1e floor. Moderate filtering on posts and comments will hide people who are not yet well-known, including ordinary posts and comments outside the monthly thread.

## Reputation

Inspect only. Reputation is not a substitute for Rule 1e. Do not treat it as the participation check.

## Dual engine

AutoMod YAML and Safety Filters can both act on the same user. When users report being blocked outside the monthly thread, inspect Crowd Control before changing 1e.
