# 29. questionnaire versions

Date: 2026-07-05

## Status

Accepted

Supercedes [14. Questionnaire Versions](0014-questionnaire-versions.md)

## Context

Some users have a hard time with technical questions. For this users, an adapted variant of the questionnaire shall be avaiable.

## Decision

`Pages` are negatively bound to `SessionVersion` objects to allow them being hidden for these `SessionVersion`. On import, e. g. a 
"simplified" version is created and each technical question cannow be hidden.

The results are static and `Session`-agnostic. As some `Facettes` within a `Page` (and it's corresponding `Widget`) require `SessionVersion` based display or hiding, these are filtered on the client side to prevent the need to have to cleanup caches frequently and deep when a `Version` is switched.

The session will be created without an actual `SessionVersion`, on switch there is the option to switch to a `full` version, which has no meta-feature, it's just selected, but not referred in a `Page.not_in_versions` nor `Facette.not_in_versions`.

## Consequences

`Page` objects relate to the `SessionVersion`. While the pages can be hidden server-sided, some result descriptions might be still technical
as they do not correlate with the `SessionVersion` itself.

`Facette` objects can also link a given `SessionVersion, but will still be transferred for the client for clients-die filtering.
