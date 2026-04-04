# 22. Translateable-Deprecation

Date: 2026-04-03

## Status

Accepted

## Context

Models which feature a translation of eat least one field use a `Translateable` as a basis. 
This base model offers the features to provide the translation. 
This approach worked, but caused an longer load time during runtime, resulting in not-acceptable delays on load.

## Decision

The `Translateable` approach is deprecated.

Following steps has been carried out:

- Removal of the `Translateable` base class
- Merge of the migrations (which will require a reset of the beta)
- Introduction of a individual `catalogue_id`
- Removal of the `is_invalidated` attribute

## Consequences

The translation feedback mode is disabled for now as it requires a rework. Translation values will be delivered to the client using the translation keys, wher possible.
Translated values shall not be transferred to the client.
