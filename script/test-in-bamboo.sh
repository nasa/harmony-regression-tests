#!/bin/bash

## Script to download regression images and run the regression tests.

set -e

if [[ -z "${HARMONY_ENVIRONMENT}" ]]; then
  echo "HARMONY_ENVIRONMENT must be set to run this script"
  exit 1
fi

case $HARMONY_ENVIRONMENT in
uat)
  harmony_host_url="https://harmony.uat.earthdata.nasa.gov"
  ;;
prod)
  harmony_host_url="https://harmony.earthdata.nasa.gov"
  ;;
sit)
  harmony_host_url="https://harmony.sit.earthdata.nasa.gov"
  ;;
*)
  echo "Valid environments are sit, uat, and prod."
  exit 1
  ;;
esac

echo "harmony host url: ${harmony_host_url}"


## download test versions of the regression images from GitHub container registry.
## default images are pulled for each test in the all_tests array
## deault images are : "ghrc.io/nasa/regression-tests-<test>:latest"
## Any bamboo variables named "REGRESSION_TESTS_<test>_IMAGE" will override the default value.
image_names=()
container_repository="ghcr.io/nasa/"
all_tests=(harmony harmony-regression hoss hga n2z swath-projector trajectory-subsetter variable-subsetter regridder)

for image in "${all_tests[@]}"; do
    base="regression-tests-${image}"
    ENV_NAME=$(echo "${base}_IMAGE" | tr '[:lower:]' '[:upper:]' | tr '-' '_')
    default="${container_repository}${base}:latest"
    image_names+=("${!ENV_NAME:-${default}}")
done


/bin/rm -f pulled-docker-images.txt
for image in "${image_names[@]}"; do
    echo "Pulling image: ${image}"
    echo "${image}" >> pulled-images.txt
    docker pull "${image}"
done


cd test \
    && export HARMONY_HOST_URL="${HARMONY_HOST_URL}" \
	      AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY}" \
	      AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID}" \
	      EDL_USER="${EDL_USER}" \
	      EDL_PASSWORD="${EDL_PASSWORD}" \
    && ./run_notebooks.sh
