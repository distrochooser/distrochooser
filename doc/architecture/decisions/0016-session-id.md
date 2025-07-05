# 16. Session ID

Date: 2025-07-05

## Status

Accepted

## Context

Each session has a session id (internally called `result_id`) which identifies a given session. In the past, it was generated randomly, but
was recently moved to UUID. The random approach required to have to iterate all results to find if the random ID was already taken, increasing
the initial load time.

The UUID is *very* long, mostly longer than the entire URL. This decision isnow rolled back. 


## Decision

The new session id consist out of two numbers, the current unix time and a random component, encoded using the `Sqids` library.
This generates a significantly shorter result id.

The database field was not altered to avoid breaking UUID-using results.

## Consequences

This increases the danger of collisions, but based on the expected user traffic this should be acceptible.
