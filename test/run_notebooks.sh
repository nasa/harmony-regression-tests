#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
source "${SCRIPT_DIR}/../script/image_name.sh"
source "${SCRIPT_DIR}/../script/compute-regression-image-tag.sh"

usage() {
  cat <<'EOF'
Usage:
  ./test/run_notebooks.sh [options] [suite ...]

Options:
  --use-versions  Use per-suite version.txt tags (or suite IMAGE env var override)
  --dynamic       Compute expected regression image tag from services_tested.txt
                  and deployed Harmony service versions; use matching tagged
                  image when available, otherwise fall back to the suite's
                  version from test/<suite>/version.txt
  -h, --help      Show this help text

Environment:
  HARMONY_HOST_URL  Required. Set to the Harmony environment URL to run tests.

Arguments:
  suite           Optional suite names (e.g. sambah hga). If omitted, run all
                  suites listed in the environment config file.

Examples:
  ./test/run_notebooks.sh --dynamic sambah
EOF
}

for arg in "$@"; do
  case "$arg" in
    -h|--help)
      usage
      exit 0
      ;;
  esac
done

if [[ -z "${HARMONY_HOST_URL:-}" ]]; then
  echo "HARMONY_HOST_URL must be set to run this script" >&2
  exit 1
fi

## Returns the image name to use for a suite when --dynamic is set.
## Computes the expected tag via compute-regression-image-tag.sh and checks
## whether an image with that tag exists in the registry. Falls back to the
## suite's version file (test/<suite>/version.txt) if no matching image is
## found.
function dynamic_image_name () {
    local suite="$1"
    local harmony_host_url="$2"
    local base="ghcr.io/nasa/regression-tests-${suite}"

    local computed_tag
    if ! computed_tag=$(compute_regression_image_tag "$suite" "$harmony_host_url"); then
      return 1
    fi

    if [[ -n "$computed_tag" ]] && \
       docker manifest inspect "${base}:${computed_tag}" >/dev/null 2>&1; then
        echo "${base}:${computed_tag}"
    else
        if [[ -n "$computed_tag" ]]; then
          echo "No image found for tag '${computed_tag}', falling back to version in ${SCRIPT_DIR}/../test/${suite}/version.txt" >&2
          echo "You can add the tag to the desired image version by running './script/add-ghcr-tag.sh ${base}:<version> ${computed_tag}'" >&2
        else
          echo "Could not compute image tag for '${suite}', falling back to version in ${SCRIPT_DIR}/../test/${suite}/version.txt" >&2
        fi
        echo "${base}:$(<"${SCRIPT_DIR}/../test/${suite}/version.txt")"
    fi
}

echo -e "\nRunning regression tests"
echo -e "Using ${HARMONY_HOST_URL}\n"


# Specify the test images to run. By default, run all suites listed in the
# selected configuration file. If the script is invoked with a list of suites,
# only run those.

# Choose the correct configuration file.
case $HARMONY_HOST_URL in
"https://harmony.earthdata.nasa.gov")
  configuration_file="${SCRIPT_DIR}/../config/services_tests_config_prod.json"
  ;;
*)
  configuration_file="${SCRIPT_DIR}/../config/services_tests_config_uat.json"
  ;;
esac

# Retrieve all tests to be run from "all" in the appropriate configuration file
IFS=","
read -ra all_images <<< "$(jq -r '.all' ${configuration_file})"
unset IFS

specified_images=()
# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
    -h|--help)
      usage
      exit 0
      ;;
        --use-versions)
            use_versions=true
            shift
            ;;
        --dynamic)
            dynamic=true
            shift
            ;;
        *)
            specified_images+=("$1")
            shift
            ;;
    esac
done

## use the user supplied images or the default list of all images.
images=("${specified_images[@]:-${all_images[@]}}")

# Select images using the dynamic tag lookup when requested; otherwise use the
# standard image naming rules from image_name.sh.
if [[ "${dynamic:-false}" == true ]]; then
  echo "Dynamic mode: fetching /service-image-tag once and reusing it for all suites"
  if ! prefetch_service_image_tags "$HARMONY_HOST_URL"; then
    echo "Failed to fetch /service-image-tag from ${HARMONY_HOST_URL}" >&2
    exit 1
  fi
fi

# launch all the docker containers and store their process IDs
for image in "${images[@]}"; do
    echo -e "Test suite ${image} starting"

    if [[ "${dynamic:-false}" == true ]]; then
      if ! full_image=$(dynamic_image_name "$image" "$HARMONY_HOST_URL"); then
        echo "Failed to determine image for ${image}" >&2
        exit 1
      fi
    else
      full_image=$(image_name "$image" "$use_versions")
    fi
    echo "running test with $full_image"
    # PIDS+=(${image},$(docker run -d -v ${PWD}/output:/workdir/output \
    #           --env EDL_PASSWORD="${EDL_PASSWORD}" --env EDL_USER="${EDL_USER}" \
    #           --env harmony_host_url="${HARMONY_HOST_URL}" "${full_image}"))
done

trap ctrl_c SIGINT SIGTERM

function ctrl_c() {
  echo "Cleaning up"
  for name_comma_pid in "${PIDS[@]}"; do
    name_pid=(${name_comma_pid//,/ })
    echo "Killing ${name_pid[0]}"
    docker kill "${name_pid[1]}" >/dev/null
    docker rm "${name_pid[1]}" >/dev/null
  done
  echo "Exiting"
  exit 1
}

exit_code=0
# wait for processes to finish and store each exit code into array STATUS'
for name_comma_pid in "${PIDS[@]}"; do
  name_pid=(${name_comma_pid//,/ })
  name=${name_pid[0]}
  pid=${name_pid[1]}

  echo "Waiting for ${name}."
  docker logs --follow "${pid}"
  code=$(docker container wait ${pid})

  if [[ ${code} -ne 0 ]]; then
    echo -e "${RED}Test suite ${name} failed with exit code ${code}${NC}" 1>&2;
    exit_code=1
  else
    echo -e "${GREEN}Test suite ${name} succeeded${NC}"
  fi
  docker rm ${pid} >/dev/null
done

if [[ ${exit_code} -ne 0 ]]; then
  echo "Tests completed (failed)"
else
  echo "Tests completed (passed)"
fi

exit ${exit_code}
