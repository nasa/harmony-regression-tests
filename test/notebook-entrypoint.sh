#!/bin/bash
# script to act as the entrypoint for running harmony regression tests in their containers.

export PATH=/opt/conda/envs/papermill-${env_sub_dir}/bin:$PATH

if ! /bin/bash /workdir/build-netrc.sh; then
  echo "Failed to build .netrc; aborting before running the notebook." >&2
  exit 1
fi

mkdir -p /workdir/output/${env_sub_dir}

export NETRC=/workdir/.netrc

start=$(date -u +"%Y-%m-%dT%H:%M:%S.%3NZ")
papermill --cwd ${env_sub_dir} ${env_sub_dir}/${env_notebook} /workdir/output/${env_sub_dir}/Results.ipynb -p harmony_host_url $harmony_host_url -k python3
exit_code=$?
end=$(date -u +"%Y-%m-%dT%H:%M:%S.%3NZ")

status="passed"
if [ $exit_code -ne 0 ]; then
  status="failed"
fi

if [ "${ASTRA:-false}" = "true" ]; then
  if ! python3 /workdir/report.py "$status" "$start" "$end"; then
    echo "Failed to submit results to the reporting service." >&2
    exit_code=1
  fi
fi

exit $exit_code
