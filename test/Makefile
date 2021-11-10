harmony-image: Dockerfile harmony/environment.yaml
	docker build -t harmony/regression-tests-harmony:latest -f ./Dockerfile --build-arg notebook=Harmony.ipynb --build-arg sub_dir=harmony .

# asf-gdal-image: Dockerfile asf-gdal/environment.yaml
#docker build -t harmony/regression-tests-asf-gdal:latest -f ./Dockerfile --build-arg notebook=GDAL_Subsetter_Regression.ipynb --build-arg sub_dir=asf-gdal .

harmony-regression-image: Dockerfile harmony-regression/environment.yaml
	docker build -t harmony/regression-tests-harmony-regression:latest -f ./Dockerfile --build-arg notebook=HarmonyRegression.ipynb --build-arg sub_dir=harmony-regression .

sds-image: Dockerfile sds/environment.yaml
	docker build -t harmony/regression-tests-sds:latest -f ./Dockerfile --build-arg notebook=SDS_Regression.ipynb --build-arg sub_dir=sds .

images: harmony-image harmony-regression-image sds-image #asf-gdal-image
