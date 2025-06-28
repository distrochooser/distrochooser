# 7. Used Icon sets

Date: 2025-06-28

## Status

Accepted

## Context

The application requires icons to look good and direct users on the UI.

## Decision

As the frontend already heavily relies on Nuxt.js, instead of attaching external frameworks and/or Icon fonts, the `@nuxt/icon` package is utilized.


## Consequences

The icons must be downloaded at build to avoid connecting to third party services at build.
