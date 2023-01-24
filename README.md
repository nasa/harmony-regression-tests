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

The final way to run the tests is on an AWS EC2 instance via terraform and
Docker. This is how the tests run on the Bamboo server, but you can also run
the tests in AWS from your laptop with proper AWS credentials.

## Install Prerequisites

* [Docker](https://www.docker.com/get-started) (to run locally in docker)
* [terraform](https://www.terraform.io/) (to run from local on AWS EC2)

## Running the Tests Locally

Each test suite is run in a separate Docker container using a temporary Docker image
you must build before running.

From the `./test` directory make all of the regression images with:

    $ make images

*`make -j images` can be used to make the images in parallel (faster), although this may lead to
Docker Desktop*

### Running in Docker:

    $ cd test
    $ export HARMONY_HOST_URL=<url of Harmony in the target environment>
    $ export EDL_PASSWORD=<your EDL password>
    $ export EDL_user=<your EDL username>
    $ export AWS_ACCESS_KEY_ID=<key for the target environement>
    $ export AWS_SECRET_ACCESS_KEY=<key secret for the target environement>
    $ ./run_notebooks.sh

Outputs can be found in the `output/<image>` directory.

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


### test in a Browswer:

To run the tests:

1. Create an isolated python environment for the test you wish to run. You can
use the environment.yml of the test to [create the environment with
conda](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file)
or you can create the environment with another virtual env, just ensure all of
the requirement from the environment.yml file are installed. (Be careful, This
will always create a conda environment named papermill, so delete any existing
environment before installing from the environment.yml).
1. Start the jupyter server: `jupyter notebook`.
1. Browse and open the jupyter notebook file for the test. (`<image>_Regression.ipynb`)
1. Update the `harmony_host_url` in the notebook.
1. Run the tests.

### Test on AWS via terraform:

Harmony tests run in the AWS us-west-2 region.  We have provided a Terraform
deployment to ease test execution in this region.

#### Create Terraform Autovars File

In the `terraform` directory create a file called `key.auto.tfvars` and
add a single line indicating the name of the public key pair file that
should be used for the EC2 instance that runs the notebooks. ([Create a key pair on EC2](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/create-key-pairs.html))

Example:
```
key_name = "harmony-sit-my-key-name"
```

#### Execute the Tests

**Important**: The following steps allocate resources in AWS. To ease repeated
tests and troubleshooting, they also don't automatically clean up the instance
they create.  See "Clean Up Test Resources" to ensure you are minimizing costs
by cleaning up resources.

First create a `.env` file in the top level directory by copying in the
`dot_env` file and filling in the proper values. Then execute the following.

    $ cd script
    $ export HARMONY_ENVIRONMENT=<uat|sit|sandbox|prod>
    $ ./test.sh

Output will be uploaded to an existing bucket specified by the `REGRESSION_TEST_OUTPUT_BUCKET`
environment variable with a folder for each notebook.

#### Clean Up Test Resources

The prior scripts do not clean up allocated resources.  To remove the resources
used to run the test, run this command from the terraform directory.

    $ cd terraform
    $ terraform destroy

Tests outputs are not automatically deleted.

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
 name: papermill
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

## Generating a Dependency Lockfile
To increase runtime efficiency, the build relies on
[conda-lock](https://pypi.org/project/conda-lock/). This is used to create a
dependency lockfile that can be used by conda to more efficiently load
dependencies. The Docker build expects a lockfile named `conda-lock.yml` to
exist at the top level of a notebook directory (next to the `environment.yaml`
file).

To build the lockfile install `conda-lock` by following the directions provided
on its website. Then generate the lockfile for your notebook by running the
following:

```
conda-lock -f environment.yaml -p linux-64
```

Test notebooks should not rely on other forms of dependency management or expect user input.
They _should_ utilize the `harmony_host_url` global variable to communicate with Harmony
or to determine the Harmony environment. This variable is set by `papermill` - see the
`Harmony.ipynb` for how to make use of this variable. More information can be found
in the [papermill](https://papermill.readthedocs.io/en/latest/usage-parameterize.html)
documentation on setting parameters.

New test suites must be added to the `Makefile`. A new `name-image` target (where name is the name of
the test suite) should be added (see the `harmony-image` example), and the new image target
should be added as a dependency of the `images` target. The docker image should have a name like
`harmony/regression-tests-<base_name>`, where `base_name` is the name of the test suite.

To build the test images on github, add the `base_name` to the list of images
in the `.github/workflows/build-all-images.yml` file.

Finally, add the image base name to the `images` array on line 6 of the `run_notebooks.sh` file.
For instance, if the image is named `harmony/regression-tests-foo`, then we would add `foo` to the
array.

The `run_notebooks.sh` file can be used as described above to run the test suite. Notebooks are
expected to exit with a non-zero exit code on failure when run from `papermill`.
