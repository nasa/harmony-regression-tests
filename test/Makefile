.PHONY: run

image: pyproject.toml poetry.lock Dockerfile Harmony.ipynb
	docker build -t harmony/regression-tests:latest .

run:
	docker run -v ${PWD}/output:/root/output --env environment=${HARMONY_ENVIRONMENT} harmony/regression-tests:latest

all: image run
