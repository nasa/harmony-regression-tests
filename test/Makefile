harmony-image: Dockerfile harmony/environment.yaml
	docker build -t harmony/regression-tests-harmony:latest -f ./Dockerfile --build-arg notebook=Harmony.ipynb --build-arg sub_dir=harmony .

harmony-regression-image: Dockerfile harmony-regression/environment.yaml
	docker build -t harmony/regression-tests-harmony-regression:latest -f ./Dockerfile --build-arg notebook=HarmonyRegression.ipynb --build-arg sub_dir=harmony-regression .

hga-image: Dockerfile hga/environment.yaml
	docker build -t harmony/regression-tests-hga:latest -f ./Dockerfile --build-arg notebook=HGA_Regression.ipynb --build-arg sub_dir=hga .

n2z-image: Dockerfile sds/environment.yaml
	docker build -t harmony/regression-tests-n2z:latest -f ./Dockerfile --build-arg notebook=N2Z_Regression.ipynb --build-arg sub_dir=n2z .

sds-image: Dockerfile sds/environment.yaml
	docker build -t harmony/regression-tests-sds:latest -f ./Dockerfile --build-arg notebook=SDS_Regression.ipynb --build-arg sub_dir=sds .

swath-projector-image: Dockerfile swath-projector/environment.yaml
	docker build -t harmony/regression-tests-swath-projector:latest -f ./Dockerfile --build-arg notebook=SwathProjector_Regression.ipynb --build-arg sub_dir=swath-projector .

images: harmony-image harmony-regression-image hga-image n2z-image sds-image swath-projector
