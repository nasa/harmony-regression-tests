#!/bin/bash

set -euo pipefail

# Usage:
# ./add-ghcr-tag.sh <source-image> <new-tag>
#
# Example:
# ./add-ghcr-tag.sh ghcr.io/nasa/regression-tests-casper:1.1.1 hoss1.2.6_maskfill1.3.3

SOURCE_IMAGE="$1"
NEW_TAG="$2"

# Extract image name without tag
IMAGE_NAME="${SOURCE_IMAGE%%:*}"

TARGET_IMAGE="${IMAGE_NAME}:${NEW_TAG}"

echo "Source image: $SOURCE_IMAGE"
echo "New image tag: $TARGET_IMAGE"

# Authenticate to GHCR (expects GHCR_TOKEN env var)
if [[ -z "${GHCR_TOKEN:-}" ]]; then
  echo "Error: GHCR_TOKEN environment variable not set"
  exit 1
fi

echo "$GHCR_TOKEN" | docker login ghcr.io -u "${GHCR_USERNAME:-}" --password-stdin

# Copy the manifest directly in the registry without pulling any layers.
# This preserves the original multi-platform manifest list and avoids
# platform-mismatch errors when running on a different architecture.
echo "Copying manifest to new tag..."
docker buildx imagetools create -t "$TARGET_IMAGE" "$SOURCE_IMAGE"

echo "Done! New tag created: $TARGET_IMAGE"
