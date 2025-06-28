# 11. Feedback

Date: 2025-06-28

## Status

Proposed

## Context

Users have opinions. They shall have the option to provide this feedback using

- Text feedback
- In App feedback

## Decision

The UI offers a "translation mode", where users can provide new translations in the UI directly.
The UI searches for these proposals and displays them for the proposing user only.

Administrative staff will still need to approve these changes.

For mappings, users can click on a `<>` icon, allowing to give thumbs up/ down for mappings. These mappings
require approval also.

All of these approvals are being carried out form the CLI only.

## Consequences

The user needs to be remembered, which conflicts with the projects "no tracking" policy.
