## This directory contains common utility functions that can be shared across regression tests.

## Include the build arg on the Makefile for your tests

This directory can be included in your test suite by adding a build-arg to the docker build command in the Makefile.

```sh
nsidc-icesat2-image: Dockerfile nsidc-icesat2/environment.yaml
	docker build -t ghcr.io/nasa/regression-tests-nsidc-icesat2:latest -f ./Dockerfile \
	--build-arg notebook=NSIDC-ICESAT2_Regression.ipynb --build-arg sub_dir=nsidc-icesat2 --build-arg shared_utils=true .
```

Doing this will cause this directory and all its files to be included at `/workdir/shared_utils` in your container when you are working locally.

## Update github workflows to include the build arg for your tests.

To include the shared_utils directory on the regression image built by GitHub you add a `shared_utils` key to the service matrix under your service like was done for the trajectory subsetter in the `.github/workflows/build-all-images.yml` file.

```yml
          -
            image: "trajectory-subsetter"
            notebook: "TrajectorySubsetter_Regression.ipynb"
            shared-utils: "true"

```

## Include the necessary python packages in your test's environment.yaml

The test environment is determined by the environment.yaml in the test directory, but if you are using routines from `shared_utils` you will need to also update your test's `environment.yaml` to include the libraries that are imported in the shared modules. That means `harmony-py` to use routines from utilities.py and a recent version of `xarray` for ones from `compare.py`.  As always you should look in the files to see if there are new requirements.

For example the pip requirements in the nsidc_icesat2 environment file :
```
name: papermill-nsidc-icesat2
channels:
  - conda-forge
dependencies:
  - python=3.11.5
  - netCDF4
  - notebook=7.2.1
  - numpy
  - papermill
  - pip
  - pip:
    - harmony-py==0.4.15
    - xarray==2024.9.0
```

## Using the shared utility routines

To use routines from the `shared_utils` dir you need to add the `../shared_utils` directory to the Python module search path using `sys.path.append()` so that the modules will be found.

```python
## Import shared utility routines:
import sys

sys.path.append('../shared_utils')
from utilities import (
    print_error,
    print_success,
    submit_and_download,
)
from compare import compare_results_to_reference_file

print_success('yay! you imported the functions.')
```
