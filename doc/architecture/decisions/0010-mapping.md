# 10. Mapping

Date: 2025-06-28

## Status

Accepted

## Context

Past version had a database based mapping, not being published as open source.

The handling of these mapping is fiddly.

## Decision

The future mappings are to be released in the main repository.

The mapping consist out of several files, which are required to be parsed in a defined order to properly resolve dependencies:

```
# Parse order
# 1: Versions
# 2: Pages
# 3: Widgets
# 4: Choosables
# 5: Facettes
# 6: Assignments     
```

To prevent the parser from reading a large amount of files as a list, a central `toml` file will be utilized as an entry point,
utilizing a "hack" to include files, e. g.

`#include ./versions/simplified.toml`

Each file change must be imported into the database, on runtime, the decisions are being made solely based on the contents of the database.


## Consequences

The `#include ` call in the main toml file makes the TOML file not compilant with some TOML parsers.
The matrix is still large and hard to understand for new mappers.


The matrix content should configure the Distrochooser aspects, but not _think_ in it. For example, there is no `LinuxDistribution` like type. Instead, 
`Choosables` are being selected based on mappings towards defined `Facettes`. This might allow to use the codebase for similar projects outside of the 
Linux topic, aswell.
