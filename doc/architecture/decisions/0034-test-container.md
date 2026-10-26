# 34. Test container

Date: 2026-10-26

## Status

Accepted

## Context

Some users report on missing elements and a general "broken" expierience. It was known that during the first Nuxt.js version, adblocker were an issue. As distrochooser 6 and previous are already utilizing SSR, this should not persist. To investigate further, a test container is embedded to identify presence of DOM-altering extensions.

## Decision

With 36e7c51c283dd2b37c2ff9f4f9260dd53b227d2f, the backend received an statistic module, which will be enriched with this information (`TimeFrameRow.TimeFrameRowType.CTR_TEST).

## Consequences

There is a second request after initial session load, requiring to update the session a second time.

To access the statistical data, the web interface must be available again from the internet. Therefore, a `ADMIN_PREFIX` will be non-empty (empty if `DEBUG` is set), to mask the URL of the admin interface.

To generate/ update this data, `python3 manage.py v6_statistics` must be triggered externally. 