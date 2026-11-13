# 39. icons

Date: 2026-11-06

## Status

Accepted

## Context

Distrochooser is utilizing the `@nuxt/icon` module, which utilizes external CDN by default. The icons are loaded on demand from external sources.

## Decision

Icons shall be loaded only from *.distrochooser.de

## Consequences

Icons used int he Components are included on build with the `icon` configuration in `nuxt.config.ts` (`scan: true`).
For `Page` models, if using an icon, it must be adedd to the `icon.clientBundle.icons` array in `nuxt.config.ts`. Otherwise it won't load.
