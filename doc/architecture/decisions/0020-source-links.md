# 20. Source Links

Date: 2026-02-01

## Status

Accepted

## Context

To properly debug assignments to identify mapping errors, the assignments require an option to list it's primary sources.

## Decision


Mappings receive a ˙sources˙ array, which is a flat array containing one of following string structures:

`<distro_identifier>;<url>`

or

`<url>`

resulting in:

```
[assignment.some-id]
facettes = ["facette-id"]
choosables = [
    "Distro1",
    "Distro2"
]
how = "negative"
sources = [
    "Distro1;https://some-url.tld"
    "https://some-other-url.tld"
]
```

Sources prefixed with a distro ID only get displayed for the given distro while unprefixed sources get displayed for all choosables mapped to this assignment.

## Consequences

The project will now display external links more significantly, possibly requiring further GDPR-related features.