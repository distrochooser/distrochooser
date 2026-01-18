# 19. Annotation workflow

Date: 2026-01-18

## Status

Accepted

## Context

If a user provides a new distribution, the matrix must be updated.
The process is quite complex, and there is a management command `annotate` to help identify missing translation values.

## Decision

No automated processes will be executed (was previously evaluated on https://github.com/distrochooser/distrochooser/pull/396)

## Consequences

The `annotate` command must be run locally, therefore must be either carried out by a maintainer of the repo or by the user themself.