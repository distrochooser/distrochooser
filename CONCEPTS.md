# Core concepts

## Folder structure

`/code/kuusi`  contains the backend, while `/code/frontend` contains the frontend.

## Concepts: Application

- The application uses Django Rest Framework to provide a RESTful API
- The Restful API is converted into a TypeScript SDK using a OpenAPI generator call 
- A Nuxt powered frontend consumes the API


## Concepts: Widgets

- Widgets can be ordered in a 12-Grid Layout
- The Navigation is not a Widget 8yet)

## Concepts: Internationalisation

- The application uses a JSON-based translation mechanism
- All localization files must reside inside on eof the folder defined in `LOCALE_PATHS`
- All localization files must follow the scheme `<name>-<code>.json`, where `<code>` is a 3166-1-alpha-2 code
- The hyphen is required and can only be part once in each file name
- The `<name>` part of the file does not serve a purpose rather than making it a bit easier to organize

### Translateable

Model instances might inherit the `Translateable` object. If inherited from this class, the inheriting class can use the `TranslateableField` field type, which is a char field. The `Translateable` class introduces a `catalogue_id`, which identifies the object.

E. g. if a class inheriting from `Translateable` has following attribute:

```
    description = TranslateableField(
        null=True, blank=True, default=None, max_length=120
    )
```

The JSON file will require following attributes:

```
    "<catalogue_id>-description": "This is my translation",
```

### Localization helpers

Some translations might not be related to an object referred as `Translatable`. 

In this case, the translations are added as-is in a JSON file:

```
    "BTN_MARK": "Mark this question",
```

To use this translation value, you can use the `_i18n_` helper function in `/code/kuusi/web/templatetags/web_extras.py`, e. g in a HTML template:

```
{% _i18n_ language_code "BTN_MARK" %}
```

> Additional localization helpers are defined in the `/code/kuusi/web/templatetags/web_extras.py` file.

## Concepts: Design

The frontend uses Bootstrap 5. The folder structure is bound to Nuxt's structure, but has roughly following shape:

- Widgets are located inside the `widgets` folder.
- Components should be as small as possible to allow reusing them
- Styling is done with SCSS


## Data model

A description of the data model can be found in the file `HOW-TO-MAP.md`.
