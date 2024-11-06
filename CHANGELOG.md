# CHANGELOG

The harmony-regression-tests repository does not follow semantic
versioning. Rather than a static releases, this repository contains of a number
of regression tests that are each semi-independent.  This CHANGELOG file should be used
to document pull requests to this repository.

## 2024-11-06 ([#112](https://github.com/nasa/harmony-regression-tests/pull/112))

- Ensures conda packages are installed from conda-forge.

## 2024-10-31 ([#107](https://github.com/nasa/harmony-regression-tests/pull/107))

- Updates the net2cog regression test suite to ensure that failures do not
  happen for environments against which the test suite is not configured. Prior
  to this change an undefined variable was causing issues when running the test
  suite against production.

## 2024-10-30 ([#111](https://github.com/nasa/harmony-regression-tests/pull/111))

- Updates the swath-projector epsg reference file

## 2024-10-29 ([#95](https://github.com/nasa/harmony-regression-tests/pull/95))

- Adds LAADS DAAC subset-band-name test suite with subsetting EV_250_Aggr500_RefSB
  variable MOD02HKM collection as a starter test
- Utilizes functions from `shared_utils`

## 2024-10-16 ([#105](https://github.com/nasa/harmony-regression-tests/pull/105))

- Updates the HyBIG regression test suite to include a test specifying a variable
  in the request. This will ensure Harmony passes UMM-Var metadata to HyBIG and
  therefore allow HyBIG to use a custom colour map for the generated browse
  imagery.
- The comparisons within the HyBIG regression test suite also now derive their
  CRS and geotransform metadata from the `.aux.xml` file for each browse image.

## 2024-10-11 ([#104](https://github.com/nasa/harmony-regression-tests/pull/104))

- Migrates trajectory-subsetter to use `shared_utils`.
- Separates `shared_utils/utilities.py` into `utilities.py` and `compare.py` preventing `xarray` from being a mandatory requirement to use `shared_utils`.
- Updates `shared_utils` `README` to mention the github action updates needed to use `shared_utils`.
- Removes old `compare_results_to_reference_file` and renames `compare_results_to_reference_file_new` -> `compare_results_to_reference_file`
- Migrates nsidc_icesat2 tests to the new `shared_utils` structure and names.

## 2024-10-11 ([#103](https://github.com/nasa/harmony-regression-tests/pull/103))

- Update the ATL03 and ATL08 reference files in the `nsidc-icesat2` regression
  test notebook to adjust to the DAS-2205 bug fix.
- Updates the `shared_utils` function `compare_results_to_reference_file_new`
  to surround comparison assertion with a `try`/`except` so all tests are run
  even when a comparison fails.

## 2024-10-02 ([#99](https://github.com/nasa/harmony-regression-tests/pull/99))

- Adds NSIDC ICESat2 Production Regression configuration.
- Updates the `shared_utils` function `compare_results_to_reference_file_new`
  to take a new optional argument `identical` which defaults to `True` but if
  set to `False` the Datatree comparison falls back to an `equals` test
  ignoring metadata in its reference file comparisons.


## 2024-09-24 ([#92](https://github.com/nasa/harmony-regression-tests/pull/92))

- Adds NSIDC ICESat2 Regression test suite.

- Adds `shared_utils` functionality. This directory contains routines that are commonly used in regression tests and limits code duplication. To include the `shared_utils` directory in your docker container, update the `Makefile` to add a shared_utils build arg. E.g. `--build-arg shared_utils=true` and update the `.github/workflows/build-all-images.yml` to add a `shared-utils` key of "true" (see the nsidc-icesat2-image target in each file)

- Adds Git LFS functionality. Large files can be configured to use [Git LFS](https://git-lfs.com/). This PR configures the NSIDC reference files  `test/nsidc-icesat2/reference_files/*.h5`.


## 2024-08-30 ([#94](https://github.com/nasa/harmony-regression-tests/pull/94))

Add regression test for net2cog

## 2024-08-05 ([#86](https://github.com/nasa/harmony-regression-tests/pull/86))

- Adds this file to capture changes to the repository.

- Adds pre-commit.ci behavior to the repository. This setup ensures consistent code style, catches common errors, and maintains file hygiene across the project.

- Updates the base image for all regression tests to `mambaorg/micromamba:1.5.8-jammy`
