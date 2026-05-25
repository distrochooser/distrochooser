# 26. Release of version 6

Date: 2026-05-25

## Status

Accepted

## Context

Currently, there are two instances

- distrochooser.de -> `v5`
- beta.distrochooser.de -> `v6`

`v6` shall soon replace the `v5` instance.

### Option 1: Bridge (used in the past)

`v5` moves to old.distrochooser.de, `v6` moves to distrochooser.de, beta.distrochooser.de is retired

Pro/ Con:

- 🙂 Easy to carry out
- 🙁 Requires old version to remain online
- 🙁 Requires new version to display hint for "old" results to forward to the old version
- 🙁 When the `v5` is shut down finally, the old results are lost

### Option 2: Migrate data

`v6` moves to distrochooser.de, beta.distrochooser.de is retired

Selected data from `v5` is migrated into `v6`database:

> Idea here:
> The bare minimum shall be migrated: The sessions and the given answers. The given answers are mapped to the catalogue id's in the new distrochooser version, allowing carrying over of the user input.
> Importance - Flags (previously boolean) will be reflected as score "0" (not important) and "2" important to utilize the 
> scoring via WEIGHT_MAP in settings.py
 
- Sessions (Date, Id, User-Agent, Referrer, Language)
- GivenAnswer (Session, Answer, Importance)

Other information, such as page structure, feedback, etc. will NOT be migrated to keep the import compact.

Pro/ Con:

- 🙂 "Clean" approach, no bridge needed
- 🙂 Historic data remains accessible (limited)
- 🙁 Requires large migration effort (2400000 + 16000000 rows as of 25.05.2026)
- 🙁 Requires new version to display alert
- 🙁 Requires database update to flag migrated data

## Decision

Both options require some additions to the frontend. In the past, only #1 was carried out. For the `v5` to `v6` switch, **option #2** is attempted to allow a seamless transistion between the versions.

For fallback purposes, `v5` will be kept as old.distrochooser.de for a limited time, most likely until the end of the year (assuming the switch is carried out in summer of 2026).

The import shall be carried out in following stages

- Export of the Django models `distrochooser.UserSession` and `distrochooser.GivenAnswer` in separate(!) runs using the `dumpdata` command (`--format json -o file.json`). A possible downtime might be considered.
- The files will be tested in a local test environment.
- The import will be carried out using the `import` management command

The domain configuration shall be adapted to reflect the switches:

- `v5` moves to old.distrochooser.de
- `v6` moves to distrochooser.de
- beta.distrochooser will be shut down

## Consequences

Due to the data amount to be migrated, some time planning must be carried out to refine the `import <session.json> <givenanswer.json>` management command introduced in #13ca236b1f749b39d322fe777b2feb3b0a75a251. As of time of writing, the import might take > 100h, improvements pending.

The frontend need to reflect the change in the relase option, displaying a remark in case a migrated result is opened. This also applies for the cloning process, so a cloned result also retains that flag.