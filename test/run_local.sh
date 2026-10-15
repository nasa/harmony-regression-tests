#!/bin/bash
# Run one regression suite with papermill against a local
# Harmony (Harmony-in-a-Box) using the currently activated environment.
#
# Usage (activate the suite's env first, e.g. `conda activate papermill-hoss`):
# from the test/ directory you can run
#   test/      $ ./run_local.sh hoss
# from the suite's directory:
#   test/hoss/ $ ../run_local.sh
#
# Output goes to test/output/<suite>/Results.ipynb, same as run_notebooks.sh.
# EDL auth comes from your existing NETRC / ~/.netrc.

set -euo pipefail

# we could change this later but leave it as local only for now.
HARMONY_HOST_URL=http://localhost:3000

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)

suite=${1:-$(basename "$PWD")}
suite=${suite%/}

# verify you're running a suite
if [[ ! -f "${SCRIPT_DIR}/${suite}/version.txt" ]]; then
  echo "'${suite}' is not a test suite. Pass a suite name or run from a suite directory." >&2
  exit 1
fi

# The Makefile is the source of truth for each suite's notebook name.
notebook=$(grep -oE "notebook=[^ ]+ --build-arg sub_dir=${suite}( |$)" "${SCRIPT_DIR}/Makefile" \
  | head -1 | sed -E 's/notebook=([^ ]+) .*/\1/' || true)
if [[ -z "${notebook}" ]]; then
  echo "Could not find the notebook for '${suite}' in ${SCRIPT_DIR}/Makefile" >&2
  exit 1
fi

command -v papermill >/dev/null || {
  echo "papermill not found; activate the env for ${suite} first." >&2
  exit 1
}

output_dir="${SCRIPT_DIR}/output/${suite}"
mkdir -p "${output_dir}"

echo "Running ${suite}/${notebook} against ${HARMONY_HOST_URL}"
echo "Output: ${output_dir}/Results.ipynb"

papermill --cwd "${SCRIPT_DIR}/${suite}" \
  "${SCRIPT_DIR}/${suite}/${notebook}" \
  "${output_dir}/Results.ipynb" \
  -p harmony_host_url "${HARMONY_HOST_URL}" \
  -k python3

echo "Test suite ${suite} succeeded"
