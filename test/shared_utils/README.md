## This directory contains common utility functions that can be shared across regression tests.

This directory can be included in your test suite by adding a build-arg to the docker build command in the Makefile.

```sh
nsidc-icesat2-image: Dockerfile nsidc-icesat2/environment.yaml
	docker build -t ghcr.io/nasa/regression-tests-nsidc-icesat2:latest -f ./Dockerfile \
	--build-arg notebook=NSIDC-ICESAT2_Regression.ipynb --build-arg sub_dir=nsidc-icesat2 --build-arg shared_utils=true .
```

Doing this will cause this directory and all its files to be included at `/workdir/shared_utils` in your container.

## Include the necessary python packages in your test's pip_requirements.txt

The test environment is determined by the environment.yaml in the test directory, but if you are including `shared_utils` you will need to also include harmony-py and either xarray-datatree or a fancy pinned version of xarray

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
    - git+https://github.com/pydata/xarray.git@ca2e9d6#egg=xarray
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
    compare_results_to_reference_file,
)

print_success('yay! you imported the functions.')
```
