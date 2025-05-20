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

# Create install function that installs uv and ruff
function install() {
    python -m pip install --upgrade pip
    pip install uv==0.7.6
    uv pip install --system --editable "$THIS_DIR"
}

function lint() {
    pre-commit run --all-files
}

# Create build function that runs ruff check and format
function build() {
    uv build "$THIS_DIR"
}


function release:test() {
    lint
    build
    publish:test
}

function release:prod() {
    release:test
    publish:prod
}

function publish:test() {
    load_env
    uv publish --repository testpypi --username=__token__ --password=$TEST_PYPI_TOKEN
}

function publish:prod() {
    load_env
    uv publish --repository pypi --username=__token__ --password=$PYPI_TOKEN
}

# Execute the requested function
if [ $# -eq 0 ]; then
    echo "No command provided"
    exit 1
fi

# Execute the function passed as argument
"$@"
