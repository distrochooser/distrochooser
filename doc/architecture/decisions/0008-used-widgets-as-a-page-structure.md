# 8. Used Widgets as a page structure

Date: 2025-06-28

## Status

Accepted

## Context

In previous versions, the project UI structure consists out pages chaned together, in v5, the page order was defined in a database, 
but only allows separation between media, checkbox or radio questions. This limits the page structure and options.

## Decision

The page structure consists out of a fixed outer structure which is defined on the client template. Each page consist out of a 12-grid
like structure where each content is a `Widget`.

Each `Widget` needs to be serialized (using Django Rest Framework) and rendered on the client (using the `WidgetWrapper.vue`), allowing different page structures based on user feedback.

## Consequences

This enlarges the code base quite a lot, but based on the advantages of variable page layout this approach will be followed.
