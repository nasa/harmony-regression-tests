#!/bin/bash

set -e

if [[ -z "${HARMONY_ENVIRONMENT}" ]]; then
  echo "HARMONY_ENVIRONMENT must be set to run this script"
  exit 1
fi

function get_elb {
  # Figure out the Harmony load balancer - just grabs the first ELB for now - need to update to filter for the right one
  echo $(aws elbv2 describe-load-balancers | jq --arg host "harmony-$HARMONY_ENVIRONMENT-frontend" '.LoadBalancers[] | select(.LoadBalancerName == $host) | .DNSName' | tr -d '"')
}

cd ..

deployenv='.deployenv'
if [ -e $deployenv ]; then
  rm $deployenv
fi

if [ -e .env ]; then
  echo "Using .env file"
  set -o allexport
  source .env
  set +o allexport
  cp .env $deployenv
else
  echo "AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}" >> $deployenv
  echo "AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}" >> $deployenv
  echo "REGRESSION_TEST_OUTPUT_BUCKET=${REGRESSION_TEST_OUTPUT_BUCKET}" >> $deployenv
fi

export AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION:-us-west-2}"
echo "AWS_DEFAULT_REGION=${AWS_DEFAULT_REGION}" >> $deployenv

# create the test environment
cd ./terraform
terraform init
terraform apply -auto-approve -var "environment_name=${HARMONY_ENVIRONMENT}"
instance_id=$(terraform output -json harmony_regression_test_instance_id | jq -r .id)

echo "intance_id = ${instance_id}"

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

echo "harmony host url: ${harmony_host_url}"

cd ..

# Set up SSH key
identity='.identity'

if [ -z ${SECRET_KEY_1+x} ]; then
  cp $SECRET_KEY_FILE $identity
else
  echo $SECRET_KEY_1$SECRET_KEY_2 | base64 -d > $identity
fi
chmod 0600 $identity

echo "INSTANCE_ID=${instance_id}" >> $deployenv
echo "HARMONY_HOST_URL=${harmony_host_url}" >> $deployenv

./script/build-image.sh

docker run --rm \
  -v $(pwd):/tmp \
  -e EDL_USERNAME \
  -e EDL_PASSWORD \
  harmony/regression-tests \
  './script/deploy-from-docker.sh'

# destroy the test environment (will be done in a separate step)
# cd terraform
# terraform destroy -auto-approve -var "environment_name=${HARMONY_ENVIRONMENT}"
