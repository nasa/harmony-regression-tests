.PHONY: run

environment = uat

image: pyproject.toml poetry.lock Dockerfile Harmony.ipynb
	docker build -t harmony/regression-tests:latest .

run:
	docker run -v ${PWD}/output:/root/output --env environment=${environment} harmony/regression-tests:latest
