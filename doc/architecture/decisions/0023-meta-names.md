# 23. Meta-Names

Date: 2026-04-08

## Status

Accepted

## Context

Choosables have metas in defined categories, such as created (age), countries ("headquarter" location), website, supported languages and architectures. 

## Decision

The meta types are defined within `ChoosableMeta.MetaName`, while the names are defined in uppercase letters. During runtime, they might be referred by lowercase letters.

## Consequences

The "fixed" relation between e. g. "COUNTRIES" and "countries" might cause discrepancies in the code and shall be addressed in the future.
