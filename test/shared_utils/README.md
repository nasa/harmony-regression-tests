## This is directory that contains common utility functions that can be shared across regression tests.

This directory can be included in your test suite by adding a build-arg to the docker build command in the Makefile.

```sh
nsidc-icesat2-image: Dockerfile nsidc-icesat2/environment.yaml
	docker build -t ghcr.io/nasa/regression-tests-nsidc-icesat2:latest -f ./Dockerfile \
	--build-arg notebook=NSIDC-ICESAT2_Regression.ipynb --build-arg sub_dir=nsidc-icesat2 --build-arg shared_utils=true .
```



Doing this will cause this directory and all its files to be included at `/workdir/shared_utils` in your container.

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
