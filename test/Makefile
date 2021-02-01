.PHONY: run

image: pyproject.toml poetry.lock Dockerfile
	docker build -t harmony/regression-tests:latest .

run:
	docker run -v ${PWD}/output:/root/output --env harmony_host_url="${HARMONY_HOST_URL}" harmony/regression-tests:latest

