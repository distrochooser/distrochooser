# Commit structure

As introduced with the decision of ADR-0032, the project starts to use semantic commit messages.

https://gist.github.com/joshbuchea/6f47e86d2510bce28f8e7f42ae84c716?permalink_comment_id=5747564#gistcomment-5747564

To prevent commits from not having this structure, following git hook can be used (e. g. dropped in `.git/hooks/commitmsg`, needs `chmod +x` to work):

```
#!/usr/bin/env bash

# Path to the commit message file (provided by Git).
COMMIT_MSG_FILE=$1

# Ignore automatic commit messages containing ' into ' or 'Merge'.
if grep --quiet --extended-regexp " into |^Merge " "$COMMIT_MSG_FILE"; then
    exit 0
fi

# Read the commit message from the file.
COMMIT_MSG=$(cat "$COMMIT_MSG_FILE")

CONVENTIONAL_COMMIT_REGEX='^(feat|fix|docs|style|refactor|test|chore|build|ci|perf|revert)(\([a-zA-Z0-9_.-]+\))?(!)?:\s.*$'

# Check if the commit message matches the regex.
if ! [[ $COMMIT_MSG =~ $CONVENTIONAL_COMMIT_REGEX ]]; then
    echo "ERROR: Commit message does not follow Conventional Commits format."
    echo
    echo "The commit message should be structured as follows:"
    echo "<type>(<optional scope>): <description>"
    echo "[optional body]"
    echo "[optional footer(s)]"
    echo
    echo "Valid types are:"
    echo "  feat:     A new feature."
    echo "  fix:      A bug fix."
    echo "  docs:     Documentation changes."
    echo "  style:    Code style changes (formatting, missing semicolons, etc.)."
    echo "  refactor: Code refactoring (neither fixes a bug nor adds a feature)."
    echo "  test:     Adding or updating tests."
    echo "  chore:    Routine tasks like updating dependencies or build tools."
    echo "  build:    Changes affecting the build system or external dependencies."
    echo "  ci:       Changes to CI configuration files or scripts."
    echo "  perf:     Performance improvements."
    echo "  revert:   Reverting a previous commit."
    echo
    echo "Examples:"
    echo "  feat(auth): add login functionality"
    echo "  fix(api)!: resolve timeout issue"
    echo "  docs(readme): update installation instructions"
    echo
    exit 1
fi

exit 0
```