# 24. country-meta-deprecation

Date: 2026-04-08

## Status

Accepted

## Context

Currently, the system has two country related fields:

- Country as in organisational center
- Language as in supported language

## Decision

The Country meta field itself is deprecated and will be rescoped into a meta field describing a operational center.

The Language meta field won't be changed.

## Consequences

Requires re import of the entire matrix.
