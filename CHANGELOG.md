# CHANGELOG

The harmony-regression-tests repository does not follow semantic
versioning. Rather than a static releases, this repository contains of a number
of regression tests that are each semi-independent.  This CHANGELOG file should be used
to document pull requests to this repository.

## 2024-08-29 ([#92](https://github.com/nasa/harmony-regression-tests/pull/92))

- Adds NSIDC ICESat2 Regression test suite.

- Adds `shared_utils` functionality. This directory contains routines that are commonly used in regression tests and limits code duplication. To include the `shared_utils` directory in your docker container, Update the Makefile to add a shared_utils build arg. E.g. `--build-arg shared_utils=true` (see the nsidc-icesat2-image target)



## 2024-08-05 ([#86](https://github.com/nasa/harmony-regression-tests/pull/86))

- Adds this file to capture changes to the repository.

- Adds pre-commit.ci behavior to the repository. This setup ensures consistent code style, catches common errors, and maintains file hygiene across the project.

- Updates the base image for all regression tests to `mambaorg/micromamba:1.5.8-jammy`
