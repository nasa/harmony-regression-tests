.PHONY: run

image: pyproject.toml poetry.lock Dockerfile Harmony.ipynb
	docker build -t harmony/regression-tests:latest .

run:
	docker run --env environment=uat harmony/regression-tests:latest
