#!/bin/bash
# Build a suite's regression image and run it with docker compose
# to test a test suite's ASTRA integration locally.
#
# Usage:
#   test/      $ ./run_astra.sh hoss
#   test/hoss/ $ ../run_astra.sh
#
# Requires:
#   export HARMONY_HOST_URL=https://harmony.uat.earthdata.nasa.gov
#   export AWS_PROFILE=harmony-sandbox
#   export EDL_SECRETS_ROLE_ARN=<The IAM role ARN that ASTRA assumes to read EDL credentials from SSM>

set -euo pipefail

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)

suite=${1:-$(basename "$PWD")}
suite=${suite%/}

# verify you're running a suite
if [[ ! -f "${SCRIPT_DIR}/${suite}/version.txt" ]]; then
  echo "'${suite}' is not a test suite. Pass a suite name or run from a suite directory." >&2
  exit 1
fi

make -C "${SCRIPT_DIR}" "${suite}-image"

cleanup() {
  echo "Cleaning up"
  docker compose -p "${suite}" down
}
trap cleanup EXIT INT TERM

compose_template() {
  cat <<'YAML'
services:
  reporter:
    image: maven.earthdata.nasa.gov/etq/reporting-api:1
    attach: false
    healthcheck:
      test: ["CMD", "python3", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/v1/docs')"]
      interval: 2s
      timeout: 2s
      retries: 15
  test:
    image: ghcr.io/nasa/regression-tests-__SUITE__:latest
    depends_on:
      reporter:
        condition: service_healthy
    environment:
      ASTRA: "true"
      ETQ_REPORTING_URL: http://reporter:8000
      harmony_host_url: ${HARMONY_HOST_URL}
      EDL_USER: ${EDL_USER}
      EDL_PASSWORD: ${EDL_PASSWORD}
      EDL_SECRETS_ROLE_ARN: ${EDL_SECRETS_ROLE_ARN}
      AWS_PROFILE: ${AWS_PROFILE}
      AWS_REGION: ${AWS_REGION}
    volumes:
      - ../output:/workdir/output
      - ${HOME}/.aws:/root/.aws:ro
YAML
}

compose_template | sed "s/__SUITE__/${suite}/" | \
  docker compose --project-directory "${SCRIPT_DIR}/${suite}" -p "${suite}" -f - up
