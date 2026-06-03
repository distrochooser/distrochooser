# 27. Session model access

Date: 2026-06-03

## Status

Accepted

## Context

After import, the `Session` table consist out of more than 2 million rows of data. This causes significant delay on load time when `Session.objects.filter()`or `Session.objects.get()` is called.

## Decision

The access to `Session` instances is abstracted using the method `Session.get(result_id)`. This method searches for the session inside the cache and returns this data. If not cached, the object will be queried once and cached (even as all `Session` objects should be cached cached).

On `Session.save()`, the cache will be filled with the data, so in case of updates and partial updates, the session should remain up to date, not requiring altering the logic of the DRF viewsets.

## Consequences

All calls for `Session.objects.filter()`or `Session.objects.get()`  are not replaced by `Session.get(result_id)`. The statistics update does a `filter` once, but is cached anyways. At some point, it might cause issues with cache hits/ non hits, but they must be addressed separately.

On local environments, this action reduces the response times by about ~500ms (having 2300000 rows of sessions).
