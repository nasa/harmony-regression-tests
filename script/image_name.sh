#!/bin/bash

## Returns the correct image name to run a notebook.
## If the test name's environmental variable exists, return that.
## otherwise:
##   if the second argument passed is 'true' return the tag value for the image read from the version.txt file.
##   else returns 'latest'
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

function image_name () {
    base="regression-tests-$1"
    if [ "$2" = true ]; then
        recent_tag=$(<"$SCRIPT_DIR/../test/$1/version.txt")
    else
        recent_tag="latest"
    fi
    env_image_name=$(echo "${base}_IMAGE" | tr '[:lower:]' '[:upper:]' | tr '-' '_')
    default_image="ghcr.io/nasa/${base}:${recent_tag}"
    echo "${!env_image_name:-${default_image}}"
}
