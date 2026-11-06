# 36. Violations

Date: 2026-10-30

## Status

Accepted

## Context

Some bots show excessive crawling amounts per month.

## Decision

A `violation` class is integerated, which can permanentely or temporary ban a user agent.

The frontend page and all info pages will utili9ze the `HardSessionFail` component to display an error.

## Consequences

There might be the need for some kind of auto banning
