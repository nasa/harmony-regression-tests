harmony-image: Dockerfile harmony/environment.yaml
	docker build -t harmony/regression-tests-harmony:latest -f ./Dockerfile --build-arg notebook=Harmony.ipynb --build-arg sub_dir=harmony .

harmony-regression-image: Dockerfile harmony-regression/environment.yaml
	docker build -t harmony/regression-tests-harmony-regression:latest -f ./Dockerfile --build-arg notebook=HarmonyRegression.ipynb --build-arg sub_dir=harmony-regression .

hga-image: Dockerfile hga/environment.yaml
	docker build -t harmony/regression-tests-hga:latest -f ./Dockerfile --build-arg notebook=HGA_Regression.ipynb --build-arg sub_dir=hga .

hoss-image: Dockerfile hoss/environment.yaml
	docker build -t harmony/regression-tests-hoss:latest -f ./Dockerfile --build-arg notebook=HOSS_Regression.ipynb --build-arg sub_dir=hoss .

n2z-image: Dockerfile n2z/environment.yaml
	docker build -t harmony/regression-tests-n2z:latest -f ./Dockerfile --build-arg notebook=N2Z_Regression.ipynb --build-arg sub_dir=n2z .

regridder-image: Dockerfile regridder/environment.yaml
	docker build -t harmony/regression-tests-regridder:latest -f ./Dockerfile --build-arg notebook=Regridder_Regression.ipynb --build-arg sub_dir=regridder .

swath-projector-image: Dockerfile swath-projector/environment.yaml
	docker build -t harmony/regression-tests-swath-projector:latest -f ./Dockerfile --build-arg notebook=SwathProjector_Regression.ipynb --build-arg sub_dir=swath-projector .

trajectory-subsetter-image: Dockerfile trajectory-subsetter/environment.yaml
	docker build -t harmony/regression-tests-trajectory-subsetter:latest -f ./Dockerfile --build-arg notebook=TrajectorySubsetter_Regression.ipynb --build-arg sub_dir=trajectory-subsetter .

variable-subsetter-image: Dockerfile variable-subsetter/environment.yaml
	docker build -t harmony/regression-tests-variable-subsetter:latest -f ./Dockerfile --build-arg notebook=VariableSubsetter_Regression.ipynb --build-arg sub_dir=variable-subsetter .

images: harmony-image harmony-regression-image hga-image hoss-image n2z-image swath-projector-image trajectory-subsetter-image variable-subsetter-image
