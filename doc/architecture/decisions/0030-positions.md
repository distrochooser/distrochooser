# 30. positions

Date: 2026-07-05

## Status

Accepted

## Context

Based on user feedback, the result list lacks an identifier about the ranking of the list.

## Decision

`RankedChoosables` wil retrieve a numberic position.

## Consequences

If two `RankedChoosables` have an identical score, they will retrieve the same position. No further ranking will be carried out.

To explain this, the `ResultListWidget` receives an explanatory text.
