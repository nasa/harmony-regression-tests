#!/bin/bash

set -euo pipefail

# Usage:
# ./add-ghcr-tag.sh <source-image> <new-tag>
#
# Example:
# ./add-ghcr-tag.sh ghcr.io/nasa/regression-tests-casper:1.1.1 hoss1.2.6_maskfill1.3.3
#
# Behavior:
#
# Add the new-tag to source-image if the source version is "latest" or 
# if the source version is a semantic version that is greater than the current version 
# associated with new-tag or the new-tag is not currently associated with any version.

SOURCE_IMAGE="$1"
NEW_TAG="$2"

# Extract image name without tag
IMAGE_NAME="${SOURCE_IMAGE%%:*}"
SOURCE_VERSION="${SOURCE_IMAGE##*:}"

TARGET_IMAGE="${IMAGE_NAME}:${NEW_TAG}"

echo "Source image: $SOURCE_IMAGE"
echo "New image tag: $TARGET_IMAGE"

# Extract GHCR owner and package name.
#
# ghcr.io/nasa/regression-tests-casper
#          ^^^^ ^^^^^^^^^^^^^^^^^^^^^^^
#          owner package
GHCR_PATH="${IMAGE_NAME#ghcr.io/}"
OWNER="${GHCR_PATH%%/*}"
PACKAGE_NAME="${GHCR_PATH#*/}"

# Authenticate to GHCR (expects GHCR_TOKEN and GHCR_USERNAME env vars)
if [[ -z "${GHCR_TOKEN:-}" ]]; then
  echo "Error: GHCR_TOKEN environment variable not set"
  exit 1
fi

if [[ -z "${GHCR_USERNAME:-}" ]]; then
  echo "Error: GHCR_USERNAME environment variable not set"
  exit 1
fi

# Semantic-version helpers
is_semver() {
  local version="${1#v}"

  [[ "$version" =~ ^[0-9]+\.[0-9]+\.[0-9]+(-[0-9A-Za-z.-]+)?(\+[0-9A-Za-z.-]+)?$ ]]
}

# Return:
#   0 => $1 > $2
#   1 => $1 <= $2
semver_gt() {
  local a="${1#v}"
  local b="${2#v}"

  # Build metadata does not affect SemVer precedence.
  a="${a%%+*}"
  b="${b%%+*}"

  local a_core="${a%%-*}"
  local b_core="${b%%-*}"

  local a_pre=""
  local b_pre=""

  if [[ "$a" == *-* ]]; then
    a_pre="${a#*-}"
  fi

  if [[ "$b" == *-* ]]; then
    b_pre="${b#*-}"
  fi

  local a_major a_minor a_patch
  local b_major b_minor b_patch

  IFS='.' read -r a_major a_minor a_patch <<< "$a_core"
  IFS='.' read -r b_major b_minor b_patch <<< "$b_core"

  if (( 10#$a_major > 10#$b_major )); then return 0; fi
  if (( 10#$a_major < 10#$b_major )); then return 1; fi

  if (( 10#$a_minor > 10#$b_minor )); then return 0; fi
  if (( 10#$a_minor < 10#$b_minor )); then return 1; fi

  if (( 10#$a_patch > 10#$b_patch )); then return 0; fi
  if (( 10#$a_patch < 10#$b_patch )); then return 1; fi

  # Release version has higher precedence than a prerelease.
  # Example:
  #   2.0.0 > 2.0.0-rc.1
  if [[ -z "$a_pre" && -n "$b_pre" ]]; then
    return 0
  fi

  if [[ -n "$a_pre" && -z "$b_pre" ]]; then
    return 1
  fi

  if [[ -z "$a_pre" && -z "$b_pre" ]]; then
    return 1
  fi

  local -a a_parts
  local -a b_parts

  IFS='.' read -ra a_parts <<< "$a_pre"
  IFS='.' read -ra b_parts <<< "$b_pre"

  local i
  local max="${#a_parts[@]}"

  if (( ${#b_parts[@]} > max )); then
    max="${#b_parts[@]}"
  fi

  for ((i = 0; i < max; i++)); do
    if (( i >= ${#a_parts[@]} )); then
      return 1
    fi

    if (( i >= ${#b_parts[@]} )); then
      return 0
    fi

    local ai="${a_parts[$i]}"
    local bi="${b_parts[$i]}"

    [[ "$ai" == "$bi" ]] && continue

    if [[ "$ai" =~ ^[0-9]+$ && "$bi" =~ ^[0-9]+$ ]]; then
      if (( 10#$ai > 10#$bi )); then
        return 0
      else
        return 1
      fi
    fi

    # Numeric prerelease identifiers have lower precedence than non-numeric.
    if [[ "$ai" =~ ^[0-9]+$ ]]; then
      return 1
    fi

    if [[ "$bi" =~ ^[0-9]+$ ]]; then
      return 0
    fi

    if [[ "$ai" > "$bi" ]]; then
      return 0
    else
      return 1
    fi
  done

  return 1
}


echo "$GHCR_TOKEN" | docker login ghcr.io -u "${GHCR_USERNAME:-}" --password-stdin

if [[ "$SOURCE_VERSION" == "latest" ]]; then
  echo "Source version is 'latest'. Skipping semantic version comparison."

  # Copy the manifest directly in the registry without pulling any layers.
  # This preserves the original multi-platform manifest list and avoids
  # platform-mismatch errors when running on a different architecture.
  docker buildx imagetools create -t "$TARGET_IMAGE" "$SOURCE_IMAGE"

  echo "Done! '$NEW_TAG' now points to '$SOURCE_IMAGE'."
  exit 0
fi

if ! is_semver "$SOURCE_VERSION"; then
  echo "Error: source image tag '$SOURCE_VERSION' is neither 'latest' nor a semantic version"
  exit 1
fi

echo "Checking whether '$NEW_TAG' already exists..."
CURRENT_VERSION=""
TAG_FOUND=false
PAGE=1

while true; do
  RESPONSE="$(
    curl --silent --show-error --fail \
      -H "Accept: application/vnd.github+json" \
      -H "Authorization: Bearer $GHCR_TOKEN" \
      -H "X-GitHub-Api-Version: 2026-03-10" \
      "https://api.github.com/orgs/${OWNER}/packages/container/${PACKAGE_NAME}/versions?per_page=100&page=${PAGE}"
  )"

  COUNT="$(jq 'length' <<< "$RESPONSE")"

  if [[ "$COUNT" -eq 0 ]]; then
    break
  fi

  # Determine whether NEW_TAG exists at all
  if jq -e \
      --arg target "$NEW_TAG" \
      '.[] | select(.metadata.container.tags | index($target))' \
      <<< "$RESPONSE" >/dev/null; then
    TAG_FOUND=true

    # Find a SemVer tag associated with the same package version
    CURRENT_VERSION="$(
      jq -r \
        --arg target "$NEW_TAG" \
        '
        .[]
        | select(.metadata.container.tags | index($target))
        | .metadata.container.tags[]
        | select(
            test("^v?[0-9]+\\.[0-9]+\\.[0-9]+([-+][0-9A-Za-z.-]+)?$")
          )
        ' <<< "$RESPONSE" |
        head -n 1
    )"

    break
  fi

  PAGE=$((PAGE + 1))
done

# Now move the tag if the source version is newer than the current version (if any)
if [[ "$TAG_FOUND" == true ]]; then

  if [[ -z "$CURRENT_VERSION" ]]; then
    echo "Error: tag '$NEW_TAG' exists, but no semantic version tag"
    echo "could be found on the same GHCR image."
    echo "Refusing to move the tag because its current version cannot be determined."
    exit 1
  fi

  echo "Existing tag '$NEW_TAG' currently points to version: $CURRENT_VERSION"

  if semver_gt "$SOURCE_VERSION" "$CURRENT_VERSION"; then
    echo "$SOURCE_VERSION is newer than $CURRENT_VERSION. Moving '$NEW_TAG' to $SOURCE_VERSION."
  else
    echo "$SOURCE_VERSION is not newer than $CURRENT_VERSION. Keeping '$NEW_TAG' on $CURRENT_VERSION."
    exit 0
  fi

else
  echo "Tag '$NEW_TAG' does not currently exist. Creating it for version $SOURCE_VERSION."
fi

echo "Copying manifest to new tag..."
docker buildx imagetools create -t "$TARGET_IMAGE" "$SOURCE_IMAGE"

echo "Done! '$NEW_TAG' now points to version $SOURCE_VERSION."
