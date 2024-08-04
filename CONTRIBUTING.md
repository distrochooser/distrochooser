# Contributing to the distrochooser project

Thank you for your interest in contributing to the distrochooser project 🎉!

# General

Distrochooser has a very slow development cycle as this is a "weekend warrior" project. This means that issues might be unanswered for months before being picked up. But don't worry, they will be discussed, but just not that fast as in large projects. 

Please note that there will no discussions with deleted accounts (on PR/ Issues/ Discussions). These threads will be closed.

# Preparations

Following documents are important for any contribution in the distrochooser repository

👉 [Code of conduct](https://github.com/distrochooser/distrochooser/blob/master/CODE_OF_CONDUCT.md)

👉 [License](https://github.com/distrochooser/distrochooser/blob/master/LICENSE)

# Contributing to the code 💻

This version of distrochooser consists out of a single monolith, based in Django 4.x.

# Contributing to the decision matrix ✅

The Distrochooser data model describes as follows:

- Translateable objects have a `catalogue_id` attribute, which is used in the translation as a search key
- A distribution is a `Choosable`, which can have multiple `ChoosableMeta` objects, which define a specified property of the entry.
- Each displayed page is a `Page` object, which is related to one `Category` object, which controls the navigation
- Each page can have multiple `Widget` objects (which can also be inherited ones from `Widget`), which are aligned in a row/ col/ width structure
- For `SelectionWidgets`, they have a topic which is used to map the answers `Facettes`
- Each `Facette` should point to `FacetteAssignments`, which map a descriptive text in a defined way ("blocking", "negative", "neutral", "positive") to the selected answer (this is the decision part)
- A `Facette` can have `FacetteBehaviours`, which can be triggered when answers might exclude themselves. `FacetteBehaviours` have a severity from warning to critical to be displayed in the UI. `FacetteBehaviour` are optional.
- Each selected answer is a `FacetteSelection` and is part of a `Session`

The matrix is defined in the /doc/matrix folder. Basically everything is defined in TOML-files.

**Important** If you introduce new mappings keep in mind that the translation requires updating as well!

# Contributing translations 🌍

https://github.com/distrochooser/translations is your starting point for translations. You can either use the Weblate instance (details in the Readme) or use a PR.

For PR users:

You can find the file `en.po` in the repository https://github.com/distrochooser/translations. For this Distrochooser version, a JSON-based format is used. Each area of translation is suffixed by an [ISO-639-1](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) language code, for example if you want to create a greek translation, use the filename `ui-gr.po`.

The english translation is the leading translation.

## How to submit the translation? 📮

You can either do a pull request into the `distrochooser/translations:main` branch or, if you don't have a GitHub account, send it via mail to `mail@chmr.eu`. Alternatively, you can use https://translate.distrochooser.de


Thank you for your support 😁

