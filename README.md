# Harmony Regression Tests

Harmony regression tests run a series of self contained tests to ensure no
regressions occur when portions of harmony are changed.

The regression tests can be run multiple ways.  Locally in Docker against SIT,
UAT and Prod. This is the preferred method of verifying no regressons have
occurred, when the services have been modified.

Alternatively, each test can be run locally in a browser against SIT, UAT, PROD
or localhost (harmony-in-a-box). This is a good choice for test development and
verifying service changes do not cause regression failures. Generally you run
locally in the browser against a single service regression test.

## Install Prerequisites

* [Docker](https://www.docker.com/get-started) (to run locally in docker)


## Running the Tests Locally

Each test suite is run in a separate Docker container using a temporary Docker image
you must build before running.

From the `./test` directory make all of the regression images with:

    $ make images

*`make -j images` can be used to make the images in parallel (faster), although this may lead to
Docker Desktop instabilities*

### Running in Docker:

    $ cd test
    $ export HARMONY_HOST_URL=<url of Harmony in the target environment>
    $ export EDL_PASSWORD=<your EDL password>
    $ export EDL_USER=<your EDL username>
    $ export AWS_ACCESS_KEY_ID=<key for the target environment>
    $ export AWS_SECRET_ACCESS_KEY=<key secret for the target environment>
    $ ./run_notebooks.sh

Outputs can be found in the `tests/output/<image>` directory.

Notes:

1. *All notebooks require variable `EDL_USER` and `EDL_PASSWORD` to
be exported for authentication against earthdata login.  If you are including
the NetCDF-to-Zarr (n2z) tests, `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`
must be set to values for your current test environment to access the
created Zarr store.*

1. *It's possible to run a selection of notebooks by providing a list of images
   to run after the run_notebooks command.  e.g. `./run_notebooks.sh hga n2z`
   would run the `harmony GDAL adapter` and `NetCDF-to-Zarr` regression tests.*

1. *`HARMONY_HOST_URL` is the harmony base url for your target environment. e.g. `SIT` would be `https://harmony.sit.earthdata.nasa.gov`*


### Test in a Browser:

To run the tests:

1. Create an isolated python environment for the test you wish to run. You can
use the environment.yml of the test to [create the environment with
conda](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file)
or you can create the environment with another virtual env, just ensure all of
the requirement from the environment.yml file are installed. They will create
conda environments named `papermill-<image>`, and you should delete any existing
environment before installing from the environment.yml.

1. Start the jupyter server: `jupyter notebook`.
1. Browse and open the jupyter notebook file for the test. (`<image>_Regression.ipynb`)
1. Update the `harmony_host_url` in the notebook.
1. Run the tests.


## Notebook Development

Notebooks and support files should be placed in a subdirectory of the `test` directory.

For example, in the `harmony` directory we have

```
├── Harmony.ipynb
├── __init__.py
├── environment.yaml
└── util.py
```

 Notebook dependencies should be listed in file named `environment.yaml` at the top level of the
 subdirectory. The `name` field in the file should be `papermill`. For example:

 ```yaml
name: papermill-<IMAGE>
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.7
  - jupyter
  - requests
  - netcdf4
  - matplotlib
  - papermill
  - pytest
  - ipytest
  - pip:
    - harmony-py
```

## μmamba (micromamba)

To increase runtime efficiency, the build relies on
[micromamba](https://mamba.readthedocs.io/en/latest/user_guide/micromamba.html).
Micromamba and mamba are meant to be drop in replacements for miniconda and
conda. The fast solving allows us to skip creating a conda-lock file, and the
dependency management is entirely defined by the `environment.yaml` file.

Test notebooks should not rely on other forms of dependency management or expect user input.
They _should_ utilize the `harmony_host_url` global variable to communicate with Harmony
or to determine the Harmony environment. This variable is set by `papermill` - see the
`Harmony.ipynb` for how to make use of this variable. More information can be found
in the [papermill](https://papermill.readthedocs.io/en/latest/usage-parameterize.html)
documentation on setting parameters.

New test suites must be added to the `Makefile`. A new `name-image` target (where name is the name of
the test suite) should be added (see the `harmony-image` example), and the new image target
should be added as a dependency of the `images` target. The docker image should have a name like
`ghcr.io/nasa/regression-tests-<base_name>`, where `base_name` is the name of the test suite.


To build the test images on github, add a new matrix target that includes the
image base name and notbook name to the list of targets in the
`.github/workflows/build-all-images.yml` file.

Finally, add the image base name to the `all_images` array in the
`run_notebooks.sh` file and the `all_tests` array in `scripts/test-in-bamboo.sh` script. For instance,
if the new image is named `ghcr.io/nasa/regression-tests-foo`, then we would add
`foo` to both arrays.

The `run_notebooks.sh` file can be used as described above to run the test suite. Notebooks are
expected to exit with a non-zero exit code on failure when run from `papermill`.
