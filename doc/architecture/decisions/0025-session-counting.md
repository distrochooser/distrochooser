# 25. session-counting

Date: 2026-04-24

## Status

Accepted

## Context

The project features a "global" test count. The count result consists out of a offset (derived from the sum of all previous versions) and the amount of finished sessions. Parallel operations of versions are not included in the count as "old.distrochooser.de" instances are only kept for a limited time after release switch.

As the site is crawled, there must be some distinguishing done to separate "visitors" from "results". There is no persistend tracking and/ or canvas fingerprinting (or similar) done. Returning users will be considered as a new visitor and/ or new result, if requested.

## Decision

- Sessions (as in `.all().count()`) are considered as visitors
- Sessions (as in `.exclude(is_ack=True).count()`) are considered as results

## Consequences

A session is only considered as a result when a list of choosables was delivered. 
During generation of the result list, the `is_ack`-flag is set.
