#!/bin/bash

## Compute a deterministic regression test image tag for a suite by combining
## service names from services_tested.txt with the deployed service versions
## from Harmony's /service-image-tag endpoint.

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

service_image_tag_url_for_host() {
  local harmony_host_url="$1"

  case "$harmony_host_url" in
    "https://harmony.uat.earthdata.nasa.gov")
      echo "https://harmony.uat.earthdata.nasa.gov/service-image-tag"
      ;;
    "https://harmony.earthdata.nasa.gov")
      echo "https://harmony.earthdata.nasa.gov/service-image-tag"
      ;;
    *)
      echo "Invalid HARMONY_HOST_URL '$harmony_host_url'. Valid values: https://harmony.uat.earthdata.nasa.gov, https://harmony.earthdata.nasa.gov" >&2
      return 1
      ;;
  esac
}

prefetch_service_image_tags() {
  local harmony_host_url="$1"
  local service_tag_url

  if [[ -n "${SERVICE_IMAGE_TAG_JSON:-}" ]]; then
    echo "Dynamic mode: using preloaded SERVICE_IMAGE_TAG_JSON (skipping /service-image-tag fetch)"
    return 0
  fi

  service_tag_url=$(service_image_tag_url_for_host "$harmony_host_url") || return 1

  if [[ -z "${HARMONY_TOKEN:-}" ]]; then
    echo "HARMONY_TOKEN must be set" >&2
    return 1
  fi

  SERVICE_IMAGE_TAG_JSON=$(curl --fail --silent --show-error \
    -H "Authorization: Bearer $HARMONY_TOKEN" \
    "$service_tag_url")

  if ! echo "$SERVICE_IMAGE_TAG_JSON" | jq -e . >/dev/null 2>&1; then
    echo "Unexpected response from $service_tag_url (not valid JSON)" >&2
    return 1
  fi

  export SERVICE_IMAGE_TAG_JSON
}

compute_regression_image_tag() {
  local suite_name="$1"
  local harmony_host_url="$2"
  local services_file="$SCRIPT_DIR/../test/$suite_name/services_tested.txt"
  local service_tag_url
  local service_tags_json
  local services_csv
  local computed_tag

  if [[ ! -f "$services_file" ]]; then
    echo "services_tested file not found: $services_file" >&2
    return 1
  fi

  service_tag_url=$(service_image_tag_url_for_host "$harmony_host_url") || return 1

  if ! command -v jq >/dev/null 2>&1; then
    echo "jq is required but not found in PATH" >&2
    return 1
  fi

  if [[ -z "${HARMONY_TOKEN:-}" ]]; then
    echo "HARMONY_TOKEN must be set" >&2
    return 1
  fi

  if [[ -n "${SERVICE_IMAGE_TAG_JSON:-}" ]]; then
    service_tags_json="$SERVICE_IMAGE_TAG_JSON"
  else
    service_tags_json=$(curl --fail --silent --show-error \
      -H "Authorization: Bearer $HARMONY_TOKEN" \
      "$service_tag_url")
  fi
  if ! echo "$service_tags_json" | jq -e . >/dev/null 2>&1; then
    echo "Unexpected response from $service_tag_url (not valid JSON)" >&2
    echo "Response starts with: $(echo "$service_tags_json" | head -c 120)" >&2
    return 1
  fi

  services_csv=$(tr -d '\n\r' < "$services_file")
  IFS=',' read -r -a raw_services <<< "$services_csv"

  parts=()
  for service in "${raw_services[@]}"; do
    service=$(echo "$service" | xargs)
    if [[ -z "$service" ]]; then
      continue
    fi

    version=$(echo "$service_tags_json" | jq -r --arg service "$service" '.[$service] // empty')
    if [[ -z "$version" ]]; then
      echo "No deployed version found for service '$service' at $service_tag_url" >&2
      return 1
    fi

    parts+=("${service}${version}")
  done

  if [[ ${#parts[@]} -eq 0 ]]; then
    echo "No services found in $services_file" >&2
    return 1
  fi

  computed_tag=$(IFS=_; echo "${parts[*]}")
  echo "$computed_tag"
}

## Returns the image name to use for a suite when dynamic mode is used.
## Computes the expected tag via compute_regression_image_tag and checks
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

usage() {
  cat <<'EOF'
Usage:
  compute-regression-image-tag.sh <suite-name> <environment>

Arguments:
  suite-name     Test suite directory under ./test (e.g. sambah)
  environment    One of: uat, prod

Environment:
  HARMONY_TOKEN  Bearer token used to call Harmony /service-image-tag

Examples:
  ./script/compute-regression-image-tag.sh sambah uat
EOF
}

main() {
  set -euo pipefail

  if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
    usage
    exit 0
  fi

  if [[ $# -ne 2 ]]; then
    usage
    exit 1
  fi

  local harmony_host_url
  case "$2" in
    uat)
      harmony_host_url="https://harmony.uat.earthdata.nasa.gov"
      ;;
    prod)
      harmony_host_url="https://harmony.earthdata.nasa.gov"
      ;;
    *)
      echo "Invalid environment '$2'. Valid values: uat, prod" >&2
      exit 1
      ;;
  esac

  compute_regression_image_tag "$1" "$harmony_host_url"
}

if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
  main "$@"
fi
