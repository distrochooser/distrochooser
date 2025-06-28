# 4. HTTP Interface

Date: 2025-06-28

## Status

Accepted

## Context

The new frontend needs to communicate with the backend.

## Decision

In past versions, the components utilize simple HTTP calls to communicate, using hand-written endpoints as a medium.
This requires double effort, as the interface needs to be written on the server and an consuming API needs to be written
on the client aswell.

As this is not feasible for a one man project. As the backend is defined in the previous ADR to conitnue to use Django, the
Django-Rest-Framework will be use das often as possible to implement the REST interface.

The client shall not consume this API directly, instead the application utilizes the drf_spectactular package to offere an
OpenAPI/ Swagger interface to properly describe the behaviour of the offered endpoints. The client utilizes it as a generated
fetch API.

## Consequences

The fetch API of the used openapi-generator-tools package does not work well with server side rendering of Nuxt, as Nuxt uses
a kind of wrapper for this. The project currently does not feature many server side calls, so this consequency can be accepted.

The only server side call as of now consist out of `PageMeta`, which requires to get the meta tags server side for SEO optimization.
