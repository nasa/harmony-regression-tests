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

retry 5 scp -v -F sshconfig -i .identity -r test "ec2-user@${INSTANCE_ID}:"
# It can take a couple minutes for docker to be available on the instance
retry 10 ssh -F sshconfig -i .identity "ec2-user@${INSTANCE_ID}" "cd test && make image"
set +e
ssh -F sshconfig -i .identity "ec2-user@${INSTANCE_ID}" "cd test && make run HARMONY_HOST_URL=${HARMONY_HOST_URL}"
exit_code=$?
set -e
# copy the output to here
retry 5 scp -F sshconfig -i .identity "ec2-user@${INSTANCE_ID}:test/output/*.ipynb" ./output

# return the exit code form running the tests
exit $exit_code