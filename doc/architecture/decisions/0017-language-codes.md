# 17. Language codes

Date: 2025-07-05

## Status

Accepted

Supercedes [9. ISO Language Code usage](0009-iso-language-code-usage.md)

## Context

Users are not used to ISO-639-3 codes, additionally, *some* users have ISO-639-1 like codes in `navigator.language`.

## Decision

We are moving back to ISO-639-1 codes.

## Consequences

We can add some kind of language check to the frontend.
The language keys must be reconfigured.

