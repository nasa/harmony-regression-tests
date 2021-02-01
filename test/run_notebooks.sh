#!/bin/bash

echo "Running regression tests"

for file in $(ls notebooks/*.ipynb); do
  echo "$file"
  dir="./output/$(basename ${file} .ipynb)"
  mkdir -p "${dir}"
  poetry run papermill "${file}" "${dir}/Results.ipynb" -p harmony_host_url $harmony_host_url

done