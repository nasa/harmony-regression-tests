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

function get_elb {
  # Figure out the Harmony load balancer - just grabs the first ELB for now - need to update to filter for the right one
  echo $(aws elbv2 describe-load-balancers | jq --arg host "harmony-$HARMONY_ENVIRONMENT-frontend" '.LoadBalancers[] | select(.LoadBalancerName == $host) | .DNSName' | tr -d '"')
}

case $HARMONY_ENVIRONMENT in
uat)
  harmony_host_url="https://harmony.uat.earthdata.nasa.gov"
  ;;
prod)
  harmony_host_url="https://harmony.earthdata.nasa.gov"
  ;;
sit|sandbox)
  harmony_host_url="http://$(get_elb)"
  ;;
*)
  echo "Valid environments are sit, uat, sandbox, and prod."
  exit 1
  ;;
esac

# create the test environment
cd ../terraform
terraform init
terraform apply -auto-approve -var "environment_name=${HARMONY_ENVIRONMENT}"
instance_id=$(terraform output -json harmony_regression_test_instance_id | jq -r .id)
# run the tests on the created EC2 instance
cd ..
retry 5 scp -F sshconfig -r test "ec2-user@${instance_id}:"
retry 5 ssh -F sshconfig "ec2-user@${instance_id}" "cd test && make image"
set +e
ssh -F sshconfig "ec2-user@${instance_id}" "cd test && make run HARMONY_HOST_URL=${harmony_host_url}"
exit_code=$?
set -e
# copy the output to here
retry 5 scp -F sshconfig "ec2-user@${instance_id}:test/output/*.ipynb" ./output
# destroy the test environment
# cd terraform
# terraform destroy -auto-approve -var "environment_name=${HARMONY_ENVIRONMENT}"

# return the exit code form running the tests
exit $exit_code