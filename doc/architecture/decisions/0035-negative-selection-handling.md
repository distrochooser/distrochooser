# 35. Negative selection handling

Date: 2026-10-29

## Status

Accepted

## Context

There are situations where a user might consider a facette selected as a "no-go" rather than a negative flag. 

## Decision

`FacetteSelections` receive a `negative_handling_active`flag, which is managed like the weight.

On calculation of results, the type of the assignment will be overwritten. A copy is used in the maps.

## Consequences

A new map is rerquired in the context to pass the information to the frontend/ `RankedChoosable` serializer.
