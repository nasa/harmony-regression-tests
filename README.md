# Harmony Regression Tests

# Running the Tests

Each test suite is run in a separate Docker container using a temporary image built at test time.
`conda` is used for dependency management. The two steps for each test suite are building and
running the associated image.

## Install Prerequisites

* [Docker](https://www.docker.com/get-started)

## Set Up Authentication
Create a .netrc file in the `test` directory of this repository. It must contain
credentials for on logging into [Earthdata Login production](https://urs.earthdata.nasa.gov)
for tests run against Harmony production or
[Earthdata Login UAT](https://uat.urs.earthdata.nasa.gov) for Harmony SIT and
UAT environments.

Example `test/.netrc` that can log into both environments:

    machine urs.earthdata.nasa.gov login SOME_USER password SOME_PASSWORD
    machine uat.urs.earthdata.nasa.gov login SOME_UAT_USER password SOME_UAT_PASSWORD

This `.netrc` file will be copied to into the docker images and used when running the
notebooks. The `.gitignore` file will prevent this from being committed to the
git project, but we recommend providing a user account with minimal privileges
for test purposes.

## Build the Images

    $ cd test
    $ make images

`make -j images` can be used to make the images in parallel (faster), although this may lead to
Docker Desktop instabilities

## Run the Notebooks

    $ cd test
    $ export HARMONY_HOST_URL=<url of Harmony in the target environment>
    $ ./run_notebooks.sh

Outputs will be in the `output` directory.
`HARMONY_HOST_URL` for SIT would be `https://harmony.sit.earthdata.nasa.gov`

# Running the Tests in an AWS for Same-Region Data Access

Harmony runs in the AWS us-west-2 region and offers additional access methods for
clients running in the same region.  We have provided a Terraform deployment to
ease test execution in this region.

## Create Terraform Autovars File
In the `terraform` directory create a file called `key.auto.tfvars` and
add a single line indicating the name of the ssh public key file that
should be used for the EC2 instance that runs the notebooks.

This file name is the name of the S3 file created in the Harmony ssh key bucket as described in the Harmony project README.md.

Example:
```
key_name = "harmony-sit-my-key-name"
```

## Execute the Tests

**Important**: The following steps allocate resources in AWS. To ease repeated
tests and troubleshooting, they also don't automatically clean up the instance
they create.  See "Clean Up Test Resources" to ensure you are minimizing costs
by cleaning up resources.

First create a `.env` file in the top level directory by copying in the `dot_env` file and filling
in the proper values. Then execute the following.

    $ cd script
    $ export HARMONY_ENVIRONMENT=<uat|sit|sandbox|prod>
    $ ./test.sh

Output will be in the bucket specified with the `REGRESSION_TEST_OUTPUT_BUCKET`
environment variable with a folder for each notebook.

## Clean Up Test Resources

The prior scripts do not clean up allocated resources.  To remove the resources
used to run the test, run.

    $ terraform destroy

Tests outputs are not automatically deleted.

# Notebook Development

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

Finally, add the image base name to the `images` array on line 6 of the `run_notebooks.sh` file.
For instance, if the image is named `harmony/regression-tests-foo`, then we would add `foo` to the
array.

The `run_notebooks.sh` file can be used as described above to run the test suite. Notebooks are
expected to exit with a non-zero exit code on failure when run from `papermill`.
