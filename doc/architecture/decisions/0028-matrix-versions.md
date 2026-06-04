# 28. matrix versions

Date: 2026-06-04

## Status

Accepted

## Context

The app is constantly changing, causing results to change and evolve over time even after the user has requested the initial result. Therefore there is the need to identify if the session results derive from a "latest" configuration or not.

## Decision

`Session` objects receive the Git hash on save. The hash is derived from the setting `GIT_HASH_PATH`, which will be filled externally (on Docker image build). The hash from `GIT_HASH_PATH` is loaded into the environment variable `GIT_HASH`.

## Consequences

The UI might display some kind of remark at some point.
