#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

## Import function that returns correct image names.  if flag --use-versions is
## set when this script is called, it will use names form versions.txt
## otherwise it will default to "latest"
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
source "${SCRIPT_DIR}/../script/image_name.sh"

echo -e "\nRunning regression tests"
echo -e "Using ${HARMONY_HOST_URL}\n"


# Specify the test images to run, by default all built by the Makefile. If
# the script is invoked with a list of images, only run those.
all_images=(
    filtering
    geoloco
    harmony
    harmony-regression
    hga
    hoss
    hybig
    net2cog
    nsidc-icesat2
    opera-rtc-s1-browse
    regridder
    sambah
    smap-l2-gridder
    subset-band-name
    swath-projector
    trajectory-subsetter
    variable-subsetter
)
specified_images=()
# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        --use-versions)
            use_versions=true
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

# launch all the docker containers and store their process IDs
for image in "${images[@]}"; do
    echo -e "Test suite ${image} starting"

    full_image=$(image_name "$image" "$use_versions")
    echo "running test with $full_image"
    PIDS+=(${image},$(docker run -d -v ${PWD}/output:/workdir/output \
                      --env EDL_PASSWORD="${EDL_PASSWORD}" --env EDL_USER="${EDL_USER}" \
                      --env harmony_host_url="${HARMONY_HOST_URL}" "${full_image}"))
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
