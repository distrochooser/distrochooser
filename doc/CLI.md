# Distrochooser CLI tooling

Distrochooser offers CLI tools to parse decision trees and process user feedback.

## parse: Import mappings from TOML

`python3 manage.py parse path/to/matrix.toml [--wipe]`

The `--wipe` parameter removes all existing data from the database. Use with caution!

## language: Process language feedback

To remove selected feedback, the `--delete` parameter can be used. If no parameters are given, existing feedback will be printed out.

Using `--clear`, all feedback can be deleted. Using `--persist`, feedback will be stored into the json files from the **FIRST** defined locale path from `settings.py`. If no JSON update is desired, but proposals should be used, the command `--approve` should be used.

Examples:

`python3 manage.py languagefeedback --delete <id1> <idn>`

`python3 manage.py languagefeedback --approve <id1> <idn>`

`python3 manage.py languagefeedback --persist <id1> <idn>`

`python3 manage.py languagefeedback --clear`

## feedback: 

Examples:

Feedback has two stages: A _pending_ feedback is a proposal for a new mapping between an `assignment` and a `choosable`. If these are approved, the `assignment` mapping will be extended correspondingly.

A non-pending _feedback_ is a feedback on top of an existing mapping between `choosable` and `assignment`. This feedback currently only has informational character.

If no parameters to `matrixfeedback` are given, all existing items will be printed out.

`python3 manage.py matrixfeedback --delete <id1> <idn>`

`python3 manage.py matrixfeedback --approve <id1> <idn>`