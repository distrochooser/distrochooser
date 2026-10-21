# 32. commit-messages

Date: 2026-10-21

## Status

Accepted

## Context

Commits message were not structured before.

The lack of a structure makes commits messy and possibly hard to follow.

## Decision

Orienting on the discussion on https://gist.github.com/joshbuchea/6f47e86d2510bce28f8e7f42ae84c716, the solution of https://gist.github.com/joshbuchea/6f47e86d2510bce28f8e7f42ae84c716?permalink_comment_id=5747564#gistcomment-5747564 is adopted, the Author agreed to consider this snippet as CC0-ish.

The prefixes of commit messages are limited to following options:

- feat:     A new feature.
- fix:      A bug fix. 
- docs:     Documentation changes.
- style:    Code style changes (formatting, missing semicolons, etc.).
- refactor: Code refactoring (neither fixes a bug nor adds a feature).
- chore:    Routine tasks like updating dependencies or build tools.

Following prefixes are **not** adopted (as of 3c4081e60fa872ef4ef4e7fd762f9fd079790bd7):

- test:     Adding or updating tests.
- build:    Changes affecting the build system or external dependencies.
- ci:       Changes to CI configuration files or scripts. 
- perf:     Performance improvements.

Reasons:

- The project does not have tests due to the fact this is a one-man project. Therefore `test:` has no purpose.
- The build pipeline is not part of the project build, ci. Changes to Dockerfiles, runscripts etc. are considered either `chore:`, `fix:` or `feat:`
- `perf:` is considered a nonfunctional requirement, therefore improvements are a `fix:`.

The commit message shall have the format. `<type>(<optional scope>): <description>`. More information will be included in `doc/COMMITS.md`.

## Consequences

Previous comments will not be altered.
