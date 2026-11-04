#!/bin/bash
# script that runs in a harmony regression test to create a .netrc file to allow for EDL access.
set -euo pipefail

if [ "${ASTRA:-false}" = "true" ]; then
  # Captured via command substitution (not `source <(...)`) so a failure in
  # fetch-edl-credentials.py propagates its exit code here instead of being
  # silently swallowed, which would otherwise fall through to placeholder
  # credentials below.
  edl_env=$(python3 /workdir/fetch-edl-credentials.py)
  eval "$edl_env"
fi

local_edl_user=${EDL_USER:-need_to_set_EDL_USER}
local_edl_password=${EDL_PASSWORD:-neet_to_set_EDL_PASSWORD}

netrc_default="machine urs.earthdata.nasa.gov login ${local_edl_user} password ${local_edl_password}\nmachine uat.urs.earthdata.nasa.gov login ${local_edl_user} password ${local_edl_password}"

echo -e $netrc_default > .netrc
