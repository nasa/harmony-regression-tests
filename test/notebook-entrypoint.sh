#!/bin/bash
# script to act as the entrypoint for running harmony regression tests in their containers.

export PATH=/opt/conda/envs/papermill/bin:$PATH

/bin/bash /root/build-netrc.sh

mkdir -p /root/output/${env_sub_dir}

papermill --cwd ${env_sub_dir} ${env_sub_dir}/${env_notebook} /root/output/${env_sub_dir}/Results.ipynb -p harmony_host_url $harmony_host_url
