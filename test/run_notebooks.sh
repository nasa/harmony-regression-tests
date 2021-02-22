#!/bin/bash

RED='\033[0;31m'
NC='\033[0m' # No Color

echo "Running regression tests"

# Add Docker images created in Makefile here
images=(harmony-regression)

# launch all the docker containers and store their process IDs
for image in ${images[@]}; do
  PIDS+=(${image},$(docker run -d -v ${PWD}/output:/root/output -v ${PWD}/${image}:/root/${image} --env harmony_host_url="${HARMONY_HOST_URL}" "harmony/regression-tests-${image}:latest"))
done

# wait for processes to finish and store each exit code into array STATUS'
for name_pid in ${PIDS[@]}; do
  IFS=","
  set -- $name_pid
  name=$1
  pid=$2
  code=$(docker container wait ${pid})
  EXIT_CODES+=(${code})
  NAMES+=(${name})
done

# check to see if any of the docker runs errored
i=0
exit_code=0
for code in ${EXIT_CODES[@]}; do
  name=${NAMES[$i]}
  if [[ ${code} -ne 0 ]]; then
    echo -e "${RED}Test suite ${name} failed with exit code ${code}${NC}"
    exit_code=1
  fi
  ((i+=1))
done

exit ${exit_code}
