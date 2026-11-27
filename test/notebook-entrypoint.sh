#!/bin/bash
# script to act as the entrypoint for running harmony regression tests in their containers.

export PATH=/opt/conda/envs/papermill-${env_sub_dir}/bin:$PATH

if ! /bin/bash /workdir/build-netrc.sh; then
  echo "Failed to build .netrc; aborting before running the notebook." >&2
  exit 1
fi

output_dir=/workdir/output/${env_sub_dir}
mkdir -p ${output_dir}
# Remove results from any previous run so they cannot be mistaken for this one.
rm -f ${output_dir}/Results.ipynb ${output_dir}/test_results.json ${output_dir}/junit.xml ${output_dir}/summary.md

export NETRC=/workdir/.netrc

start=$(date -u +"%Y-%m-%dT%H:%M:%S.%3NZ")
papermill --cwd ${env_sub_dir} ${env_sub_dir}/${env_notebook} ${output_dir}/Results.ipynb -p harmony_host_url $harmony_host_url -k python3
exit_code=$?
end=$(date -u +"%Y-%m-%dT%H:%M:%S.%3NZ")

status="passed"
if [ $exit_code -ne 0 ]; then
  status="failed"
fi

# Generate per-test results (test_results.json, junit.xml and summary.md).
# Failure to generate the report does not change the test suite result.
if ! python3 /workdir/notebook_report.py ${output_dir}/Results.ipynb ${env_sub_dir} ${output_dir} \
  --notebook-name ${env_notebook} --notebook-status $status; then
  echo "Failed to generate per-test results report." >&2
fi

if [ "${ASTRA:-false}" = "true" ]; then
  if ! python3 /workdir/report.py "$status" "$start" "$end"; then
    echo "Failed to submit results to the reporting service." >&2
    exit_code=1
  fi
fi

exit $exit_code
