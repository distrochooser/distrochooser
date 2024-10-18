# Core concepts

This project is a Django applicaiton and utilizes some of Django's features.

## Concepts: Application

- Views are rendered server-sided
- The use of JavaScript is as small as possible

## Concepts: Layout

- The application has only one layout
- Inside the layout a `Page` is displayed
- The `Page` contains `Widgets`, which are located in an 12-column grid layout, each Widget has a fixed width
- The navigation is linear. Each page features a `next_page` property
- The navigation is derived from the `next_page` of the available `Page` objects as a kind of chain

## Concepts: Widgets

Widgets are the contents of `Page` objects. All widgets overwrite the `proceed` and `render` functions of the `Widget` base class. If `proceed` returns false, the use will be held on the page, unless the uses forces a navigation.

An navigation can be forced if the post value `BTN_FORCED_NAVIGATION` is present.

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

The frontend uses Bootstrap 5.

The templates are located in the `/code/kuusi/web/templates` folder. There is the base layout file `_layout.html`, which defines the base page structure.

Templates related to `Widget` classes are located in the folder `/code/kuusi/web/templates/widgets`, while templates used in template tags from `web_extras.py` are located in `/code/kuusi/web/template/tags`.

SCSS components are located in the folder `/design`. The files are split based on a purpose.

If additional class names are being introduced, the class prefix `ku-` should be used, e. g. in file `/design/scss/logo.scss`:

```
.ku-logo {
    width: 250px;
    margin-bottom: 1em;
}
```

The SCSS files are embedded in a `/design/scss/custom.scss` file, which brings the Bootstrap 5 and Distrochooser theme parts together.

To get these file compiled/ picked up by the webserver, the script `build-styles` is available inside the `/design/package.json`. Important: **Please execute this scripts from the folder `/design`, as the `build-styles` script uses relative paths.**

## Data model

A description of the data model can be found in the file `HOW-TO-MAP.md`.

