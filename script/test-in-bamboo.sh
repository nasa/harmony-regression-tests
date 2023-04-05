#!/bin/bash

## Script to download regression images and run the regression tests.
## Intended to be run as part of Continuous Integration in Bamboo.

set -ex

## Returns the correct image name to pull from docker.  If the test name's
## environmental variable exists, return that, otherwise return the default
## value for the image.
function image_name () {
    base="regression-tests-$1"
    env_image_name=$(echo "${base}_IMAGE" | tr '[:lower:]' '[:upper:]' | tr '-' '_')
    default_image="ghcr.io/nasa/${base}:latest"
    echo "${!env_image_name:-${default_image}}"
}

if [[ -z "${HARMONY_ENVIRONMENT}" ]]; then
  echo "HARMONY_ENVIRONMENT must be set to run this script"
  exit 1
fi

# choose the correct harmony host.
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


## Download test versions of the regression images from GitHub container registry.
## Images are pulled for each test in the all_tests array
## default images have a pattern: "ghrc.io/nasa/regression-tests-<test>:latest"
## Any bamboo variables named "REGRESSION_TESTS_<test>_IMAGE" will override the default value.
## e.g. if REGRESSION_TESTS_N2Z_IMAGE environment was set, the value would be used instead of the default.

image_names=()
all_tests=(harmony harmony-regression hoss hga n2z swath-projector trajectory-subsetter variable-subsetter regridder)
for image in "${all_tests[@]}"; do
    image_names+=($(image_name "$image"))
done

# download all of the images and output their names
/bin/rm -f pulled-docker-images.txt
for image in "${image_names[@]}"; do
    echo "Pulling image: ${image}"
    echo "${image}" >> pulled-images.txt
    docker pull "${image}"
done

## run the tests
cd test \
    && export HARMONY_HOST_URL="${harmony_host_url}" \
	      AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY}" \
	      AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID}" \
	      EDL_USER="${EDL_USER}" \
	      EDL_PASSWORD="${EDL_PASSWORD}" \
    && ./run_notebooks.sh

# Copy the notebook artefacts up to S3:
if [[ -z "${REGRESSION_TEST_OUTPUT_BUCKET}" ]]; then
  aws s3 cp output "s3://${REGRESSION_TEST_OUTPUT_BUCKET}" --recursive
fi
