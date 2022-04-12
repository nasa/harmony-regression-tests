harmony-image: Dockerfile harmony/environment.yaml
	docker build -t harmony/regression-tests-harmony:latest -f ./Dockerfile --build-arg notebook=Harmony.ipynb --build-arg sub_dir=harmony .

harmony-regression-image: Dockerfile harmony-regression/environment.yaml
	docker build -t harmony/regression-tests-harmony-regression:latest -f ./Dockerfile --build-arg notebook=HarmonyRegression.ipynb --build-arg sub_dir=harmony-regression .

hga-image: Dockerfile hga/environment.yaml
	docker build -t harmony/regression-tests-hga:latest -f ./Dockerfile --build-arg notebook=HGA_Regression.ipynb --build-arg sub_dir=hga .

sds-image: Dockerfile sds/environment.yaml
	docker build -t harmony/regression-tests-sds:latest -f ./Dockerfile --build-arg notebook=SDS_Regression.ipynb --build-arg sub_dir=sds .

images: harmony-image harmony-regression-image sds-image hga-image
