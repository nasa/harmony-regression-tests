harmony-image: Dockerfile harmony/environment.yaml
	docker build -t harmony/regression-tests-harmony:latest -f ./Dockerfile --build-arg notebook=Harmony.ipynb --build-arg sub_dir=harmony .

asf-gdal-image: Dockerfile asf-gdal/environment.yaml
	docker build -t harmony/regression-tests-asf-gdal:latest -f ./Dockerfile --build-arg notebook=GDAL_Subsetter_Regression.ipynb --build-arg sub_dir=asf-gdal .

harmony-regression-image: Dockerfile harmony-regression/environment.yaml
	docker build -t harmony/regression-tests-harmony-regression:latest -f ./Dockerfile --build-arg notebook=HarmonyRegression.ipynb --build-arg sub_dir=harmony-regression .

images: harmony-image asf-gdal-image harmony-regression-image
