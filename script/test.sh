#!/bin/bash

set -ex

if [[ -z "${HARMONY_ENVIRONMENT}" ]]; then
  echo "HARMONY_ENVIRONMENT must be set to run this script"
  exit 1
fi

function retry {
  set +e
  local retries=$1
  shift

  local count=0
  until "$@"; do
    exit=$?
    count=$(($count + 1))
    if [ $count -lt $retries ]; then
      sleep 10
      echo "Retry $count/$retries exited $exit, retrying"
    else
      echo "Retry $count/$retries exited $exit, no more retries left."
      set -e
      return $exit
    fi
  done
  set -e
  return 0
}

# create the test environment
cd ../terraform
terraform init
terraform apply -auto-approve
instance_id=$(terraform output -json harmony_regression_test_instance_id | jq -r .id)
# run the tests on the created EC2 instance
cd ..
retry 5 scp -rT test "ec2-user@${instance_id}:"
retry 5 ssh "ec2-user@${instance_id}" "cd test && make image"
set +e
ssh "ec2-user@${instance_id}" "cd test && make run HARMONY_ENVIRONMENT=${HARMONY_ENVIRONMENT}"
exit_code=$?
set -e
# copy the output to here
retry 5 scp "ec2-user@${instance_id}:test/output/*.ipynb" ./output
# destroy the test environment 
cd terraform
terraform destroy -auto-approve

# return the exit code form running the tests
exit $exit_code