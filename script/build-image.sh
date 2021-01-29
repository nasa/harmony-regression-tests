#!/bin/bash

set -e

image="harmony/regression-tests"
tag=${1:-latest}

docker build -t ${image}:${tag} .
