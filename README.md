# Harmony Regression Tests

Harmony regression tests run a series of self contained tests to ensure no
regressions occur when portions of harmony are changed.

The regression tests can be run multiple ways.  Locally in Docker against SIT,
UAT and Prod. This is the preferred method of verifying no regressons have
occurred, when the services have been modified.

Alternatively, each test can be run locally in a browser against SIT, UAT, PROD
or localhost (Harmony-In-A-Box). This is a good choice for test development and
verifying service changes do not cause regression failures. Generally you run
locally in the browser against a single service regression test.

## Install Prerequisites

* [Docker](https://www.docker.com/get-started) (to run locally in docker)
* [git-lfs](https://git-lfs.com/) (to handle large files)


### Cloning the repostiory.

To work with this repository, ensure git-lfs (Git Large File Storage) is
installed on your system, as it's used to manage some large files stored in
GitHub.


## Running the Tests in GitHub:

Each test suite can be individually invoked via a GitHub workflow. Navigate to
the [GitHub Actions tab](https://github.com/nasa/harmony-regression-tests/actions)
for this repository. Then select the "Run test suite" workflow from the lefthand
menu. On the right hand side, click the "Run workflow" dropdown, and select the
correct Docker image and Harmony environment. That should manually trigger the
workflow.

The regression test GitHub actions can also be invoked through different event types
after a Harmony service is successfully deployed in Harmony or after a new version of
the Harmony server is deployed. Currently, only HOSS regression event type is supported.
The regression test event type for other Harmony services and Harmony server will be added
in the near future.

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

1. *`HARMONY_HOST_URL` is the harmony base url for your target
   environment. e.g. `SIT` would be `https://harmony.sit.earthdata.nasa.gov`*

1. *The `run_notebooks.sh` script cannot be used to test against
   Harmony-in-a-Box, i.e. `HARMONY_HOST_URL=http://localhost:3000`, due to
   Docker-in-Docker issues.  To test against a local Harmony instance, the
   notebook should be run manually on a Jupyter notebook server (e.g., in a
   browser).*

For more information on running a local Harmony instance, see the [Harmony
README](https://github.com/nasa/harmony/blob/main/README.md).


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

## Adding a new test suite:

1. Create a subdirectory within `test` that contains a notebook, environment,
   version and supporting files, as described in the next section. For ease, it
   is simplest to use the same string for the subdirectory name and the suite
   name.
1. Update the `test/Makefile` to be able to build a Docker image for the new
   test suite optionally including the shared utility directory:

   ```
   <new-suite-name>-image
       docker build -t ghcr.io/nasa/regression-tests-<new-suite-name>:latest -f ./Dockerfile --build-arg notebook=<new-test-notebook-name> --build-arg sub_dir=<new-suite-subdirectory> [--build-arg shared_utils=true] .
   ```

1. If you would like to use shared utilities to help ease the coding you can
   add the shared_util build-arg to your docker build command in the Makefile
   (as well as adding it as a key in the `workflow/build-all-images.yml` file).
   When enabed, this argument will include the `tests/shared_utils` directory
   as a sibling directory to your tests.  See the
   `tests/shared_utils/README.md` file for more information.

1. Update the `make images` rule to include building the new image.

   ```
   images: <pre existing rules already listed> <new-suite-name>-image
   ```
1. Update `test/run_notebooks.sh` to include the new test image in `all_images`:
   ```
   all_images=(<pre existing test suites> <new-suite-name>)
   ```
1. Update `script/test-in-bamboo.sh` to list the new suite name in `all_tests`.

With this in place, the new test suite should be able to be built and run:

```bash
EDL_USER=...
EDL_PASSWORD=...
HARMONY_HOST_URL=https://harmony.sit.earthdata.nasa.gov  # Or UAT or production
cd test
make <new-suite-name>-image
./run_notebooks.sh <new-suite-name>
```

After this, the test suite will need to be integrated with the GitHub workflow
to create a new version of the test image any time the related `version.txt`
file is updated. To do so, simply add a new target to the
[build-all-images.yml](https://github.com/nasa/harmony-regression-tests/blob/main/.github/workflows/build-all-images.yml) workflow in the `.github/workflows` directory:

```yaml
-
  image: <new-suite-name>
  notebook: <new-notebook-name>
```

The above is the basic structure for adding a new image to the CI/CD.  Two additional options `shared-utils` and `lfs` default to off, but can be over-ridden as they are for the nsidc-icesat2 image. `shared-utils` controls the addition of the `tests/shared_utils` directory into your image. `lfs` enables git LFS for your image and should be enabled only if you have added reference files with git LFS.

``` yaml
    -
      image: "nsidc-icesat2"
      notebook: "NSIDC-ICESAT2_Regression.ipynb"
      shared-utils: "true"
      lfs: "true"

```


## Test suite contents:

This section of the README describes the files that are expected in every test
suite subdirectory.

For example, in the `swath-projector` directory we have

```
├── reference_files
├── SwathProjector_Regression.ipynb
├── environment.yaml
├── utilities.py
└── version.txt
```

* `reference_files` contains golden template files for expected outputs of
   `tests`.  When you add new binary files to your test, you should configure
   them to to use Git LFS as well as keep them as small as possible.
* `SwathProjector_Regression.ipynb` is the regression test Jupyter notebook
  itself, running tests in cells. A test suite fails when a Jupyter notebook
  cell returns an error from the execution. Each regression test is designed to
  trigger this failure state for failed tests by asserting whether the output
  matches expectations.
* `environment.yaml` defines the conda environment and packages present in it.
  The Docker image for each test suite will use the appropriate environment
  file to define the conda environment the Jupyter notebook is executed within
  during regression testing.
* `utilities.py` is a file containing lower level helper functions. Usually,
  these helper functions have been removed from the notebook itself in order to
  simplify the appearance of the notebook and make it easier to understand upon
  test failures.
* `version.txt` contains a semantic version number for the latest version of
  the regression tests. This will be iterated either as new tests are added, or
  as the test outputs are updated. Changing this file in a PR, and then merging
  that PR to the `main` branch will trigger the publication of a new version of
  that regression test Docker image.

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

### Versioning

The regression test notebooks follow semantic versioning:

```
major.minor.patch
```

Every time a regression test suite is updated, the version number in the
`version.txt` file for that suite should be iterated by the appropriate type of
version increment. This will likely occur for one of three reasons:

* Adding, updating or removing tests within the notebook (or associated utility
  functionality).
* Adding or updating Python dependencies in the `environment.yaml` file for
  the test suite.
* Updating the overall Docker image for all test suites, in which case all
  suites should have their `version.txt` incremented.

The CI/CD pipeline for this repository will release a new Docker image for a
test suite to
[ghcr.io](https://github.com/orgs/nasa/packages?repo_name=harmony-regression-tests)
whenever a change in the relevant `version.txt` file is merged to the main
branch.

To use these changes in the overall Harmony CI/CD pipeline in Bamboo, the
environment variables for the appropriate regression test deployment
environment (SIT, UAT or production) should also be updated.

Note - the manual update step for Bamboo environment variables is brittle, and
improvements are being considered to make the choice of regression test image
version more automated.

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

## pre-commit hooks:

This repository uses [pre-commit](https://pre-commit.com/) to enable pre-commit
checking the repository for some coding standard best practices. These include:

* Removing trailing whitespaces.
* Removing blank lines at the end of a file.
* Ensure JSON files have valid formats.
* [ruff](https://github.com/astral-sh/ruff) Python linting checks.
* [black](https://black.readthedocs.io/en/stable/index.html) Python code
  formatting checks.

To enable these checks:

```bash
# Install pre-commit Python package:
pip install pre-commit

# Install the git hook scripts:
pre-commit install
```


If you have installed the hooks locally, when you commit your changes the hook
will validate your changes before actually committing to your repository. If
there are failures you will have to opportunity to fix them and add them to
your commit.

[pre-commit.ci](pre-commit.ci) is configured such that these same hooks will be
automatically run for every pull request. Because of this, it is highly
recommended that you also do this locally, since failures will prevent your PR
from being merged.
