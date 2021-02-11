#!/bin/bash

set -ex

if [ -e .deployenv ]; then
  set -o allexport
  source .deployenv
  set +o allexport
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
      sleep 15
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

# copy the test directory to the EC2 instance
retry 5 scp -v -F sshconfig -i .identity -r test "ec2-user@${INSTANCE_ID}:"
# create a .netrc file on the EC2 instance
netrc_default="default login ${EDL_USER} password ${EDL_PASSWORD}"
retry 5 ssh -F sshconfig -i .identity "ec2-user@${INSTANCE_ID}" "echo \"${netrc_default}\" > ./test/.netrc"
# It can take a couple minutes for docker to be available on the instance
retry 10 ssh -F sshconfig -i .identity "ec2-user@${INSTANCE_ID}" "cd test && make -j images"
set +e
ssh -F sshconfig -i .identity "ec2-user@${INSTANCE_ID}" "cd test && export HARMONY_HOST_URL=${HARMONY_HOST_URL} && ./run_notebooks.sh"
exit_code=$?
set -e
# copy the output to here
retry 5 scp -r -F sshconfig -i .identity "ec2-user@${INSTANCE_ID}:test/output/*" ./output
# copy the output to s3
aws s3 cp output "s3://${REGRESSION_TEST_OUTPUT_BUCKET}" --recursive

# return the exit code form running the tests
exit $exit_code