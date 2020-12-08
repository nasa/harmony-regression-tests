# Harmony Regression Tests

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

## Run the notebook

    $ papermill Harmony.ipynb Results.ipynb -p environment uat

## Start JupyterLab

    $ jupyter-lab
