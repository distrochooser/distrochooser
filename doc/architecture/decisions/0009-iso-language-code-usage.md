# 9. ISO Language Code usage

Date: 2025-06-28

## Status

Accepted

## Context

Translations must be identified.

## Decision

In the past, a pseudo ISO-639-1 code was used, but does not covere related languages and/ or languages of the same family.
To address this issue, ISO-639-3 shall be used.

## Consequences

Browsers seem to utilize ISO-639-1, so no language identification can be used on the client directly, thus only the fallback to the english locale
is available then.
