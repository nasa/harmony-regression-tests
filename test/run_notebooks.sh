#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo "Running regression tests"

# Add Docker images created in Makefile here
images=(harmony harmony-regression sds hga n2z)

# launch all the docker containers and store their process IDs
for image in "${images[@]}"; do
    echo -e "Test suite ${image} starting"

    # insert AWS Credential variables for n2z only
    if [[ $image == "n2z" ]]; then
	creds="--env AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} --env AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}"
    else
	creds=""
    fi
    PIDS+=(${image},$(docker run -d -v ${PWD}/output:/root/output -v ${PWD}/${image}:/root/${image} ${creds} --env harmony_host_url="${HARMONY_HOST_URL}" "harmony/regression-tests-${image}:latest"))
done

trap ctrl_c SIGINT SIGTERM

function ctrl_c() {
  echo "Cleaning up"
  for name_comma_pid in ${PIDS[@]}; do
    name_pid=(${name_comma_pid//,/ })
    echo "Killing ${name_pid[0]}"
    docker kill "${name_pid[1]}" >/dev/null
  done
  echo "Exiting"
  exit 1
}

exit_code=0
# wait for processes to finish and store each exit code into array STATUS'
for name_comma_pid in ${PIDS[@]}; do
  name_pid=(${name_comma_pid//,/ })
  name=${name_pid[0]}
  pid=${name_pid[1]}

  echo "Waiting for ${name}."
  docker logs --follow "${pid}"
  code=$(docker container wait ${pid})

  if [[ ${code} -ne 0 ]]; then
    echo -e "${RED}Test suite ${name} failed with exit code ${code}${NC}" 1>&2;
    exit_code=1
  else
    echo -e "${GREEN}Test suite ${name} succeeded${NC}"
  fi
  docker rm ${pid} >/dev/null
done

if [[ ${exit_code} -ne 0 ]]; then
  echo "Tests completed (failed)"
else
  echo "Tests completed (passed)"
fi

exit ${exit_code}
