filtering-image: Dockerfile filtering/environment.yaml
	docker build -t ghcr.io/nasa/regression-tests-filtering:latest -f ./Dockerfile \
	--build-arg notebook=Filtering_Regression.ipynb --build-arg sub_dir=filtering .

harmony-image: Dockerfile harmony/environment.yaml
	docker build -t ghcr.io/nasa/regression-tests-harmony:latest -f ./Dockerfile \
	--build-arg notebook=Harmony.ipynb --build-arg sub_dir=harmony .

harmony-regression-image: Dockerfile harmony-regression/environment.yaml
	docker build -t ghcr.io/nasa/regression-tests-harmony-regression:latest -f ./Dockerfile \
	--build-arg notebook=HarmonyRegression.ipynb --build-arg sub_dir=harmony-regression .

hga-image: Dockerfile hga/environment.yaml
	docker build -t ghcr.io/nasa/regression-tests-hga:latest -f ./Dockerfile \
	--build-arg notebook=HGA_Regression.ipynb --build-arg sub_dir=hga .

hoss-image: Dockerfile hoss/environment.yaml
	docker build -t ghcr.io/nasa/regression-tests-hoss:latest -f ./Dockerfile \
	--build-arg notebook=HOSS_Regression.ipynb --build-arg sub_dir=hoss .

hybig-image: Dockerfile hybig/environment.yaml
	docker build -t ghcr.io/nasa/regression-tests-hybig:latest -f ./Dockerfile \
	--build-arg notebook=HyBIG_Regression.ipynb --build-arg sub_dir=hybig .

nsidc-icesat2-image: Dockerfile nsidc-icesat2/environment.yaml
	docker build -t ghcr.io/nasa/regression-tests-nsidc-icesat2:latest -f ./Dockerfile \
	--build-arg notebook=NSIDC-ICESAT2_Regression.ipynb --build-arg sub_dir=nsidc-icesat2 \
	--build-arg shared_utils=true .

regridder-image: Dockerfile regridder/environment.yaml
	docker build -t ghcr.io/nasa/regression-tests-regridder:latest -f ./Dockerfile \
	--build-arg notebook=Regridder_Regression.ipynb --build-arg sub_dir=regridder \
	--build-arg shared_utils=true .

smap-l2-gridder-image: Dockerfile smap-l2-gridder/environment.yaml
	docker build -t ghcr.io/nasa/regression-tests-smap-l2-gridder:latest -f ./Dockerfile \
	--build-arg notebook=smap-l2-gridder_Regression.ipynb --build-arg sub_dir=smap-l2-gridder \
	--build-arg shared_utils=true .

swath-projector-image: Dockerfile swath-projector/environment.yaml
	docker build -t ghcr.io/nasa/regression-tests-swath-projector:latest -f ./Dockerfile \
	--build-arg notebook=SwathProjector_Regression.ipynb --build-arg sub_dir=swath-projector .

subset-band-name-image: Dockerfile subset-band-name/environment.yaml
	docker build -t ghcr.io/nasa/regression-tests-subset-band-name:latest -f ./Dockerfile \
	--build-arg notebook=SubsetBandName_Regression.ipynb --build-arg sub_dir=subset-band-name \
	--build-arg shared_utils=true .

trajectory-subsetter-image: Dockerfile trajectory-subsetter/environment.yaml
	docker build -t ghcr.io/nasa/regression-tests-trajectory-subsetter:latest -f ./Dockerfile \
	--build-arg notebook=TrajectorySubsetter_Regression.ipynb --build-arg sub_dir=trajectory-subsetter \
	--build-arg shared_utils=true .

variable-subsetter-image: Dockerfile variable-subsetter/environment.yaml
	docker build -t ghcr.io/nasa/regression-tests-variable-subsetter:latest -f ./Dockerfile \
	--build-arg notebook=VariableSubsetter_Regression.ipynb --build-arg sub_dir=variable-subsetter .

geoloco-image: Dockerfile geoloco/environment.yaml
	docker build -t ghcr.io/nasa/regression-tests-geoloco:latest -f ./Dockerfile \
	--build-arg notebook=Geoloco_Regression.ipynb --build-arg sub_dir=geoloco .

net2cog-image: Dockerfile net2cog/environment.yaml
	docker build -t ghcr.io/nasa/regression-tests-net2cog:latest -f ./Dockerfile \
	--build-arg notebook=net2cog_Regression.ipynb --build-arg sub_dir=net2cog .

sambah-image: Dockerfile sambah/environment.yaml
	docker build -t ghcr.io/nasa/regression-tests-sambah:latest -f ./Dockerfile \
	--build-arg notebook=SAMBAH_Regression.ipynb --build-arg sub_dir=sambah \
	--build-arg shared_utils=true .

opera-rtc-s1-browse-image: Dockerfile opera-rtc-s1-browse/environment.yaml
	docker build -t ghcr.io/nasa/regression-tests-opera-rtc-s1-browse:latest -f ./Dockerfile \
	--build-arg notebook=opera-rtc-s1-browse_Regression.ipynb --build-arg sub_dir=opera-rtc-s1-browse .

images: filtering-image \
	harmony-image \
	harmony-regression-image \
	hga-image \
	hoss-image \
	hybig-image \
	nsidc-icesat2-image \
	regridder-image \
	smap-l2-gridder-image \
	subset-band-name-image \
	swath-projector-image \
	trajectory-subsetter-image \
	variable-subsetter-image \
	geoloco-image \
	net2cog-image \
	sambah-image \
	opera-rtc-s1-browse-image
