# Kuusi definition language

This definition language is a file-based frontend to allow versionized definition of a semi-complex decision matrix. It does not replace the admin UI, but can be used in automated processes.

## Basics

- Each statement is finalized with a ";"
- Comments are initialized with a "#" with a scope of the rest of the line
- Files can be splitted using `@include file.ku;` (the filename extension can be arbitary)
- Id's can be alphanumerical and can contain "-"
- Translations are handled in app as the entries are translated using gettext

## Apply

An *.ku file can be applied using `python3 manage.py parse <path-to-the-file>`. Old elements will be marked as `is_invalidated=True`, so these data can still be utilized, e. g. for old result display.

## Data Types

### Facette

An facette is a specific information which will be used to identify choosables. A facette can be child of another facettes, 
but there is no further nesting.

```
@facette <id> (topic <topic-id>);
```

Child facettes:

```
@facette <id> (topic <topic-id>) parent <parent-facette-id>;
```

### Facette Behaviour

A facette behaviour controls if a given facette selection will trigger a warning, info or error, e. g. when facettes are not meant to be selected together.

A behvaviour can feature a direction to allow narrow down certain situation better. The criticality and the direction have defaults and can be omitted if needed.

```
@facettebehaviour <id> (subject <facette-a-id> subject <facetteb-id> object <facette-c-id>) <criticality> <direction>;
```

Criticality is one of:
- `warning` - will trigger a warning in the result
- `info` - will trigger a info text in the result
- `error`- will cause the user to be informed while answering

Direction is one of
- `bidirectional`
- `subject_to_object`
- `object_to_subject`

Direction defaults to `bidirectional`, criticality to `info` if omitted.

### Choosable

A choosable is the entry which can be selected by the user's answers. A choosable can feature meta values, which are an unlimited list of key value pairs with certain types. 

```
@choosable <id> (meta_value1_type meta_value1_value meta_value1_content meta_value2_type meta_value2_value meta_value2_content);
```

Meta value type can be one of

- `link`
- `text`
- `date`
- `flag` (as in country-flag, ISO 639-1)

### Assignment

An assignment maps a set of facettes to a set of choosables with a certain weight. The weight controls if the mapping is a positive (0), negative (-1) or neutral (0) value.

```
@assignment <id> (<facette1_id> <facette2_id>) to <choosable1_id> to <choosable2_id> <type>;
```

Type can be one of

- `positive` 
- `Negative`
- `Neutral`