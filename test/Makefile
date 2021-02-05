.PHONY: run

image: pyproject.toml poetry.lock Dockerfile
	docker build -t harmony/regression-tests:latest .

image2: Dockerfile.conda harmony/environment.yaml
	docker build  --no-cache -t harmony/regression-tests2:latest -f ./Dockerfile.conda --build-arg notebook=Harmony.ipynb --build-arg sub_dir=harmony .

image3: Dockerfile.conda gdal_subsetter/environment.yaml
	docker build  --no-cache -t harmony/regression-tests3:latest -f ./Dockerfile.conda --build-arg notebook=GDAL_Subsetter_Regression.ipynb --build-arg sub_dir=gdal_subsetter .


run:
	docker run -v ${PWD}/output:/opt/harmony/output --env harmony_host_url="${HARMONY_HOST_URL}" harmony/regression-tests:latest

run2:
	docker run -v ${PWD}/output:/root/output --env harmony_host_url="${HARMONY_HOST_URL}" harmony/regression-tests2:latest

run3:
	docker run -v ${PWD}/output:/root/output --env harmony_host_url="${HARMONY_HOST_URL}" harmony/regression-tests3:latest

