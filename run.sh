set -ex

THIS_DIR=$(cd "$(dirname "$0")" && pwd)

# Load environment variables from .env file if it exists
function load_env() {
    if [ -f "$THIS_DIR/.env" ]; then
        set -a
        source "$THIS_DIR/.env"
        set +a
    fi
}

# Create install function that installs uv and dependencies
function install() {
    python -m pip install --upgrade pip
    pip install uv
    uv pip install --system --editable "$THIS_DIR"
}

function lint_and_format() {
    pre-commit run --files '*.py'
}

function lint_and_format:ci() {
    SKIP=no-commit-to-branch pre-commit run --files '*.py'
}

function build() {
    uv build "$THIS_DIR"
}

function release:test() {
    lint_and_format
    build
    publish:test
}

function release:prod() {
    release:test
    publish:prod
}

function publish:test() {
    load_env
    uv publish --index testpypi --username=__token__ --password=$TEST_PYPI_TOKEN
}

function publish:prod() {
    load_env
    uv publish --index pypi --username=__token__ --password=$PYPI_TOKEN
}

function tag_release() {
    load_env
    VERSION=$(cat "$THIS_DIR/version.txt")
    git tag "v$VERSION"
}

function bump_version() {
    load_env
    CURRENT_VERSION=$(cat "$THIS_DIR/version.txt")

    # Parse version components
    IFS='.' read -r -a version_parts <<< "$CURRENT_VERSION"
    MAJOR=${version_parts[0]}
    MINOR=${version_parts[1]}
    PATCH=${version_parts[2]}

    # Increment patch version
    NEW_PATCH=$((PATCH + 1))
    NEW_VERSION="$MAJOR.$MINOR.$NEW_PATCH"

    # Update version.txt
    echo "$NEW_VERSION" > "$THIS_DIR/version.txt"
}

# Execute the requested function
if [ $# -eq 0 ]; then
    echo "No command provided"
    exit 1
fi

# Execute the function passed as argument
"$@"
