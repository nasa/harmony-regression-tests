# Harmony Regression Tests

# Running the Tests

## Install Prerequisites

* [Docker](https://www.docker.com/get-started)

## Build the Image & Run the Container

    $ cd test
    $ make image
    $ make run

By default this will run the tests against the UAT environment. To run
against a specific environment:

    $ make run environment=prod

Valid environment values are: sbx, sit, uat, prod.

# Notebook Development

**Note** - this section applies to the contents of the `test` directory

These prerequisites and steps are only needed if you want to do local
development on the project. 

## Prerequisites

* [pyenv](https://github.com/pyenv/pyenv)
* [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv)
* [poetry](https://python-poetry.org/)

## Install Python 3.8 (if needed)

    $ pyenv install 3.8.5

## Install dependencies

    $ pyenv virtualenv 3.8.5 harmony-rt
    $ pyenv local harmony-rt
    $ pyenv activate harmony-rt
    $ poetry install
    $ pyenv rehash

## Run the notebooks

    $ ./run_notebooks harmony_host_url=<url of Harmony in the target environment>
    
e.g., 
    
    $ ./run_notebooks harmony_host_url="https://harmony.sit.earthdata.nasa.gov"

Outputs will be in the `output` directory

## Start JupyterLab

    $ jupyter-lab
