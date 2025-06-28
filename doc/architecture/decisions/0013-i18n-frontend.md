# 13. Frontend translation

Date: 2025-06-28

## Status

Accepted

## Context

Translation needs to be properly used.

## Decision

The frontend implements and refers translation only by their key and uses a central `__i` function to receive the translation.


## Consequences

The translation "haystack" need to be delivered to the client at all times and the function needs to distiguish between "static" translation values
and the values referring to an `Translatable` (see [0012. i18n (JSON)](0012-i18n.md)).

Also this must work properly with the feedback defined in [0011. Feedback](0011-feedback.md)
