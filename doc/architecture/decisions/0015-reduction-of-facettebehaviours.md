# 15. Reduction of `FacetteBehaviours`

Date: 2025-06-29

## Status

Accepted

## Context

Facette Behaviours have a criticality, a description and a direction. This complexity increases maintenance effort.

## Decision

As the core function behind the behaviours is to display conflicting answers, the `FacetteBehaviour` is reduced to this functionality.
Also, no descriptivie text is displayed to reduce translation efforts.

Additionally, there is no direction anymore, a bidirectional relationship is assumed.

## Consequences

Complex relationships between `Facettes` can't be implemented for now.
