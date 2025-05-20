set -ex

THIS_DIR=$(cd "$(dirname "$0")" && pwd)

# Create install function that installs uv and ruff
function install() {
    python -m pip install --upgrade pip
    pip install uv
    uv pip install --editable "$THIS_DIR"
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
    load_dotenv
    uv publish --repository testpypi
    --username=__token__
    --password=$TEST_PYPI_TOKEN
}

function publish:prod() {
    load_dotenv
    uv publish --repository pypi
    --username=__token__
    --password=$PYPI_TOKEN
}
