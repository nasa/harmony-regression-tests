#!/bin/bash

echo "Running regression test"

for file in $(ls notebooks/*.ipynb); do
  echo "$file"
  dir="/root/output/$(basename ${file} .ipynb)"
  mkdir "${dir}"
  poetry run papermill "${file}" "${dir}/Results.ipynb" -p harmony_host_url $harmony_host_url

done