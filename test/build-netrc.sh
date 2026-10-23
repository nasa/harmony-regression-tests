#!/bin/bash
# script that runs in a harmony regression test to create a .netrc file to allow for EDL access.

if [ -f "${env_sub_dir}/fetch-edl-credentials.py" ]; then
  source <(python3 "${env_sub_dir}/fetch-edl-credentials.py")
fi

local_edl_user=${EDL_USER:-need_to_set_EDL_USER}
local_edl_password=${EDL_PASSWORD:-neet_to_set_EDL_PASSWORD}

netrc_default="machine urs.earthdata.nasa.gov login ${local_edl_user} password ${local_edl_password}\nmachine uat.urs.earthdata.nasa.gov login ${local_edl_user} password ${local_edl_password}"

echo -e $netrc_default > .netrc
