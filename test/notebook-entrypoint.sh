#!/bin/bash
# script to act as the entrypoint for running harmony regression tests in their containers.

export PATH=/opt/conda/envs/papermill/bin:$PATH

/bin/bash /workdir/build-netrc.sh

mkdir -p /workdir/output/${env_sub_dir}

export NETRC=/workdir/.netrc

papermill --cwd ${env_sub_dir} ${env_sub_dir}/${env_notebook} /workdir/output/${env_sub_dir}/Results.ipynb -p harmony_host_url $harmony_host_url
