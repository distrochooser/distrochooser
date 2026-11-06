# 37. facette-images

Date: 2026-11-04

## Status

Accepted

## Context

`Facettes` can currently either be a checkbox or a radio element. There are question contexts where a descriptive image can help the user to understand the `Facette` better.

## Decision

The `Facette` model receives a `image_path`and `image_credit`. Both are string, the first containing a URL to the image to use, the second an descriptive text about license, author, source etc.

## Consequences

1. Mixing of image with non image facette within the same topic makes no sense, even as the `FacetteSelectionWidget` will display them.
2. The `FacetteSelectionWidget` renders images of facettes, but requires that an wrapping container is present, as the image facettes are rendered as col's, while non-image facettes are just divs containing an input/ label combination.