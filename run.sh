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

# Execute the requested function
if [ $# -eq 0 ]; then
    echo "No command provided"
    exit 1
fi

# Execute the function passed as argument
"$@"
