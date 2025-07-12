# How to map?

## Introduction

The Distrochooser data model describes as follows:

- Translateable objects have a `catalogue_id` attribute, which is used in the translation as a search key
- A distribution is a `Choosable`, which can have multiple `ChoosableMeta` objects, which define a specified property of the entry.
- Each displayed page is a `Page` object
- Each page can have multiple `Widget` objects (which can also be inherited ones from `Widget`), which are aligned in a row/ col/ width structure
- For `SelectionWidgets`, they have a topic which is used to map the answers `Facettes`
- Each `Facette` should point to `FacetteAssignments`, which map a descriptive text in a defined way ("blocking", "negative", "neutral", "positive") to the selected answer (this is the decision part)
- A `Facette` can have `FacetteBehaviours`, which can be triggered when answers might exclude themselves. `FacetteBehaviours` are considered critical errors for conflicting answers and are being displayed in the UI. `FacetteBehaviour` are optional.
- Each selected answer is a `FacetteSelection` and is part of a `Session`

## Where does the decision matrix comes from?

The matrix is defined in the `/matrix/` folder. Basically everything is defined in TOML-files. The Id's of the elements are used as `catalogue_id` mentioned earlier and are used to reference objects.

**Important: If you introduce new mappings keep in mind that the translation requires updating as well!**

## Folder structure of /matrix/

|folder|description|
|--|--|
|assignments|The mapping itself to bind facettes to choosables|
|choosables|The distributions and it's meta information|
|facettes|Contains answers to map to questions, referred by a topic|
|pages|Contains defintion for each questionaire page, including it's structure, widgets etc.|
|version|Defines questionaire versions to hide certain pages from the use (e. g. to realize simplified questionaire editions)|


## Recommendations: Mapping strictness

In general, distributions should be "open towards generic". E. g. a distribution for beginners should receive positive mappings for answers like "I am a beginner", while mappings for "I am a professional" will either receive no or only neutral mappings. To keep translations and update effort as small as possible, neutral mappings should only be used if there is a informational benefit for the user to display this texts.


## Example: Update a distribution  mapping or introduce a new distribution

> You can create new choosable entries with the manage.py newchoosable <file_with_choosables.toml> --catalogue_id <id for the new distribution>

In this example, we want to add the mapping of the question `I want to game` of the distribution `Debian`.

Step 1: **Identify the desired distribution** in `choosable.toml` (it's defined as a `choosable`)

```
[...]
[[choosable]]
catalogue_id="debian" <-- This is the value you are looking for!
bg_color="#d70a53"
fg_color="white"
[...]
```
**You are introducing a new distribution?** You can also add meta blocks. This meta blocks have a type and a name, which is fixed. The meta blocks are **optional**, but help to improve the user expierience.

> The combination between type and name is fixed (it may be merged into one field at some point)

|Type|Name|Description|
|--|--|--|
|link|website|The website to the distributions homepage|
|flag|country|An country flag. The flags are displayed using https://github.com/lipis/flag-icons, so your language code should match  ISO `3166-1-alpha-2` as seen on https://www.iso.org/obp/ui/#search/code/.
|date|age|The starting date of the distribution project|

An complete distribution block can look like this and should be placed inside the `choosables.toml` files:

```
[[choosable]]
catalogue_id="debian"
bg_color="#d70a53"
fg_color="white"
[[choosable.meta]]
meta_type="link"
meta_name="website"
meta_value="https://debian.org"
[[choosable.meta]]
meta_type="date"
meta_name="age"
meta_value="1993-09-15"
[[choosable.meta]]
meta_type="flag"
meta_name="country"
meta_value="us"
```


Step 2: **Identify the question and facette**, it is defined in on of the toml files in the `facettes` folder. Each file represents the facettes for a question.

> In this example, the file `scenario.toml` is the wanted file. Within this file, you can find the desired facette. The identifier after `facette.` represents it's translation key, you can find these keys in the translation files aswell, if you want to search based on known translation strings.

```
[facette.gaming-usage] <-- This is the important key.
topic = "scenario" <-- This is the mapping to a question widget with the topic "scenario"
```

**You are adding a new distribution?** You will need to add mappings for all answer facettes, based on the distribution characteristics. For this, you can iterate the files from `facettes/`

Step 3: **Create the assignment**

- Locate the `assigments.toml` file (recommendation for new distributions: `Introduce new files, e. g. /assignments/my-distro.toml`)
- Find if the key of the facette is already present. Facettes are referred in this way: `from = ["<facette key>"]`. Keep in mind that facettes can have different directions, based on the attribute `how`.
- If no facette is existing, add your new facette to the file:

```
[assignment.my-matrix-addition] <-- this is an internal descriptor. Should be alphanumeric, can have hyphens
description = "my-matrix-addition" <-- This is the key for the translation
facettes = ["gaming-usage"] <-- This is the facette
choosables = ["debian"] <-- This is the choosable ID
how = "positive" <-- This is the mapping value (see below)
```

The value of `how` can be either:

> The defined weight on the `how` values might change at some point. The currently valid values can bee derived from `AssignmentType.get_score()`

- `positive` - Results in +1 point at calculation
- `negative` - Results in -1 point at calculation
- `neutral` - Results in 0 points at calculation (but will be added to the reasons, e. g. for informational purposes)
- `blocking` - Results in -100 points at calculation

**Added new files?** If you introduce a new TOML file, make sure you add this file into the include list inside the file `matrix.toml`: `#include <relativepath.toml>`. Make sure that following order is preserved: 1. `versions/` 2. `pages/` 3. `facettes/` 4. choosables/ 5. `assignments/`


Step 4: **Add translation values**

If your assingment(s) `description` fields are not already present within the translations, it must be added to them. It's recommeded to start with `en-<scope>.json` as the start point. E. g. if you introduced an assignment, add values into `facetteassignment-en.json`. Same applies for `facettes`, `choosables`, `pages` or UI changes (`ui-<lang>.json`).


> The mapping is already exhausting task. For this we will focus for the moment on having the translation complete in the `en.json` file, adding the translations for other languages at a secondary task, done by me or other focused contributors.

Step 5: **Test your changes**

Use the command `python manage.py parse /matrix/matrix.toml` to reimport everything.

The command `python manage.py annotate ../matrix/` adds comments to each file, showing relevant missing translations

Step 6: **All good? Commit them**

Definition of done in short:

1. Pull Request with changes in distrochooser: `/matrix/`
2. If required: Pull request with changes in translations: `*-en.json` files
3. Your PR should feature some descriptive text about your changes

Thank you!
