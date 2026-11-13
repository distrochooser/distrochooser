# 38. next-page

Date: 2026-11-06

## Status

Accepted

## Context

The `Page` model features several artefacts which belong to the "Monolith era" of Distrochooser 6:
- `is_visible` 
- `next_page` 
- `previous_page` 

While `is_visible`  and `previous_page` are `@property` functions, `next_page` is a field. The field's purpose is to allow to create a chain, based on the `SessionVersion` linked in the `Session` applied. As with v6.8.0, this leads to issues and increases complexity.

## Decision

1. The mentioned artefacts are removed.
2. A `index` field is added to the `Page` model.
3. Ordering of pages is controlled by the `index` field (via `order_by`) and `get_session_version_pages` returns the queryset instead of needing a linked chain

## Consequences

The index field is numeric and variance in `SessionVersion` of the questionnaire are not possible besides on/ off.
