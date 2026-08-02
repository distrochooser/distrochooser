# 31. range meta filter

Date: 2026-08-02

## Status

Accepted

## Context

Distrochooser impelements `MetaFilterValues` which allow the user to filter by additional values not covered by `Facette`objects.

Examples:

- Countries (as in operational centers) (select, multiple)
- Supported architectures (select, multiple)
- Age of the distribution (number, single)

## Decision

To cover the release interval of a given distribution, a new type is implemented, adding a `<input type='range'/>` to the `Cell` component.
The user can name a minimal interval in years. Distributions receive a `positive` hit and no hit if not matching.

## Consequences

1. It might be required to add a `negative` hit when the minimal does not match the user requirement.
2. Mapping updates are required
3. There are currently no options for additional attributes, such as `step=<number>`