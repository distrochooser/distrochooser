# 14. Questionnaire Versions

Date: 2025-06-28

## Status

Superceded by [29. questionnaire versions](0029-questionnaire-versions.md)

## Context

Some users have a hard time with technical questions. For this users, an adapted variant of the questionnaire shall be avaiable.

## Decision

`Pages` are negatively bound to `SessionVersion` objects to allow them being hidden for these `SessionVersion`. On import, e. g. a 
"simplified" version is created and each technical question cannow be hidden.

## Consequences

Only `Page` objects relate to the `SessionVersion`. While the pages can be hidden, some result descriptions might be still technical
as they do not correlate with the `SessionVersion` itself.
